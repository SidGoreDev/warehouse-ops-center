from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Dict

import yaml

from .client import NebiusVllmClient, build_messages_for_video, build_messages_text_only
from .config import AppConfig
from .evaluation.evaluator import evaluate_results
from .media import is_probably_url, video_arg_to_video_url
from .parsing import parse_model_output
from .pipeline import MODE_BUILDERS, run_full, run_mode
from .prompts import composite_report


def _cmd_analyze(args: argparse.Namespace) -> int:
    cfg = AppConfig.load(require_endpoint=True)
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
    cfg = AppConfig.load(require_endpoint=True)
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


def _cmd_render(args: argparse.Namespace) -> int:
    cfg = AppConfig.load(require_endpoint=False)

    def mk_body(*, messages: list[dict], include_mm: bool) -> dict:
        body: dict = {
            "model": cfg.model,
            "messages": messages,
            "temperature": cfg.temperature,
            "top_p": cfg.top_p,
            "top_k": cfg.top_k,
            "presence_penalty": cfg.presence_penalty,
            "repetition_penalty": cfg.repetition_penalty,
            "max_tokens": cfg.max_tokens,
        }
        if cfg.seed is not None:
            body["seed"] = cfg.seed
        if include_mm:
            body["mm_processor_kwargs"] = {"fps": cfg.mm_fps, "do_sample_frames": cfg.mm_do_sample_frames}
        return body

    out: dict = {
        "note": "This command does not call Nebius. It prints the request payload(s) you will send.",
        "base_url": cfg.base_url,
        "endpoint": f"{cfg.base_url}/v1/chat/completions",
        "auth_header": "Authorization: Bearer <redacted>",
        "requests": [],
    }

    if args.mode != "full":
        prompt = MODE_BUILDERS[args.mode]()
        video_url = video_arg_to_video_url(args.video, embed=args.embed_video)
        msgs = build_messages_for_video(prompt_text=prompt, video_url=video_url)
        out["requests"].append({"mode": args.mode, "body": mk_body(messages=msgs, include_mm=True)})
    else:
        video_url = video_arg_to_video_url(args.video, embed=args.embed_video)
        for mode in ("load", "safety", "security", "timeline"):
            prompt = MODE_BUILDERS[mode]()
            msgs = build_messages_for_video(prompt_text=prompt, video_url=video_url)
            out["requests"].append({"mode": mode, "body": mk_body(messages=msgs, include_mm=True)})

        composite_prompt = composite_report.build_prompt(
            load_json={"...": "load_json_here"},
            safety_json={"...": "safety_json_here"},
            security_json={"...": "security_json_here"},
            timeline_json=[{"...": "timeline_json_here"}],
        )
        msgs = build_messages_text_only(prompt_text=composite_prompt)
        out["requests"].append({"mode": "composite_report", "body": mk_body(messages=msgs, include_mm=False)})

    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


def _cmd_parse(args: argparse.Namespace) -> int:
    raw_path = Path(args.raw)
    text = raw_path.read_text(encoding="utf-8")
    think, parsed, _json_text = parse_model_output(text)

    out_dir = Path(args.out_dir) if args.out_dir else raw_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    base = raw_path.name
    if base.endswith(".raw.txt"):
        base = base[: -len(".raw.txt")]
    else:
        base = raw_path.stem

    think_path = out_dir / f"{base}.think.txt"
    json_path = out_dir / f"{base}.json"

    if think is not None:
        if args.force or not think_path.exists():
            think_path.write_text(think + "\n", encoding="utf-8")
    if args.force or not json_path.exists():
        json_path.write_text(json.dumps(parsed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps({"think_path": str(think_path), "json_path": str(json_path)}, indent=2))
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

    pr = sp.add_parser("render", help="Print the exact vLLM request payload (offline).")
    pr.add_argument("--mode", required=True, choices=["load", "safety", "security", "timeline", "full"])
    pr.add_argument("--video", required=True, help="Path to local video or a URL/data: URI")
    pr.add_argument(
        "--embed-video",
        action="store_true",
        help="Embed local video as a base64 data: URI in the printed payload (can be very large).",
    )
    pr.set_defaults(func=_cmd_render)

    pp = sp.add_parser("parse", help="Parse a saved *.raw.txt model output into JSON + think files (offline).")
    pp.add_argument("--raw", required=True, help="Path to a saved raw output (e.g., outputs/clip__load.raw.txt)")
    pp.add_argument("--out-dir", default="", help="Output directory (default: same as raw file)")
    pp.add_argument("--force", action="store_true", help="Overwrite existing outputs")
    pp.set_defaults(func=_cmd_parse)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
