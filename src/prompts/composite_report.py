from __future__ import annotations

import json

from .common import with_reasoning_suffix


def build_prompt(*, load_json: dict, safety_json: dict, security_json: dict, timeline_json: list) -> str:
    prompt = f"""You have analyzed a warehouse video segment. Here are the results from four analysis passes:

LOAD ANALYSIS: {json.dumps(load_json, ensure_ascii=False)}
PPE AUDIT: {json.dumps(safety_json, ensure_ascii=False)}
SECURITY SCAN: {json.dumps(security_json, ensure_ascii=False)}
INCIDENT TIMELINE: {json.dumps(timeline_json, ensure_ascii=False)}

Synthesize these into a single shift safety report. Include:
1. Executive summary (2-3 sentences)
2. Critical findings requiring immediate action
3. Overall safety score (0-100)
4. Top 3 recommendations

Return as JSON:
{{
  "executive_summary": "string",
  "safety_score": number,
  "critical_findings": ["list"],
  "recommendations": ["list"],
  "shift_status": "NORMAL | ELEVATED_RISK | UNSAFE"
}}

If any upstream section is empty, still produce a report and mention the limitation in "executive_summary".

Return ONLY valid JSON after the </think> tag. Do not use markdown fences."""
    return with_reasoning_suffix(prompt)
