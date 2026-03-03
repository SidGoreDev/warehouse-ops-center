#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import yaml


def build_manifest(video_dir: Path, out_path: Path, *, limit: int) -> None:
    vids = []
    for ext in (".mp4", ".mov", ".mkv", ".avi"):
        vids.extend(sorted(video_dir.rglob(f"*{ext}")))
    vids = vids[:limit]
    clips = [{"stream_id": f"clip_{i+1:02d}", "path": str(p).replace("\\", "/")} for i, p in enumerate(vids)]

    manifest = {
        "session": "auto-generated",
        "description": f"Generated from {video_dir} (limit={limit})",
        "jobs": [],
    }
    for mode in ("load", "safety", "security", "timeline"):
        manifest["jobs"].append(
            {
                "type": "per_stream",
                "mode": mode,
                "clips": clips,
                "output_dir": "outputs/auto/per_stream/",
            }
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video-dir", default="data/videos", help="Directory containing videos (default: data/videos)")
    ap.add_argument("--out", default="batch/batch_manifest_auto.yaml", help="Output manifest path")
    ap.add_argument("--limit", type=int, default=8, help="Max videos to include")
    args = ap.parse_args()

    build_manifest(Path(args.video_dir), Path(args.out), limit=args.limit)
    print(f"Wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

