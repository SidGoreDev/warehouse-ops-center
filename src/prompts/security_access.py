from __future__ import annotations

from .common import with_reasoning_suffix


def build_prompt() -> str:
    prompt = """Analyze this warehouse video for potential unauthorized access or suspicious behavior.

Consider:
1. Is each person's attire consistent with authorized warehouse personnel (uniforms, badges, PPE)?
2. Are their movements consistent with normal operations or do they appear lost, hurried, or evasive?
3. Are they accessing areas that appear restricted (marked zones, locked areas, offices)?
4. Is their handling of materials appropriate (careful/trained vs. rough/unfamiliar)?

Return results as JSON:
{
  "persons": [
    {
      "person_id": "Person N",
      "authorization_assessment": "authorized | suspicious | unauthorized",
      "reasoning": "string",
      "indicators": ["list of behavioral/visual indicators"]
    }
  ],
  "overall_security": "CLEAR | ALERT | BREACH",
  "recommended_action": "string"
}

Return ONLY valid JSON after the </think> tag. Do not use markdown fences."""
    return with_reasoning_suffix(prompt)
