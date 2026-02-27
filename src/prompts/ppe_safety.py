from __future__ import annotations

from .common import with_reasoning_suffix


def build_prompt() -> str:
    prompt = """You are a warehouse safety auditor. Analyze this video for PPE (Personal Protective Equipment) compliance.

For each worker visible in the video:
1. Identify what safety equipment they are wearing (hard hat, hi-vis vest, safety glasses, steel-toe boots, gloves).
2. Identify what safety equipment they SHOULD be wearing based on the activities observed.
3. Flag any compliance gaps.

Return results as JSON:
{
  "workers": [
    {
      "worker_id": "Worker N",
      "observed_ppe": ["list of equipment"],
      "required_ppe": ["list based on activity"],
      "compliant": boolean,
      "violation_description": "string or null"
    }
  ],
  "overall_compliance": "COMPLIANT | PARTIAL | NON-COMPLIANT",
  "summary": "string"
}

Return ONLY valid JSON after the </think> tag. Do not use markdown fences."""
    return with_reasoning_suffix(prompt)
