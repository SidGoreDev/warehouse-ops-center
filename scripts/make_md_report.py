from __future__ import annotations

import argparse
import datetime as _dt
import json
from pathlib import Path
import glob
from typing import Any, Dict, List, Tuple


MODES = ("load", "safety", "security", "timeline")


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _clip_key_from_filename(name: str) -> Tuple[str, str]:
    # "<clip>.mp4__<mode>.json"
    if "__" not in name:
        raise ValueError(f"Unexpected filename (missing '__'): {name}")
    clip, rest = name.split("__", 1)
    if not rest.endswith(".json"):
        raise ValueError(f"Unexpected filename (not .json): {name}")
    mode = rest[: -len(".json")]
    return clip, mode


def _safe_str(x: Any) -> str:
    if x is None:
        return ""
    return str(x)


def _md_escape(s: str) -> str:
    # Minimal table-safe escaping.
    return s.replace("|", "\\|").replace("\n", " ").strip()


def _shorten(s: str, n: int = 160) -> str:
    s = " ".join(_safe_str(s).split())
    if len(s) <= n:
        return s
    return s[: n - 3] + "..."


def _fmt_event_line(e: Dict[str, Any]) -> str:
    start = _safe_str(e.get("start"))
    end = _safe_str(e.get("end"))
    et = _safe_str(e.get("event_type"))
    sev = _safe_str(e.get("severity"))
    cap = _shorten(e.get("caption", ""), 220)
    return f"{start}-{end} [{et}/{sev}] {cap}"


def _find_video_path_for_clip(clip: str) -> str | None:
    """
    Attempt to locate a video under data/videos/** matching the clip filename.
    Returns a workspace-relative posix path suitable for markdown links, or None.
    """
    # First try a small set of "known good" folders to avoid linking to older/blurrier re-encodes.
    preferred_dirs = [
        Path("data/videos/meva_examples_selected10"),
        Path("data/videos/meva_school_selected_30s_copy"),
        Path("data/videos/meva_school_selected_30s"),
    ]
    for d in preferred_dirs:
        p = d / clip
        if p.is_file():
            return p.as_posix()

    # Fallback: search anywhere under data/videos/**.
    pattern = str(Path("data") / "videos" / "**" / clip)
    matches = [Path(p) for p in glob.glob(pattern, recursive=True)]
    matches = [m for m in matches if m.is_file()]
    if not matches:
        return None
    # Prefer stable, deterministic ordering.
    best = sorted(matches, key=lambda p: (p.as_posix().lower(), p.as_posix()))[0]
    return best.as_posix()


def build_report(results_dir: Path) -> str:
    rows: Dict[str, Dict[str, Any]] = {}
    missing_by_clip: Dict[str, List[str]] = {}

    json_files = sorted(results_dir.glob("*.json"))
    for p in json_files:
        clip, mode = _clip_key_from_filename(p.name)
        if mode not in MODES:
            continue
        rows.setdefault(clip, {})[mode] = _read_json(p)

    clips = sorted(rows.keys())
    for clip in clips:
        missing = [m for m in MODES if m not in rows[clip]]
        if missing:
            missing_by_clip[clip] = missing

    # Aggregates
    n_clips = len(clips)
    safety_counts: Dict[str, int] = {"COMPLIANT": 0, "PARTIAL": 0, "NON-COMPLIANT": 0, "": 0}
    security_counts: Dict[str, int] = {"CLEAR": 0, "ALERT": 0, "BREACH": 0, "": 0}
    # Load prompt expects: SAFE | WARNING | CRITICAL (but we also tolerate unknowns).
    load_counts: Dict[str, int] = {"SAFE": 0, "WARNING": 0, "CRITICAL": 0, "": 0}
    timeline_event_total = 0
    timeline_nonempty = 0

    for clip in clips:
        load = rows[clip].get("load") or {}
        safety = rows[clip].get("safety") or {}
        security = rows[clip].get("security") or {}
        timeline = rows[clip].get("timeline")

        lr = _safe_str(load.get("overall_risk"))
        load_counts[lr] = load_counts.get(lr, 0) + 1
        safety_counts[_safe_str(safety.get("overall_compliance"))] = safety_counts.get(
            _safe_str(safety.get("overall_compliance")), 0
        ) + 1
        security_counts[_safe_str(security.get("overall_security"))] = security_counts.get(
            _safe_str(security.get("overall_security")), 0
        ) + 1

        if isinstance(timeline, list):
            timeline_event_total += len(timeline)
            if len(timeline) > 0:
                timeline_nonempty += 1

    now = _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    out: List[str] = []
    out.append("# Warehouse Ops Center - Test Report")
    out.append("")
    out.append(f"Generated: `{now}`")
    out.append(f"Results dir: `{results_dir.as_posix()}`")
    out.append("")

    out.append("## Summary")
    out.append("")
    out.append(f"- Clips: `{n_clips}`")
    out.append(f"- Timeline events: `{timeline_event_total}` (non-empty clips: `{timeline_nonempty}`)")
    load_summary_parts = [
        f"SAFE={load_counts.get('SAFE',0)}",
        f"WARNING={load_counts.get('WARNING',0)}",
        f"CRITICAL={load_counts.get('CRITICAL',0)}",
    ]
    extra_load = sorted(k for k in load_counts.keys() if k not in ("", "SAFE", "WARNING", "CRITICAL") and load_counts.get(k, 0) > 0)
    for k in extra_load:
        load_summary_parts.append(f"{k}={load_counts.get(k,0)}")
    out.append(f"- Load overall_risk counts: `{', '.join(load_summary_parts)}`")
    out.append(
        f"- Safety overall_compliance counts: `COMPLIANT={safety_counts.get('COMPLIANT',0)}`, `PARTIAL={safety_counts.get('PARTIAL',0)}`, `NON-COMPLIANT={safety_counts.get('NON-COMPLIANT',0)}`"
    )
    out.append(
        f"- Security overall_security counts: `CLEAR={security_counts.get('CLEAR',0)}`, `ALERT={security_counts.get('ALERT',0)}`, `BREACH={security_counts.get('BREACH',0)}`"
    )
    if missing_by_clip:
        out.append(f"- Missing outputs: `{len(missing_by_clip)}` clip(s)")
    out.append("")

    out.append("## Clip Matrix")
    out.append("")
    out.append("| Clip | Load | Safety | Security | Timeline events | Notes |")
    out.append("|---|---:|---:|---:|---:|---|")
    for clip in clips:
        load = rows[clip].get("load") or {}
        safety = rows[clip].get("safety") or {}
        security = rows[clip].get("security") or {}
        timeline = rows[clip].get("timeline")

        lr = _md_escape(_safe_str(load.get("overall_risk")))
        sc = _md_escape(_safe_str(safety.get("overall_compliance")))
        sec = _md_escape(_safe_str(security.get("overall_security")))
        te = len(timeline) if isinstance(timeline, list) else ""

        video_path = _find_video_path_for_clip(clip)
        clip_cell = f"`{clip}`"
        if video_path:
            clip_cell = f"[`{clip}`]({video_path})"

        notes_parts: List[str] = []
        if clip in missing_by_clip:
            notes_parts.append("missing: " + ", ".join(missing_by_clip[clip]))
        if isinstance(timeline, list) and len(timeline) == 0:
            notes_parts.append("timeline empty")
        notes = _md_escape("; ".join(notes_parts))
        out.append(f"| {clip_cell} | {lr} | {sc} | {sec} | {te} | {notes} |")
    out.append("")

    out.append("## Per-Clip Details")
    out.append("")

    for clip in clips:
        out.append(f"### {clip}")
        out.append("")

        video_path = _find_video_path_for_clip(clip)
        if video_path:
            out.append(f"- video: [`{video_path}`]({video_path})")
        else:
            out.append("- video: (not found under `data/videos/**`)")

        # Link to local JSON artifacts for quick inspection.
        # These are workspace-relative links (may be gitignored, but clickable locally).
        json_links: List[str] = []
        for mode in MODES:
            p = (results_dir / f"{clip}__{mode}.json").as_posix()
            if (results_dir / f"{clip}__{mode}.json").exists():
                json_links.append(f"[`{mode}`]({p})")
        if json_links:
            out.append(f"- outputs: " + " ".join(json_links))
        out.append("")

        load = rows[clip].get("load")
        if isinstance(load, dict):
            out.append("**Load/Physics**")
            out.append("")
            out.append(f"- overall_risk: `{_safe_str(load.get('overall_risk'))}`")
            rr = _safe_str(load.get("risk_reasoning"))
            if rr:
                out.append(f"- risk_reasoning: {_md_escape(_shorten(rr, 400))}")
            loads = load.get("loads")
            if isinstance(loads, list) and loads:
                out.append(f"- loads: `{len(loads)}`")
            else:
                out.append("- loads: `0`")
            out.append("")

        safety = rows[clip].get("safety")
        if isinstance(safety, dict):
            out.append("**PPE/Safety**")
            out.append("")
            out.append(f"- overall_compliance: `{_safe_str(safety.get('overall_compliance'))}`")
            summ = _safe_str(safety.get("summary"))
            if summ:
                out.append(f"- summary: {_md_escape(_shorten(summ, 420))}")
            workers = safety.get("workers")
            if isinstance(workers, list) and workers:
                noncompliant = [w for w in workers if w.get("compliant") is False]
                out.append(f"- workers: `{len(workers)}` (non-compliant: `{len(noncompliant)}`)")
                # Show up to 5 violations
                shown = 0
                for w in noncompliant[:5]:
                    wid = _safe_str(w.get("worker_id"))
                    viol = _safe_str(w.get("violation_description"))
                    out.append(f"- violation: `{wid}`: {_md_escape(_shorten(viol, 260))}")
                    shown += 1
                if len(noncompliant) > shown:
                    out.append(f"- violation: ... plus `{len(noncompliant) - shown}` more")
            else:
                out.append("- workers: `0`")
            out.append("")

        security = rows[clip].get("security")
        if isinstance(security, dict):
            out.append("**Security/Access**")
            out.append("")
            out.append(f"- overall_security: `{_safe_str(security.get('overall_security'))}`")
            ra = _safe_str(security.get("recommended_action"))
            if ra:
                out.append(f"- recommended_action: {_md_escape(_shorten(ra, 420))}")
            persons = security.get("persons")
            if isinstance(persons, list) and persons:
                out.append(f"- persons: `{len(persons)}`")
                suspicious = [
                    p
                    for p in persons
                    if _safe_str(p.get("authorization_assessment")).lower() in ("suspicious", "unauthorized")
                ]
                if suspicious:
                    out.append(f"- flagged_persons: `{len(suspicious)}`")
                for p in persons[:5]:
                    pid = _safe_str(p.get("person_id"))
                    aa = _safe_str(p.get("authorization_assessment"))
                    reason = _safe_str(p.get("reasoning"))
                    out.append(f"- person: `{pid}` `{aa}`: {_md_escape(_shorten(reason, 240))}")
                if len(persons) > 5:
                    out.append(f"- person: ... plus `{len(persons) - 5}` more")
            else:
                out.append("- persons: `0`")
            out.append("")

        timeline = rows[clip].get("timeline")
        if isinstance(timeline, list):
            out.append("**Incident Timeline**")
            out.append("")
            out.append(f"- events: `{len(timeline)}`")
            for e in timeline[:10]:
                if isinstance(e, dict):
                    out.append(f"- event: {_md_escape(_fmt_event_line(e))}")
            if len(timeline) > 10:
                out.append(f"- event: ... plus `{len(timeline) - 10}` more")
            out.append("")

        if clip in missing_by_clip:
            out.append("**Missing Outputs**")
            out.append("")
            out.append(f"- missing: `{', '.join(missing_by_clip[clip])}`")
            out.append("")

    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--results-dir", default="outputs/auto/per_stream", help="Directory containing per-stream *.json outputs")
    ap.add_argument("--out", default="reports/test_report.md", help="Where to write the markdown report")
    args = ap.parse_args()

    results_dir = Path(args.results_dir)
    if not results_dir.exists():
        raise SystemExit(f"results dir not found: {results_dir}")

    md = build_report(results_dir)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")
    print(out_path.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
