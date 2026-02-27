from __future__ import annotations

from .common import with_reasoning_suffix


def build_prompt() -> str:
    prompt = """Analyze this warehouse video and generate a timestamped incident report of all safety-relevant events.

Safety-relevant events include:
- Near-misses (forklift near pedestrian, falling objects narrowly avoided)
- PPE violations (removal of equipment, entering zone without required gear)
- Improper material handling (overloaded pallets, unsafe stacking, dragging loads)
- Ergonomic risks (improper lifting posture, repetitive strain movements)
- Equipment misuse (speeding forklifts, blocked emergency exits)

Provide timestamps in mm:ss.ff format. Return as JSON (an array):
[
  {
    "start": "mm:ss.ff",
    "end": "mm:ss.ff",
    "caption": "string",
    "event_type": "near_miss | ppe_violation | improper_handling | ergonomic_risk | equipment_misuse",
    "severity": "low | medium | high | critical",
    "recommended_action": "string"
  }
]

Return ONLY valid JSON after the </think> tag. Do not use markdown fences."""
    return with_reasoning_suffix(prompt)
