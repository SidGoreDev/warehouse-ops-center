# Ground Truth Labeling (Offline)

This project evaluates CR2 outputs against hand-labeled JSON ground truth.

## Directory Layout

Ground truth files live under:

`data/ground_truth/<video_filename>/<mode>.json`

Examples:
- `data/ground_truth/forklift_01.mp4/load.json`
- `data/ground_truth/forklift_01.mp4/timeline.json`

`data/` is gitignored. Commit only small templates or docs, not raw videos.

## Mode Schemas (Templates)

### `load.json`

```json
{
  "loads": [
    {
      "description": "string",
      "box_2d": [0, 0, 0, 0],
      "estimated_weight_kg": 0,
      "estimated_weight_reasoning": "string",
      "stability_assessment": "stable",
      "equipment_limit_exceeded": false
    }
  ],
  "overall_risk": "SAFE",
  "risk_reasoning": "string"
}
```

### `safety.json`

```json
{
  "workers": [
    {
      "worker_id": "Worker 1",
      "observed_ppe": [],
      "required_ppe": [],
      "compliant": true,
      "violation_description": null
    }
  ],
  "overall_compliance": "COMPLIANT",
  "summary": "string"
}
```

### `security.json`

```json
{
  "persons": [
    {
      "person_id": "Person 1",
      "authorization_assessment": "authorized",
      "reasoning": "string",
      "indicators": []
    }
  ],
  "overall_security": "CLEAR",
  "recommended_action": "string"
}
```

### `timeline.json`

```json
[
  {
    "start": "00:00.00",
    "end": "00:00.00",
    "caption": "string",
    "event_type": "near_miss",
    "severity": "low",
    "recommended_action": "string"
  }
]
```

## Labeling Tips

- Use `mm:ss.ff` timestamps and keep them consistent (2-digit seconds; decimals in hundredths is fine).
- Prefer fewer, higher-signal events over exhaustive micro-events.
- For PPE and security, keep stable IDs (`Worker 1`, `Person 1`) to simplify matching.
