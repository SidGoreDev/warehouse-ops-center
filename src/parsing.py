from __future__ import annotations

import json
import re
from typing import Any, Optional, Tuple


THINK_RE = re.compile(r"<think>\s*(?P<think>.*?)\s*</think>", re.DOTALL | re.IGNORECASE)


def extract_think(text: str) -> Optional[str]:
    m = THINK_RE.search(text)
    if not m:
        return None
    return m.group("think").strip()


def _strip_code_fences(s: str) -> str:
    s = s.strip()
    if s.startswith("```"):
        # Remove first fence line and last fence if present.
        lines = s.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return s


def _find_json_start(text: str) -> int:
    # Prefer JSON after </think> if present.
    lower = text.lower()
    think_end = lower.find("</think>")
    start_search = think_end + len("</think>") if think_end != -1 else 0
    for i in range(start_search, len(text)):
        if text[i] in "{[":
            return i
    # Fallback: scan from beginning
    for i, ch in enumerate(text):
        if ch in "{[":
            return i
    raise ValueError("No JSON object/array start found in model output.")


def _extract_balanced(text: str, start: int) -> str:
    opening = text[start]
    closing = "}" if opening == "{" else "]"
    depth = 0
    in_str = False
    esc = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        else:
            if ch == '"':
                in_str = True
                continue
            if ch == opening:
                depth += 1
            elif ch == closing:
                depth -= 1
                if depth == 0:
                    return text[start : i + 1]
    raise ValueError("Unbalanced JSON in model output.")


def extract_json_text(text: str) -> str:
    s = _strip_code_fences(text)
    start = _find_json_start(s)
    return _extract_balanced(s, start).strip()


def _common_repairs(s: str) -> str:
    # Keep repairs conservative; only fix very common minor issues.
    s = s.strip()
    # Convert smart quotes to straight quotes.
    s = s.replace("\u201c", '"').replace("\u201d", '"').replace("\u2018", "'").replace("\u2019", "'")
    # Remove trailing commas before } or ]
    s = re.sub(r",\s*([}\]])", r"\1", s)
    return s


def json_loads_with_repairs(s: str) -> Any:
    last_err: Optional[Exception] = None
    attempt = s
    for _ in range(3):
        try:
            return json.loads(attempt)
        except Exception as e:  # noqa: BLE001
            last_err = e
            attempt = _common_repairs(attempt)
    raise ValueError(f"Failed to parse JSON after repairs: {last_err}") from last_err


def parse_model_output(text: str) -> Tuple[Optional[str], Any, str]:
    """
    Returns: (think_text, parsed_json, json_text)
    """
    think = extract_think(text)
    json_text = extract_json_text(text)
    parsed = json_loads_with_repairs(json_text)
    return think, parsed, json_text


def parse_mmssff_to_seconds(ts: str) -> float:
    # mm:ss.ff
    m = re.fullmatch(r"(?P<mm>\d{1,2}):(?P<ss>\d{2})\.(?P<ff>\d{1,3})", ts.strip())
    if not m:
        raise ValueError(f"Bad timestamp format (expected mm:ss.ff): {ts!r}")
    mm = int(m.group("mm"))
    ss = int(m.group("ss"))
    ff = int(m.group("ff"))
    # Treat ff as centiseconds if 2 digits, milliseconds if 3 digits, tenths if 1 digit.
    denom = 10 if len(m.group("ff")) == 1 else 100 if len(m.group("ff")) == 2 else 1000
    return mm * 60.0 + ss + ff / denom
