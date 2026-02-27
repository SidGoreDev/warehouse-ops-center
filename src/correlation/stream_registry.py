from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Stream:
    stream_id: str
    label: str
    zone: str
    video_path: str
    time_offset_seconds: float = 0.0
    analysis_modes: Optional[List[str]] = None


@dataclass(frozen=True)
class FacilityLayout:
    zone_adjacency: Dict[str, List[str]]


@dataclass(frozen=True)
class StreamRegistry:
    streams: List[Stream]
    facility_layout: FacilityLayout

    @staticmethod
    def from_json(d: dict) -> "StreamRegistry":
        layout = FacilityLayout(zone_adjacency=d.get("facility_layout", {}).get("zone_adjacency", {}))
        streams = []
        for s in d.get("streams", []):
            streams.append(
                Stream(
                    stream_id=s["stream_id"],
                    label=s.get("label", s["stream_id"]),
                    zone=s.get("zone", "unknown"),
                    video_path=s["video_path"],
                    time_offset_seconds=float(s.get("time_offset_seconds", 0.0)),
                    analysis_modes=s.get("analysis_modes"),
                )
            )
        return StreamRegistry(streams=streams, facility_layout=layout)
