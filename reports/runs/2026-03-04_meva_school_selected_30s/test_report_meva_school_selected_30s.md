# Warehouse Ops Center - Test Report

Generated: `2026-03-04 02:24:35`
Results dir: `outputs/auto/per_stream`

## Summary

- Clips: `5`
- Timeline events: `4` (non-empty clips: `4`)
- Load overall_risk counts: `SAFE=5, WARNING=0, CRITICAL=0`
- Safety overall_compliance counts: `COMPLIANT=4`, `PARTIAL=0`, `NON-COMPLIANT=1`
- Security overall_security counts: `CLEAR=5`, `ALERT=0`, `BREACH=0`

## Clip Matrix

| Clip | Load | Safety | Security | Timeline events | Notes |
|---|---:|---:|---:|---:|---|
| `2018-03-07.16-55-06.17-00-06.school.G336.r13_trim30s.mp4` | SAFE | COMPLIANT | CLEAR | 1 |  |
| `2018-03-07.16-55-06.17-00-06.school.G339.r13_trim30s.mp4` | SAFE | NON-COMPLIANT | CLEAR | 1 |  |
| `2018-03-07.16-55-06.17-00-06.school.G424.r13_trim30s.mp4` | SAFE | COMPLIANT | CLEAR | 0 | timeline empty |
| `2018-03-07.17-00-06.17-05-06.school.G339.r13_trim30s.mp4` | SAFE | COMPLIANT | CLEAR | 1 |  |
| `2018-03-07.17-00-06.17-05-06.school.G424.r13_trim30s.mp4` | SAFE | COMPLIANT | CLEAR | 1 |  |

## Per-Clip Details

### 2018-03-07.16-55-06.17-00-06.school.G336.r13_trim30s.mp4

**Load/Physics**

- overall_risk: `SAFE`
- risk_reasoning: The video depicts a quiet suburban area with no visible loads, pallets, or lifting equipment. Pedestrians are walking at a normal pace, and there are no signs of unsafe handling, unstable stacking, or equipment exceeding weight limits. The scene appears calm and free of immediate safety hazards.
- loads: `0`

**PPE/Safety**

- overall_compliance: `COMPLIANT`
- summary: No workers visible.
- workers: `0`

**Security/Access**

- overall_security: `CLEAR`
- recommended_action: No assessment was possible as no clear descriptions of individuals, their attire, or specific actions were provided to evaluate authorization or suspicious behavior.
- persons: `0`

**Incident Timeline**

- events: `1`
- event: 00:00.50-00:27.50 [improper_handling/low] Pedestrians walk leisurely along the sidewalk, maintaining a safe distance from the road and other individuals. No sudden movements or near-misses are observed.

### 2018-03-07.16-55-06.17-00-06.school.G339.r13_trim30s.mp4

**Load/Physics**

- overall_risk: `SAFE`
- risk_reasoning: The video does not show visible loads, pallets, or lifting equipment being handled. Workers are engaged in manual tasks (e.g., shoveling, raking) with no indication of unsafe stacking or exceeding equipment limits. Safety measures like traffic cones and appropriate footwear are present, and the scene appears orderly with no immediate hazards.
- loads: `0`

**PPE/Safety**

- overall_compliance: `NON-COMPLIANT`
- summary: Four workers are wearing hard hats and high-visibility vests, which are correct. However, they are not wearing safety gloves, which is required for handling soil and tools. This omission is a compliance gap.
- workers: `4` (non-compliant: `4`)
- violation: `Worker 1`: Safety gloves are not observed while handling soil or tools.
- violation: `Worker 2`: Safety gloves are not observed while handling soil or tools.
- violation: `Worker 3`: Safety gloves are not observed while handling soil or tools.
- violation: `Worker 4`: Safety gloves are not observed while handling soil or tools.

**Security/Access**

- overall_security: `CLEAR`
- recommended_action: No assessment was possible as no individuals were clearly visible for analysis.
- persons: `0`

**Incident Timeline**

- events: `1`
- event: 00:00.50-00:27.50 [near_miss/high] A pedestrian is walking very close to the construction site, posing a potential risk of injury if construction materials or equipment are mishandled or if a vehicle enters the area unexpectedly. The proximity of the p...

### 2018-03-07.16-55-06.17-00-06.school.G424.r13_trim30s.mp4

**Load/Physics**

- overall_risk: `SAFE`
- risk_reasoning: No active load handling operations are observed. The orange crane/lift and other equipment are stationary, and no loads or pallets are visible in motion or being manipulated. The scene depicts a static parking lot environment with no immediate safety hazards related to load handling.
- loads: `0`

**PPE/Safety**

- overall_compliance: `COMPLIANT`
- summary: No workers visible.
- workers: `0`

**Security/Access**

- overall_security: `CLEAR`
- recommended_action: No assessment was possible as no individuals were clearly visible for analysis.
- persons: `0`

**Incident Timeline**

- events: `0`

### 2018-03-07.17-00-06.17-05-06.school.G339.r13_trim30s.mp4

**Load/Physics**

- overall_risk: `SAFE`
- risk_reasoning: The scene depicts manual labor with no visible loads, pallets, or lifting equipment. Workers are using shovels and tools within safe manual handling limits, and the area is cordoned off with traffic cones. There is no indication of unstable stacking or equipment exceeding weight limits. Pedestrians are on a separate sidewalk, and the blocked road suggests controlled access, contributing to a sa...
- loads: `0`

**PPE/Safety**

- overall_compliance: `COMPLIANT`
- summary: All workers are wearing appropriate PPE for their tasks.
- workers: `3` (non-compliant: `0`)

**Security/Access**

- overall_security: `CLEAR`
- recommended_action: No assessment was possible as no individuals were clearly visible for analysis.
- persons: `0`

**Incident Timeline**

- events: `1`
- event: 00:00.50-00:27.50 [improper_handling/low] Construction workers wearing bright yellow safety vests and hard hats are digging a trench on a road near a building. The trench is surrounded by orange traffic cones to mark the work area. A white pickup truck is par...

### 2018-03-07.17-00-06.17-05-06.school.G424.r13_trim30s.mp4

**Load/Physics**

- overall_risk: `SAFE`
- risk_reasoning: No visible loads, pallets, or active lifting equipment are present in the scene. The red pickup truck has an attachment, but it is not engaged in handling any objects. The people are walking casually without interacting with machinery or loads, and there are no signs of unstable stacking or equipment limits being exceeded.
- loads: `0`

**PPE/Safety**

- overall_compliance: `COMPLIANT`
- summary: No workers visible.
- workers: `0`

**Security/Access**

- overall_security: `CLEAR`
- recommended_action: No assessment possible as no individuals are clearly visible for analysis.
- persons: `0`

**Incident Timeline**

- events: `1`
- event: 00:00.50-00:27.50 [improper_handling/low] A group of individuals is walking in a coordinated manner across the parking lot, with some gesturing or pointing while maintaining a steady pace. The scene remains calm and orderly throughout the video, with no immed...
