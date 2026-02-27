from __future__ import annotations

from typing import Dict, List


def apply_time_offset(events: List[dict], offset_seconds: float) -> List[dict]:
    """
    Tier 2 stub: shift timeline event timestamps by a known per-camera offset.
    A full implementation will parse mm:ss.ff, add offset, and reformat.
    """
    _ = offset_seconds
    return events


def align_streams(per_stream: Dict[str, List[dict]], offsets: Dict[str, float]) -> Dict[str, List[dict]]:
    aligned: Dict[str, List[dict]] = {}
    for sid, events in per_stream.items():
        aligned[sid] = apply_time_offset(events, offsets.get(sid, 0.0))
    return aligned
