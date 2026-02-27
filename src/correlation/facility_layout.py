from __future__ import annotations

from typing import Dict, List


def are_zones_adjacent(zone_adjacency: Dict[str, List[str]], a: str, b: str) -> bool:
    if a == b:
        return True
    return b in zone_adjacency.get(a, []) or a in zone_adjacency.get(b, [])
