from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class ExampleVideo:
    key: str
    size: int

    @property
    def filename(self) -> str:
        return self.key.split("/")[-1]

    @property
    def action(self) -> str:
        # examples/videos/ex033-load-vehicle.mp4 -> load-vehicle
        name = self.filename
        if not name.startswith("ex") or "-" not in name:
            return "unknown"
        return name.split("-", 1)[1].rsplit(".", 1)[0]


def _run_meva_s3_ls() -> dict:
    # Reuse our existing public S3 listing script.
    p = subprocess.run(
        [
            sys.executable,
            "scripts/meva_s3.py",
            "ls",
            "--s3-uri",
            "s3://mevadata-public-01/examples/videos/",
            "--all",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(p.stdout)


def _to_https_url(key: str) -> str:
    # Public bucket supports virtual-hosted-style URLs.
    return f"https://mevadata-public-01.s3.amazonaws.com/{key}"


def _write_downloader_ps1(keys: List[str], out_path: Path, dest_dir: str) -> None:
    lines: List[str] = []
    lines.append('param([string]$OutDir = "' + dest_dir.replace('"', "") + '")')
    lines.append('$ErrorActionPreference = "Stop"')
    lines.append('New-Item -ItemType Directory -Force -Path $OutDir | Out-Null')
    lines.append("")
    lines.append("$items = @(")
    for idx, k in enumerate(keys):
        url = _to_https_url(k)
        name = k.split("/")[-1]
        comma = "," if idx != len(keys) - 1 else ""
        lines.append(f'  @{{ url = "{url}"; name = "{name}" }}{comma}')
    lines.append(")")
    lines.append("")
    lines.append("foreach ($it in $items) {")
    lines.append("  $dst = Join-Path $OutDir $it.name")
    lines.append("  if (Test-Path $dst) { Write-Host \"SKIP $($it.name)\"; continue }")
    lines.append("  Write-Host \"GET  $($it.name)\"")
    lines.append("  curl.exe -L --fail --retry 5 --retry-delay 2 -o $dst $it.url")
    lines.append("}")
    lines.append("Write-Host \"Done.\"")
    lines.append("")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def _write_manifest_yaml(keys: List[str], out_path: Path, dest_dir: str) -> None:
    # Keep this manifest simple and deterministic, without needing PyYAML at generation time.
    # (We already depend on PyYAML in runtime, but this script is a build helper.)
    clips: List[Tuple[str, str]] = []
    for i, k in enumerate(keys, start=1):
        name = k.split("/")[-1]
        stream_id = f"ex_{i:02d}_{name.rsplit('.',1)[0]}"
        path = str(Path(dest_dir) / name).replace("\\", "/")
        clips.append((stream_id, path))

    def emit_job(mode: str, anchor: str | None = None) -> List[str]:
        ls: List[str] = []
        ls.append("- type: per_stream")
        ls.append(f"  mode: {mode}")
        if anchor:
            ls.append(f"  clips: &{anchor}")
        else:
            ls.append("  clips: *clips")
        if anchor:
            for sid, p in clips:
                ls.append(f"  - stream_id: {sid}")
                ls.append(f"    path: {p}")
        ls.append("  output_dir: outputs/auto/per_stream/")
        return ls

    out: List[str] = []
    out.append("session: auto-generated")
    out.append("description: MEVA public examples/videos - curated 10-clip MVP demo set")
    out.append("jobs:")
    out.extend(emit_job("load", anchor="clips"))
    out.extend(emit_job("safety"))
    out.extend(emit_job("security"))
    out.extend(emit_job("timeline"))
    out.append("")

    out_path.write_text("\n".join(out), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-index", default="reports/meva_examples_video_index.md")
    ap.add_argument("--out-keys", default="batch/meva_examples_selected10_keys.txt")
    ap.add_argument("--out-manifest", default="batch/batch_manifest_meva_examples_selected10.yaml")
    ap.add_argument("--out-downloader", default="scripts/download_meva_examples_selected10.ps1")
    ap.add_argument("--dest-dir", default="data/videos/meva_examples_selected10")
    args = ap.parse_args()

    listing = _run_meva_s3_ls()
    objs = listing.get("objects") or []
    vids: List[ExampleVideo] = [ExampleVideo(key=o["Key"], size=int(o.get("Size", 0))) for o in objs]

    # Action inventory
    by_action: Dict[str, List[ExampleVideo]] = defaultdict(list)
    for v in vids:
        by_action[v.action].append(v)
    counts = Counter({a: len(vs) for a, vs in by_action.items()})

    # Curated 10 with 3x/3x/3x + 1 security-oriented clip.
    desired = [
        "heavy-carry",
        "load-vehicle",
        "unload-vehicle",
        "theft",
    ]
    selected: List[ExampleVideo] = []
    for act in desired:
        vs = sorted(by_action.get(act, []), key=lambda x: x.filename)
        need = 3 if act != "theft" else 1
        if len(vs) < need:
            raise SystemExit(f"Not enough videos for action={act!r} (need {need}, have {len(vs)})")
        selected.extend(vs[:need])

    # Stable ordering in outputs
    selected = sorted(selected, key=lambda x: x.filename)
    keys = [v.key for v in selected]

    # Write index markdown
    out_lines: List[str] = []
    out_lines.append("# MEVA Public Examples - Video Index")
    out_lines.append("")
    out_lines.append("Source: `s3://mevadata-public-01/examples/videos/`")
    out_lines.append(f"Total videos: `{len(vids)}`")
    out_lines.append("")
    out_lines.append("## Action Counts")
    out_lines.append("")
    out_lines.append("| Action | Count |")
    out_lines.append("|---|---:|")
    for act, c in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        out_lines.append(f"| `{act}` | {c} |")
    out_lines.append("")
    out_lines.append("## Selected 10 Clips (Curated MVP Set)")
    out_lines.append("")
    out_lines.append("These were chosen to ensure multiple clips per action (3+3+3) plus 1 security-relevant clip.")
    out_lines.append("")
    out_lines.append("| # | File | Action | Size (MB) | S3 Key |")
    out_lines.append("|---:|---|---|---:|---|")
    for i, v in enumerate(selected, start=1):
        out_lines.append(
            f"| {i} | `{v.filename}` | `{v.action}` | {v.size/1024/1024:.2f} | `{v.key}` |"
        )
    out_lines.append("")
    out_lines.append("## How To Get Multiple Clips Of The Same Action")
    out_lines.append("")
    out_lines.append("- In `examples/videos/`, the action is encoded directly in the filename: `exNNN-<action>.mp4`.")
    out_lines.append("- To get multiple clips of an action, pick multiple `exNNN` entries with the same `<action>` label.")
    out_lines.append("")

    out_index = Path(args.out_index)
    out_index.parent.mkdir(parents=True, exist_ok=True)
    out_index.write_text("\n".join(out_lines).rstrip() + "\n", encoding="utf-8")

    # Keys list
    out_keys = Path(args.out_keys)
    out_keys.parent.mkdir(parents=True, exist_ok=True)
    out_keys.write_text("\n".join(keys) + "\n", encoding="utf-8")

    # Downloader + manifest
    _write_downloader_ps1(keys, Path(args.out_downloader), args.dest_dir)
    _write_manifest_yaml(keys, Path(args.out_manifest), args.dest_dir)

    print(out_index.as_posix())
    print(out_keys.as_posix())
    print(Path(args.out_downloader).as_posix())
    print(Path(args.out_manifest).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
