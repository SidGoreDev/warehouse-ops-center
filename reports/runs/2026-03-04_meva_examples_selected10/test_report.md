# Warehouse Ops Center - Test Report

Generated: `2026-03-04 02:33:09`
Results dir: `outputs/runs/2026-03-04_meva_examples_selected10/per_stream`

## Summary

- Clips: `10`
- Timeline events: `6` (non-empty clips: `6`)
- Load overall_risk counts: `SAFE=8, WARNING=2, CRITICAL=0`
- Safety overall_compliance counts: `COMPLIANT=8`, `PARTIAL=1`, `NON-COMPLIANT=1`
- Security overall_security counts: `CLEAR=9`, `ALERT=1`, `BREACH=0`

## Clip Matrix

| Clip | Load | Safety | Security | Timeline events | Notes |
|---|---:|---:|---:|---:|---|
| [`ex027-heavy-carry.mp4`](data/videos/meva_examples_selected10/ex027-heavy-carry.mp4) | SAFE | COMPLIANT | CLEAR | 1 |  |
| [`ex028-heavy-carry.mp4`](data/videos/meva_examples_selected10/ex028-heavy-carry.mp4) | SAFE | PARTIAL | CLEAR | 1 |  |
| [`ex029-heavy-carry.mp4`](data/videos/meva_examples_selected10/ex029-heavy-carry.mp4) | WARNING | COMPLIANT | CLEAR | 1 |  |
| [`ex033-load-vehicle.mp4`](data/videos/meva_examples_selected10/ex033-load-vehicle.mp4) | WARNING | COMPLIANT | ALERT | 1 |  |
| [`ex034-load-vehicle.mp4`](data/videos/meva_examples_selected10/ex034-load-vehicle.mp4) | SAFE | COMPLIANT | CLEAR | 0 | timeline empty |
| [`ex035-load-vehicle.mp4`](data/videos/meva_examples_selected10/ex035-load-vehicle.mp4) | SAFE | COMPLIANT | CLEAR | 0 | timeline empty |
| [`ex085-theft.mp4`](data/videos/meva_examples_selected10/ex085-theft.mp4) | SAFE | COMPLIANT | CLEAR | 1 |  |
| [`ex086-unload-vehicle.mp4`](data/videos/meva_examples_selected10/ex086-unload-vehicle.mp4) | SAFE | COMPLIANT | CLEAR | 0 | timeline empty |
| [`ex087-unload-vehicle.mp4`](data/videos/meva_examples_selected10/ex087-unload-vehicle.mp4) | SAFE | NON-COMPLIANT | CLEAR | 1 |  |
| [`ex088-unload-vehicle.mp4`](data/videos/meva_examples_selected10/ex088-unload-vehicle.mp4) | SAFE | COMPLIANT | CLEAR | 0 | timeline empty |

## Per-Clip Details

### ex027-heavy-carry.mp4

- video: [`data/videos/meva_examples_selected10/ex027-heavy-carry.mp4`](data/videos/meva_examples_selected10/ex027-heavy-carry.mp4)
- outputs: [`load`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex027-heavy-carry.mp4__load.json) [`safety`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex027-heavy-carry.mp4__safety.json) [`security`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex027-heavy-carry.mp4__security.json) [`timeline`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex027-heavy-carry.mp4__timeline.json)

**Load/Physics**

- overall_risk: `SAFE`
- risk_reasoning: No loads, pallets, or lifting equipment are visible in the scene, and there are no unsafe practices related to load handling observed.
- loads: `0`

**PPE/Safety**

- overall_compliance: `COMPLIANT`
- summary: No workers visible.
- workers: `0`

**Security/Access**

- overall_security: `CLEAR`
- recommended_action: No assessment possible as no human activity is visible.
- persons: `0`

**Incident Timeline**

- events: `1`
- event: 00:02.00-00:29.00 [improper_handling/medium] Two individuals are seen carrying a large, rectangular object across the parking lot from left to right. They move steadily but must navigate around pedestrians and avoid the bus stop shelter to prevent collisions or ...

### ex028-heavy-carry.mp4

- video: [`data/videos/meva_examples_selected10/ex028-heavy-carry.mp4`](data/videos/meva_examples_selected10/ex028-heavy-carry.mp4)
- outputs: [`load`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex028-heavy-carry.mp4__load.json) [`safety`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex028-heavy-carry.mp4__safety.json) [`security`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex028-heavy-carry.mp4__security.json) [`timeline`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex028-heavy-carry.mp4__timeline.json)

**Load/Physics**

- overall_risk: `SAFE`
- risk_reasoning: The video does not show any active load handling, lifting equipment, or unsafe stacking of objects. All visible items (e.g., cooler, table, bag) are stationary and appear stable, with no signs of tipping or exceeding weight limits. The scene depicts a normal pedestrian environment with no immediate safety hazards.
- loads: `0`

**PPE/Safety**

- overall_compliance: `PARTIAL`
- summary: Worker Heavy Carry_1 is wearing a hard hat but lacks gloves for safe heavy lifting. Other workers are not in a hazardous environment and do not require PPE.
- workers: `1` (non-compliant: `1`)
- violation: `Heavy Carry_1`: Worker is missing gloves while carrying a heavy load, which is required for hand protection.

**Security/Access**

- overall_security: `CLEAR`
- recommended_action: No assessment possible as no individuals are visible.
- persons: `0`

**Incident Timeline**

- events: `1`
- event: 00:00.20-00:14.60 [improper_handling/medium] A person in a red jacket is seen carrying a large object along a paved path in a park or campus area. They are moving steadily while others walk nearby, some stopping to observe. The person appears to be handling the ...

### ex029-heavy-carry.mp4

- video: [`data/videos/meva_examples_selected10/ex029-heavy-carry.mp4`](data/videos/meva_examples_selected10/ex029-heavy-carry.mp4)
- outputs: [`load`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex029-heavy-carry.mp4__load.json) [`safety`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex029-heavy-carry.mp4__safety.json) [`security`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex029-heavy-carry.mp4__security.json) [`timeline`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex029-heavy-carry.mp4__timeline.json)

**Load/Physics**

- overall_risk: `WARNING`
- risk_reasoning: The individual carrying the heavy object is navigating a crowded hallway, increasing the risk of collisions or loss of balance. The object's size and weight may exceed ergonomic limits for safe manual handling, especially in a dynamic environment with multiple people moving around. While no lifting equipment is present, the combination of a heavy load and a busy setting creates a hazardous scen...
- loads: `1`

**PPE/Safety**

- overall_compliance: `COMPLIANT`
- summary: No workers visible.
- workers: `0`

**Security/Access**

- overall_security: `CLEAR`
- persons: `1`
- person: `Heavy Carry:1` `authorized`: The individual is using a labeled "Heavy Carry" cart in a school hallway, which aligns with expected behavior for transporting materials. No suspicious or unauthorized actions are observed; the movement is steady and purposeful, consiste...

**Incident Timeline**

- events: `1`
- event: 00:00.000-00:35.100 [/] A person labeled "Heavy Carry:1" is pushing a wheeled cart with a heavy object through a school hallway, navigating past stationary and moving individuals while maintaining a steady pace. The cart operator should slow...

### ex033-load-vehicle.mp4

- video: [`data/videos/meva_examples_selected10/ex033-load-vehicle.mp4`](data/videos/meva_examples_selected10/ex033-load-vehicle.mp4)
- outputs: [`load`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex033-load-vehicle.mp4__load.json) [`safety`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex033-load-vehicle.mp4__safety.json) [`security`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex033-load-vehicle.mp4__security.json) [`timeline`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex033-load-vehicle.mp4__timeline.json)

**Load/Physics**

- overall_risk: `WARNING`
- risk_reasoning: The "Load_Vehicle_3" is moving slowly in a parking lot area where pedestrians are present, posing a potential collision risk if the vehicle operator fails to yield or if pedestrians do not notice the vehicle. No visible loads are shown, but the vehicle's operation in a pedestrian zone without clear separation of traffic paths increases safety concerns.
- loads: `0`

**PPE/Safety**

- overall_compliance: `COMPLIANT`
- summary: No workers visible.
- workers: `0`

**Security/Access**

- overall_security: `ALERT`
- recommended_action: Monitor individuals in casual attire near the warehouse perimeter and verify their authorization status through security checks or communication with the facility.
- persons: `1`
- flagged_persons: `1`
- person: `Person N` `unauthorized`: Individuals are seen walking on a sidewalk and near a parking lot but are not wearing uniforms, badges, or PPE typically associated with authorized warehouse personnel. Their presence in the area without visible authorization indicators ...

**Incident Timeline**

- events: `1`
- event: 00:00.10-00:08.10 [near_miss/critical] A black car drives along the road while passing close to a pedestrian walking on the sidewalk, requiring the pedestrian to adjust their path to avoid the vehicle. This near-miss situation occurs as the car moves from ...

### ex034-load-vehicle.mp4

- video: [`data/videos/meva_examples_selected10/ex034-load-vehicle.mp4`](data/videos/meva_examples_selected10/ex034-load-vehicle.mp4)
- outputs: [`load`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex034-load-vehicle.mp4__load.json) [`safety`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex034-load-vehicle.mp4__safety.json) [`security`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex034-load-vehicle.mp4__security.json) [`timeline`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex034-load-vehicle.mp4__timeline.json)

**Load/Physics**

- overall_risk: `SAFE`
- risk_reasoning: No visible loads, pallets, or lifting equipment are present in the scene. The individuals appear to be engaged in casual interaction near parked vehicles, with no indication of hazardous material handling or unsafe load operations.
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

### ex035-load-vehicle.mp4

- video: [`data/videos/meva_examples_selected10/ex035-load-vehicle.mp4`](data/videos/meva_examples_selected10/ex035-load-vehicle.mp4)
- outputs: [`load`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex035-load-vehicle.mp4__load.json) [`safety`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex035-load-vehicle.mp4__safety.json) [`security`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex035-load-vehicle.mp4__security.json) [`timeline`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex035-load-vehicle.mp4__timeline.json)

**Load/Physics**

- overall_risk: `SAFE`
- risk_reasoning: No active load handling, pallets, or lifting operations are observed. The telescopic handler and vehicles are stationary, with no visible unsafe interactions or unstable stacking.
- loads: `0`

**PPE/Safety**

- overall_compliance: `COMPLIANT`
- summary: No workers visible.
- workers: `0`

**Security/Access**

- overall_security: `CLEAR`
- recommended_action: Continue monitoring the scene for any sudden movements or unauthorized access to vehicles or restricted areas.
- persons: `3`
- person: `Person 2` `authorized`: Person 2 is interacting with the trunk of the white hatchback, which appears to be a routine activity (e.g., loading/unloading items). No suspicious behavior or restricted access is indicated.
- person: `Person 3` `authorized`: Person 3 is walking toward the white hatchback, likely to assist or observe Person 2’s activity. Their movement is normal and consistent with collaborative work in the parking lot.
- person: `Person 4` `authorized`: Person 4 is standing near the orange utility vehicle, which may be part of their operational role. No unusual behavior or restricted access is observed.

**Incident Timeline**

- events: `0`

### ex085-theft.mp4

- video: [`data/videos/meva_examples_selected10/ex085-theft.mp4`](data/videos/meva_examples_selected10/ex085-theft.mp4)
- outputs: [`load`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex085-theft.mp4__load.json) [`safety`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex085-theft.mp4__safety.json) [`security`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex085-theft.mp4__security.json) [`timeline`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex085-theft.mp4__timeline.json)

**Load/Physics**

- overall_risk: `SAFE`
- risk_reasoning: The scene depicts a waiting area with no visible loads, pallets, or lifting equipment. People are seated or standing casually, and there are no signs of industrial material handling activities. The environment appears stable with no immediate safety hazards related to load handling.
- loads: `0`

**PPE/Safety**

- overall_compliance: `COMPLIANT`
- summary: No workers visible.
- workers: `0`

**Security/Access**

- overall_security: `CLEAR`
- recommended_action: No assessment was possible as no clear indications of unauthorized access or suspicious behavior were observed.
- persons: `0`

**Incident Timeline**

- events: `1`
- event: 00:02.800-00:08.000 [theft/medium] A woman in dark clothing approaches another seated woman, takes an item from her, and walks away, flagged as a theft event by the system. This action involves direct interaction that could escalate into a conflict or ...

### ex086-unload-vehicle.mp4

- video: [`data/videos/meva_examples_selected10/ex086-unload-vehicle.mp4`](data/videos/meva_examples_selected10/ex086-unload-vehicle.mp4)
- outputs: [`load`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex086-unload-vehicle.mp4__load.json) [`safety`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex086-unload-vehicle.mp4__safety.json) [`security`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex086-unload-vehicle.mp4__security.json) [`timeline`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex086-unload-vehicle.mp4__timeline.json)

**Load/Physics**

- overall_risk: `SAFE`
- risk_reasoning: No lifting equipment or loads are visible in the scene. The individuals are manually handling items from a vehicle trunk without any indication of unsafe practices, equipment failure, or unstable stacking. The environment appears calm and controlled, with no immediate safety concerns.
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

### ex087-unload-vehicle.mp4

- video: [`data/videos/meva_examples_selected10/ex087-unload-vehicle.mp4`](data/videos/meva_examples_selected10/ex087-unload-vehicle.mp4)
- outputs: [`load`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex087-unload-vehicle.mp4__load.json) [`safety`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex087-unload-vehicle.mp4__safety.json) [`security`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex087-unload-vehicle.mp4__security.json) [`timeline`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex087-unload-vehicle.mp4__timeline.json)

**Load/Physics**

- overall_risk: `SAFE`
- risk_reasoning: No industrial activity, loads, or lifting equipment are present in the scene. The parking lot is static with no movement or handling of goods, indicating a low-risk environment.
- loads: `0`

**PPE/Safety**

- overall_compliance: `NON-COMPLIANT`
- summary: Worker near the red pickup truck lacks required PPE, including a high-visibility vest and safety glasses, posing a safety risk.
- workers: `1` (non-compliant: `1`)
- violation: `Worker N`: Worker not wearing high-visibility vest or safety glasses while performing tasks near parked vehicles.

**Security/Access**

- overall_security: `CLEAR`
- recommended_action: No assessment was possible as no human activity was observed in the video.
- persons: `0`

**Incident Timeline**

- events: `1`
- event: 00:11.50-00:12.80 [improper_handling/low] A person is actively loading or unloading items from a vehicle in the parking lot, with no immediate safety hazards observed in the scene. The individual is wearing dark clothing and appears to be handling objects nea...

### ex088-unload-vehicle.mp4

- video: [`data/videos/meva_examples_selected10/ex088-unload-vehicle.mp4`](data/videos/meva_examples_selected10/ex088-unload-vehicle.mp4)
- outputs: [`load`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex088-unload-vehicle.mp4__load.json) [`safety`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex088-unload-vehicle.mp4__safety.json) [`security`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex088-unload-vehicle.mp4__security.json) [`timeline`](outputs/runs/2026-03-04_meva_examples_selected10/per_stream/ex088-unload-vehicle.mp4__timeline.json)

**Load/Physics**

- overall_risk: `SAFE`
- risk_reasoning: No loads, pallets, or lifting equipment are visible or being handled in the scene. The individuals are either standing or walking without interacting with any objects that would require load-handling safety measures.
- loads: `0`

**PPE/Safety**

- overall_compliance: `COMPLIANT`
- summary: No workers visible.
- workers: `0`

**Security/Access**

- overall_security: `CLEAR`
- recommended_action: No assessment possible as no individuals are visible.
- persons: `0`

**Incident Timeline**

- events: `0`
