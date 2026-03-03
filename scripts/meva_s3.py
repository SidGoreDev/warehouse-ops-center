#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


BUCKET_DEFAULT = "mevadata-public-01"
S3_HTTPS_BASE = "https://{bucket}.s3.amazonaws.com/"


def _s3_https_url(bucket: str, key: str) -> str:
    key = key.lstrip("/")
    return S3_HTTPS_BASE.format(bucket=bucket) + urllib.parse.quote(key)


def _parse_s3_uri(s: str) -> tuple[str, str]:
    # s3://bucket/prefix...
    if not s.startswith("s3://"):
        raise ValueError("Expected s3:// URI")
    u = urllib.parse.urlparse(s)
    bucket = u.netloc
    key = u.path.lstrip("/")
    return bucket, key


def _list_v2(
    *,
    bucket: str,
    prefix: str,
    delimiter: str | None,
    max_keys: int,
    continuation_token: str | None = None,
) -> tuple[list[str], list[dict], bool, str | None]:
    params: dict[str, str] = {"list-type": "2", "prefix": prefix, "max-keys": str(max_keys)}
    if delimiter:
        params["delimiter"] = delimiter
    if continuation_token:
        params["continuation-token"] = continuation_token
    url = S3_HTTPS_BASE.format(bucket=bucket) + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url) as resp:
        xml = resp.read()

    root = ET.fromstring(xml)
    ns = ""
    if root.tag.startswith("{"):
        ns = root.tag.split("}")[0] + "}"

    common_prefixes = []
    for cp in root.findall(f".//{ns}CommonPrefixes/{ns}Prefix"):
        if cp.text:
            common_prefixes.append(cp.text)

    contents = []
    for c in root.findall(f".//{ns}Contents"):
        key = c.findtext(f"{ns}Key")
        size = c.findtext(f"{ns}Size")
        if not key:
            continue
        contents.append({"Key": key, "Size": int(size) if size is not None else None})

    is_trunc = (root.findtext(f"{ns}IsTruncated") or "false").lower() == "true"
    token = root.findtext(f"{ns}NextContinuationToken") if is_trunc else None
    return common_prefixes, contents, is_trunc, token


def cmd_ls(args: argparse.Namespace) -> int:
    if args.s3_uri:
        bucket, prefix = _parse_s3_uri(args.s3_uri)
    else:
        bucket = args.bucket
        prefix = args.prefix.lstrip("/")
    delimiter = "/" if args.delimiter else None

    all_cps: list[str] = []
    all_objs: list[dict] = []
    token: str | None = None
    is_trunc = False

    while True:
        cps, objs, is_trunc, token = _list_v2(
            bucket=bucket, prefix=prefix, delimiter=delimiter, max_keys=args.max_keys, continuation_token=token
        )
        all_cps.extend(cps)
        all_objs.extend(objs)
        if not args.all or not is_trunc:
            break

    out = {
        "bucket": bucket,
        "prefix": prefix,
        "common_prefixes": all_cps,
        "objects": all_objs,
        "is_truncated": is_trunc,
    }
    if is_trunc and token:
        out["next_token"] = token

    import json  # local import to keep top tidy

    print(json.dumps(out, indent=2))
    return 0


def _pick_per_camera(keys: list[str], cameras: list[str], per_camera: int) -> list[str]:
    # naive deterministic selection: first N matches per camera in listing order
    selected: list[str] = []
    counts: dict[str, int] = {c: 0 for c in cameras}
    cam_res = {c: re.compile(re.escape(c), re.IGNORECASE) for c in cameras}
    for k in keys:
        for c, rx in cam_res.items():
            if counts[c] >= per_camera:
                continue
            if rx.search(k):
                selected.append(k)
                counts[c] += 1
                break
        if all(v >= per_camera for v in counts.values()):
            break
    return selected


def cmd_plan(args: argparse.Namespace) -> int:
    bucket, hour_prefix = _parse_s3_uri(args.hour_prefix_s3)
    # Hour-level prefixes should be small, but we handle pagination defensively.
    objs: list[dict] = []
    token: str | None = None
    while True:
        cps, page_objs, is_trunc, token = _list_v2(
            bucket=bucket, prefix=hour_prefix, delimiter=None, max_keys=1000, continuation_token=token
        )
        if cps:
            print(
                "ERROR: hour prefix returned CommonPrefixes (expected objects only). Did you pass a non-hour prefix?",
                file=sys.stderr,
            )
            return 2
        objs.extend(page_objs)
        if not is_trunc:
            break

    keys = [o["Key"] for o in objs if o.get("Key")]
    exts = tuple(args.ext.lower().split(","))
    keys = [k for k in keys if k.lower().endswith(exts)]

    cameras = [c.strip() for c in args.cameras.split(",") if c.strip()]
    if not cameras:
        print("ERROR: no cameras specified", file=sys.stderr)
        return 2

    selected = _pick_per_camera(keys, cameras, args.per_camera)
    if not selected:
        print("ERROR: no files matched camera patterns at this prefix.", file=sys.stderr)
        return 2

    repo_root = Path(__file__).resolve().parent.parent
    out_list = repo_root / args.out_list
    out_list.parent.mkdir(parents=True, exist_ok=True)
    out_list.write_text("\n".join(selected) + "\n", encoding="utf-8")

    # Generate a PowerShell downloader using curl.exe.
    dl_ps1 = repo_root / args.download_script
    dl_ps1.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append("param(")
    lines.append("  [string]$OutDir = \"data\\\\meva\\\\raw\"")
    lines.append(")")
    lines.append("$ErrorActionPreference = 'Stop'")
    lines.append("New-Item -ItemType Directory -Force -Path $OutDir | Out-Null")
    lines.append("")
    lines.append(f"$bucket = \"{bucket}\"")
    lines.append(f"$base = \"{S3_HTTPS_BASE.format(bucket=bucket)}\"")
    lines.append("")
    lines.append("# Keys selected from MEVA public S3 via list-type=2; download with curl.exe")
    lines.append("$keys = @(")
    for i, k in enumerate(selected):
        comma = "," if i != len(selected) - 1 else ""
        lines.append(f"  \"{k}\"{comma}")
    lines.append(")")
    lines.append("")
    lines.append("foreach ($k in $keys) {")
    lines.append("  $rel = $k -replace '^.*/', ''")
    lines.append("  $out = Join-Path $OutDir $rel")
    lines.append("  if (Test-Path $out) { Write-Host \"SKIP $rel\"; continue }")
    lines.append("  $url = $base + [uri]::EscapeUriString($k)")
    lines.append("  Write-Host \"GET $rel\"")
    lines.append("  curl.exe -L --fail --retry 3 --retry-delay 2 -o $out $url")
    lines.append("}")
    lines.append("Write-Host \"Done.\"")
    dl_ps1.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("Wrote:")
    print(f"- Selected key list: {out_list}")
    print(f"- Download script:    {dl_ps1}")
    print("")
    print("Next:")
    print(f"- Run: powershell -File {dl_ps1.as_posix()} -OutDir data\\\\meva\\\\raw")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="meva_s3")
    sp = p.add_subparsers(dest="cmd", required=True)

    pls = sp.add_parser("ls", help="List prefixes/objects from the MEVA public S3 bucket (no aws cli required).")
    pls.add_argument("--s3-uri", default="", help="s3://bucket/prefix (recommended)")
    pls.add_argument("--bucket", default=BUCKET_DEFAULT, help="Bucket name (default: mevadata-public-01)")
    pls.add_argument("--prefix", default="drops-123-r13/", help="Key prefix (default: drops-123-r13/)")
    pls.add_argument("--delimiter", action="store_true", help="Use delimiter=/ to list 'directories'")
    pls.add_argument("--max-keys", type=int, default=200, help="Max keys (default: 200)")
    pls.add_argument("--all", action="store_true", help="Paginate until complete")
    pls.set_defaults(func=cmd_ls)

    ppl = sp.add_parser("plan", help="Pick a small set of hour-level clips and generate a downloader script.")
    ppl.add_argument(
        "--hour-prefix-s3",
        required=True,
        help="Hour-level prefix, e.g. s3://mevadata-public-01/drops-123-r13/<facility>/<date>/<hour>/",
    )
    ppl.add_argument("--cameras", required=True, help="Comma-separated camera patterns (e.g., G328,G329,G330)")
    ppl.add_argument("--per-camera", type=int, default=4, help="Files per camera (default: 4)")
    ppl.add_argument("--ext", default=".avi,.mp4", help="Extensions to include (comma-separated)")
    ppl.add_argument("--out-list", default="data/meva/meva_selected_keys.txt", help="Where to write selected key list")
    ppl.add_argument(
        "--download-script",
        default="scripts/download_meva_selected.ps1",
        help="Where to write the generated downloader script",
    )
    ppl.set_defaults(func=cmd_plan)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
