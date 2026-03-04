from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from .client import NebiusVllmClient, build_messages_for_video, build_messages_text_only
from .media import file_to_data_uri, is_probably_url
from .parsing import parse_model_output
from .prompts import composite_report, incident_timeline, load_physics, ppe_safety, security_access


MODE_BUILDERS = {
    "load": load_physics.build_prompt,
    "safety": ppe_safety.build_prompt,
    "security": security_access.build_prompt,
    "timeline": incident_timeline.build_prompt,
}


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_mode(
    *,
    client: NebiusVllmClient,
    mode: str,
    video: str,
    out_dir: str,
    force: bool = False,
) -> Dict[str, Any]:
    if mode not in MODE_BUILDERS:
        raise ValueError(f"Unknown mode: {mode}")

    outp = Path(out_dir)
    outp.mkdir(parents=True, exist_ok=True)
    base = Path(video).name.replace(":", "_").replace("/", "_").replace("\\", "_")
    stem = base

    raw_path = outp / f"{stem}__{mode}.raw.txt"
    think_path = outp / f"{stem}__{mode}.think.txt"
    json_path = outp / f"{stem}__{mode}.json"

    if json_path.exists() and not force:
        return json.loads(json_path.read_text(encoding="utf-8"))

    if is_probably_url(video):
        video_url = video
    else:
        video_url = file_to_data_uri(video)

    def _call_model(messages: list[dict], *, extra_body: Optional[dict] = None) -> Any:
        # Some Nebius/vLLM deployments reject certain `mm_processor_kwargs` even though they are
        # recommended in the NVIDIA guide. Try with kwargs first, then retry without.
        try:
            return client.chat_completions(messages=messages, extra_body=extra_body)
        except RuntimeError as e:
            msg = str(e)
            if "Qwen3VLProcessor" in msg and "kwargs=" in msg and extra_body and "mm_processor_kwargs" in extra_body:
                eb = dict(extra_body)
                eb.pop("mm_processor_kwargs", None)
                if not eb:
                    eb = None
                return client.chat_completions(messages=messages, extra_body=eb)
            raise

    prompt = MODE_BUILDERS[mode]()
    messages = build_messages_for_video(prompt_text=prompt, video_url=video_url)
    extra_body = {"mm_processor_kwargs": client.mm_processor_kwargs()}

    resp = _call_model(messages, extra_body=extra_body)
    _write_text(raw_path, resp.content_text)

    try:
        think, parsed, _json_text = parse_model_output(resp.content_text)
    except ValueError:
        # Occasionally the model gets stuck in <think> and never emits JSON. Retry once with a
        # "JSON-only" instruction and tighter sampling to reduce rambling.
        retry_prompt = prompt.rstrip() + "\n\nIMPORTANT: Output ONLY valid JSON. Do NOT output <think> tags. No markdown fences."
        retry_messages = build_messages_for_video(prompt_text=retry_prompt, video_url=video_url)
        retry_extra = {
            "mm_processor_kwargs": client.mm_processor_kwargs(),
            "temperature": 0.2,
            "top_p": 0.9,
            "repetition_penalty": 1.1,
        }
        resp2 = _call_model(retry_messages, extra_body=retry_extra)
        retry_raw_path = outp / f"{stem}__{mode}.retry1.raw.txt"
        _write_text(retry_raw_path, resp2.content_text)
        think, parsed, _json_text = parse_model_output(resp2.content_text)

    if think is not None:
        _write_text(think_path, think + "\n")
    _write_json(json_path, parsed)
    return parsed


def run_full(
    *,
    client: NebiusVllmClient,
    video: str,
    out_dir: str,
    force: bool = False,
) -> Dict[str, Any]:
    load_out = run_mode(client=client, mode="load", video=video, out_dir=out_dir, force=force)
    safety_out = run_mode(client=client, mode="safety", video=video, out_dir=out_dir, force=force)
    security_out = run_mode(client=client, mode="security", video=video, out_dir=out_dir, force=force)
    timeline_out = run_mode(client=client, mode="timeline", video=video, out_dir=out_dir, force=force)

    prompt = composite_report.build_prompt(
        load_json=load_out,
        safety_json=safety_out,
        security_json=security_out,
        timeline_json=timeline_out,
    )

    # Composite is a second-pass CR2 call using structured outputs (text-only).
    messages = build_messages_text_only(prompt_text=prompt)

    resp = client.chat_completions(messages=messages)
    outp = Path(out_dir)
    base = Path(video).name.replace(":", "_").replace("/", "_").replace("\\", "_")

    raw_path = outp / f"{base}__full.raw.txt"
    think_path = outp / f"{base}__full.think.txt"
    json_path = outp / f"{base}__full.json"

    _write_text(raw_path, resp.content_text)
    think, parsed, _json_text = parse_model_output(resp.content_text)
    if think is not None:
        _write_text(think_path, think + "\n")
    _write_json(json_path, parsed)
    return parsed
