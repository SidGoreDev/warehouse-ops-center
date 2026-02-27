from __future__ import annotations

from typing import Dict, List, Tuple


def candidate_pairs(
    per_stream_events: Dict[str, List[dict]],
    *,
    max_dt_seconds: float = 5.0,
) -> List[Tuple[Tuple[str, dict], Tuple[str, dict]]]:
    """
    Tier 2 stub: produce candidate cross-stream event pairs before CR2 reasoning.
    A full implementation should use time windows + zone adjacency + entity overlap.
    """
    _ = max_dt_seconds
    sids = list(per_stream_events.keys())
    pairs: List[Tuple[Tuple[str, dict], Tuple[str, dict]]] = []
    for i in range(len(sids)):
        for j in range(i + 1, len(sids)):
            for e1 in per_stream_events[sids[i]]:
                for e2 in per_stream_events[sids[j]]:
                    pairs.append(((sids[i], e1), (sids[j], e2)))
    return pairs
