from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

import yaml

from .client import NebiusVllmClient
from .config import AppConfig
from .evaluation.evaluator import evaluate_results
from .pipeline import run_full, run_mode


def _cmd_analyze(args: argparse.Namespace) -> int:
    cfg = AppConfig.load()
    client = NebiusVllmClient(cfg)

    out_dir = args.out
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    if args.mode == "full":
        out = run_full(client=client, video=args.video, out_dir=out_dir, force=args.force)
    else:
        out = run_mode(client=client, mode=args.mode, video=args.video, out_dir=out_dir, force=args.force)

    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


def _cmd_batch(args: argparse.Namespace) -> int:
    cfg = AppConfig.load()
    client = NebiusVllmClient(cfg)

    manifest_path = Path(args.manifest)
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    jobs = manifest.get("jobs", [])
    if not isinstance(jobs, list):
        raise RuntimeError("batch manifest: 'jobs' must be a list")

    for job in jobs:
        jtype = job.get("type")
        if jtype == "per_stream":
            mode = job["mode"]
            clips = job["clips"]
            out_dir = job["output_dir"]
            for clip in clips:
                path = clip["path"]
                run_mode(client=client, mode=mode, video=path, out_dir=out_dir, force=args.force)
        elif jtype == "evaluation":
            results_dir = job["results_dir"]
            gt_dir = job["ground_truth_dir"]
            out_path = job.get("output", str(Path(results_dir) / "eval_report.json"))
            report = evaluate_results(results_dir=results_dir, ground_truth_dir=gt_dir)
            Path(out_path).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        else:
            raise RuntimeError(f"Unsupported job type: {jtype}")
    return 0


def _cmd_eval(args: argparse.Namespace) -> int:
    report = evaluate_results(results_dir=args.results, ground_truth_dir=args.ground_truth)
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="warehouse-ops-center")
    sp = p.add_subparsers(dest="cmd", required=True)

    pa = sp.add_parser("analyze", help="Run a single analysis mode on a single video.")
    pa.add_argument("--mode", required=True, choices=["load", "safety", "security", "timeline", "full"])
    pa.add_argument("--video", required=True, help="Path to local video or a URL/data: URI")
    pa.add_argument("--out", default="outputs", help="Output directory (default: outputs/)")
    pa.add_argument("--force", action="store_true", help="Re-run even if output files already exist")
    pa.set_defaults(func=_cmd_analyze)

    pb = sp.add_parser("batch", help="Run a batch manifest (YAML).")
    pb.add_argument("--manifest", required=True, help="Path to batch manifest YAML")
    pb.add_argument("--force", action="store_true", help="Re-run even if outputs already exist")
    pb.set_defaults(func=_cmd_batch)

    pe = sp.add_parser("eval", help="Evaluate saved results against ground truth.")
    pe.add_argument("--results", required=True, help="Directory of saved *.json outputs")
    pe.add_argument("--ground-truth", required=True, help="Ground truth directory")
    pe.add_argument("--out", required=True, help="Path to write eval report JSON")
    pe.set_defaults(func=_cmd_eval)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
