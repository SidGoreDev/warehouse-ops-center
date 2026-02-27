from __future__ import annotations

from .common import with_reasoning_suffix


def build_prompt() -> str:
    prompt = """Analyze this warehouse/industrial scene for load handling safety.

1. Locate bounding boxes for all loads, pallets, and lifting equipment.
2. Estimate the weight of each load based on visual cues (size, material, packaging type, pallet configuration).
3. Determine if any load appears to exceed safe handling limits for the equipment shown.
4. Check stacking stability — are loads stacked in a way that could topple?

Return results as JSON with the following structure:
{
  "loads": [
    {
      "description": "string",
      "box_2d": [x1, y1, x2, y2],
      "estimated_weight_kg": number,
      "estimated_weight_reasoning": "string",
      "stability_assessment": "stable | unstable | marginal",
      "equipment_limit_exceeded": boolean
    }
  ],
  "overall_risk": "SAFE | WARNING | CRITICAL",
  "risk_reasoning": "string"
}

If you cannot identify any loads or lifting equipment, return:
- "loads": []
- "overall_risk": "SAFE"
- and explain why in "risk_reasoning".

Return ONLY valid JSON after the </think> tag. Do not use markdown fences."""
    return with_reasoning_suffix(prompt)
