# Warehouse Ops Center — Physical AI Safety Reasoning
## NVIDIA Cosmos Cookoff Project Spec

**Codename:** WarehouseAI Critic
**Deadline:** March 5, 2026 — 5:00 PM PT
**Model:** Cosmos-Reason2-8B (required)
**Infra:** Nebius Cloud H100 + vLLM
**Prior art:** Physical AI Critic (previous repo) — see `lessons_learned.md`

> **⚠️ Required input:** This spec depends on `lessons_learned.md`, a summary of infrastructure access, tooling stack, known issues, and development patterns from the previous Physical AI Critic project. That file must live in the repo root and be read by any agent before starting implementation work. It contains Nebius Cloud access procedures, vLLM server configuration, the `reasoning_content` null workaround, and other hard-won operational knowledge that should NOT be re-derived from scratch.

---

## 1. Elevator Pitch

> One model. Multiple safety reasoning tasks. Zero custom CV models.

Cosmos Reason 2 is the system. Every analysis, every judgment, every physics chain-of-thought runs through a single VLM with domain-specific prompts. The project showcases what CR2's reasoning engine can do when pointed at real-world safety video:

- Read a scene and reason about **physical load limits, center of gravity, and stacking stability**
- Watch workers and reason about **what PPE is required given the activity observed**, not just detect what's present
- Observe behavior and reason about **whether a person's actions are authorized** based on visual context
- Generate **timestamped incident timelines** with structured JSON from unstructured video
- Produce **chain-of-thought physics narratives** that explain *why* something is dangerous, not just *that* it is

The `<think>` blocks are the product. The structured JSON is the delivery format. Everything else is scaffolding around CR2.

---

## 1B. Scope Tiers — The Crystal Structure

CR2 is the center of the crystal. Each tier adds capability radiating outward, but the inner tiers must be solid before expanding.

```
                    ┌─────────────────────────────┐
                    │       STRETCH (Tier 3)       │
                    │  Streamlit dashboard          │
                    │  Isaac Sim synthetic clips     │
                    │  Omniverse digital twin        │
                    │  NeMoGuard integration         │
                    │  PDF shift report export       │
                ┌───┴─────────────────────────────┴───┐
                │       ENHANCEMENT (Tier 2)           │
                │  Multi-stream correlation engine      │
                │  D3.js Timeline Correlation View      │
                │  Cross-camera causal reasoning        │
                │  Facility layout / zone adjacency     │
            ┌───┴─────────────────────────────────────┴───┐
            │              MVP (Tier 1)                    │
            │                                              │
            │  ┌────────────────────────────────────────┐  │
            │  │         COSMOS REASON 2                 │  │
            │  │   <think> physics reasoning </think>    │  │
            │  │   Structured JSON output                │  │
            │  │   4 analysis modes (single-stream)      │  │
            │  └────────────────────────────────────────┘  │
            │                                              │
            │  + CLI tool to run any mode on any video     │
            │  + MEVA dataset with curated test clips      │
            │  + Evaluation harness with ground truth      │
            │  + Demo video (< 3 min) showing CR2 in action│
            │  + Public repo with README                   │
            └──────────────────────────────────────────────┘
```

### Tier 1 — MVP (Contest Submission Requirement)

**This is what ships on March 5. Non-negotiable.**

Everything in Tier 1 is directly about Cosmos Reason 2 doing reasoning work on video.

| Component | What It Proves About CR2 |
|---|---|
| **Load Physics Analysis** | CR2 can ground objects in 2D, estimate physical properties (weight, CoG), and reason about capacity limits |
| **PPE Safety Audit** | CR2 can reason about context-dependent requirements — not just "is there a helmet" but "does this activity require a helmet" |
| **Security Access Detection** | CR2 can make authorization judgments from behavioral and visual cues with chain-of-thought justification |
| **Incident Timeline Generator** | CR2 can perform temporal localization with structured JSON output — directly from the prompt guide |
| **CLI tool** | Clean interface: `python -m src.cli analyze --mode load --video clip.mp4` → JSON output with `<think>` reasoning |
| **Evaluation harness** | Quantitative evidence that CR2 reasoning is grounded, not hallucinated |
| **Demo video** | 3-minute story showing CR2's reasoning quality across domains |
| **Public repo + README** | Reproducible, clear, professional |

**MVP quality bar:** A judge watches the demo video and thinks "CR2 is doing real physics reasoning here, not just describing what it sees." The `<think>` chains are the star of the show.

### Tier 2 — Enhancement (Build If MVP is Solid by Day 4)

Multi-stream correlation, timeline visualization, cross-camera causal reasoning. These are impressive engineering BUT they only matter if the per-stream CR2 reasoning is already compelling. The correlation engine is a second CR2 call (text-only reasoning on structured outputs), so it does showcase CR2 further — but it's additive, not foundational.

**Gate:** Only start Tier 2 work if GPU-2 results (Day 3) show that per-stream analysis modes produce high-quality reasoning chains and accurate structured output. If the per-stream prompts still need iteration, stay in Tier 1.

### Tier 3 — Stretch (Only If Tiers 1+2 Are Done and Polished)

Dashboard, synthetic data, guardrails integration, export formats. These are "future work" slide material — mention them in the demo video's closing 20 seconds, don't try to build them.

---

## 2. Competition Alignment

### Submission Checklist Mapping (MVP Focus)

| Requirement | How MVP Addresses It |
|---|---|
| **Problem & use case clearly explained** | Warehouse/facility injuries cost $15B/yr in the US. Current systems are object-detection-only — no physics reasoning about *why* something is dangerous |
| **Cosmos Reason 2 demonstrably integrated into core reasoning loop** | CR2 IS the system. Every analysis mode is a CR2 inference call with reasoning enabled. The `<think>` blocks contain physics-grounded chain-of-thought. No secondary models, no fallback classifiers. Four distinct reasoning tasks prove CR2's versatility, not just one trick |
| **Demo video < 3 min** | Structured around CR2 output quality: Problem (20s) → "CR2 is the system" (15s) → Four modes with `<think>` chains on screen (100s) → Evaluation results (15s) → Future vision (30s) |
| **Code + README** | Public GitHub repo with CLI tool, evaluation harness, curated MEVA clips, and reproducible results. Clean, professional, minimal dependencies |

### NVIDIA Stack Alignment

| NVIDIA Product | Connection |
|---|---|
| **Cosmos Reason 2** | Core reasoning engine — every inference is CR2 |
| **Metropolis** | Natural deployment target for edge warehouse cameras |
| **Omniverse / Isaac Sim** | Future work: digital twin warehouse with real-time safety overlay |
| **NeMo Guardrails** | Future work: confidence thresholding on safety-critical decisions |
| **Jetson** | Future work: edge inference for real-time camera feeds |

---

## 2B. Prior Project Handoff — `lessons_learned.md`

This is a **new repo**, not a continuation of the previous Physical AI Critic project. However, the previous project produced significant operational knowledge about the Cosmos Reason 2 / vLLM / Nebius Cloud stack that must carry forward. The file `lessons_learned.md` captures this knowledge and lives at the repo root.

### What `lessons_learned.md` Must Contain

Any agent or developer starting work on this repo should read `lessons_learned.md` FIRST before writing any code. The file should cover:

**Infrastructure & Access:**
- Nebius Cloud account setup and instance provisioning steps (H100 GPU)
- Public IP is volatile; verify in console before every session
- SSH key configuration and connection procedure
- Instance startup / shutdown procedure (console vs. CLI)
- Cost management notes (hourly rate, billing behavior on shutdown vs. terminate)

**Model Serving — vLLM:**
- If self-hosting vLLM: exact vLLM launch command for Cosmos-Reason2-8B (and any flags you control)
- If using a Nebius-managed vLLM template: document the deployed endpoint URL + model name string (do not assume you can change vLLM flags)
- Server health check / readiness verification
- Known startup time after restart (e.g., 1–2 minutes before vLLM responds)

**Known Issues & Workarounds:**
- `reasoning_content` may be null in Nebius-managed deployments — do not depend on it; parse `<think>...</think>` from raw output instead
- JSON parsing robustness and repair strategy for minor schema errors

**API Client Patterns:**
- OpenAI-compatible API endpoint at `http://<public_ip>:8000` (base URL, model name string)
- vLLM API key is separate from Nebius IAM auth (CLI)
- Environment variable names and legacy fallbacks used by the client
- Message format for video input (media-first ordering, video_url vs. base64)
- Sampling parameter defaults that worked well (temperature, top_p, top_k)
- Response parsing: how to reliably extract JSON from model output that may include preamble text

**Development Patterns:**
- What worked well in the previous project's development flow
- What wasted time or caused rework
- Prompt iteration strategy that was effective
- Evaluation approach and what metrics were meaningful
- Config precedence: CLI args → `.env` → environment variables → defaults
- Separation of concerns: thin client, pipeline, schema, CLI
- Offline tests with mocked HTTP responses
- Session-start SOP (console IP check, `.env` update, SSH, endpoint health check)

**Tool Stack:**
- Python version, key dependencies, virtual environment setup
- Nebius CLI is Linux-only; use WSL on Windows
- Any npm/Node dependencies used
- Git workflow and branch strategy used
- Local development environment notes (Windows/PowerShell specifics)

### How It's Consumed

The file is referenced in three ways:

1. **By agents:** Any AI coding agent (Claude Code, etc.) tasked with implementation work should be instructed to `cat lessons_learned.md` before starting. The file IS the onboarding doc.

2. **By the `client.py` module:** The vLLM client implementation should be built using the exact configuration documented in `lessons_learned.md` rather than guessing at parameters. Copy what worked.

3. **By `scripts/start_server.sh` (optional/self-host only):** If you self-host vLLM, the vLLM launch command should be lifted directly from the file, not reconstructed.

### What Does NOT Go in `lessons_learned.md`

- Secrets, API keys, or tokens (these go in `.env` or environment variables, referenced by name only)
- The full previous codebase (this is a summary, not a code dump)
- Anything specific to the old project's evaluation criteria or prompt templates (those are being rebuilt for the new domain)

---

## 2C. Operational Notes (from lessons_learned.md)

These are non-negotiable operational constraints carried over from the prior project. Follow them exactly.

**Access + endpoint reality:**
- Nebius VM public IP is **volatile**. Check the Nebius Console before every session and update `.env` with the current IP.
- The vLLM endpoint is OpenAI-compatible at `http://<public_ip>:8000`.
- If you see SSH host key mismatches after a restart, clear the old entry: `ssh-keygen -R <old_ip>`.
- Canonical SSH username is defined in cloud-init (previously `sgdev`). Use the exact configured username.

**Auth separation:**
- vLLM API key authenticates to the model endpoint. Nebius IAM auth (CLI) authenticates to the cloud control plane. They are **not interchangeable**.

**Reasoning parser reality:**
- On Nebius-managed deployments, you should assume `reasoning_content` may be null and you may not be able to change vLLM startup flags.
- Treat `<think>...</think>` in the raw message content as the canonical reasoning trace. Do not depend on `reasoning_content`.

**.env keys and precedence:**
- Required keys: `NEBIUS_VLLM_BASE_URL`, `NEBIUS_VLLM_API_KEY`, `NEBIUS_VLLM_MODEL`, `NEBIUS_VLLM_TIMEOUT_S`.
- Optional sampling overrides (defaults follow the NVIDIA prompt guide): `NEBIUS_VLLM_TEMPERATURE`, `NEBIUS_VLLM_TOP_P`, `NEBIUS_VLLM_TOP_K`, `NEBIUS_VLLM_PRESENCE_PENALTY`, `NEBIUS_VLLM_REPETITION_PENALTY`.
- Legacy fallbacks are supported: `COSMOS_API_BASE`, `COSMOS_API_KEY`, `COSMOS_MODEL`.

**CLI availability:**
- The Nebius CLI is Linux-only; on Windows, use WSL if you need the CLI. For ad-hoc checks, the web console is usually faster.

**Session-start SOP (short):**
1. Confirm VM running in Nebius Console and record current public IP.
2. Update `.env` with the current IP.
3. Verify SSH, then verify port 8000 reachability.
4. Hit `/v1/models` with the API key. A 401 without the key still means the endpoint is up.

---

## 3. System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     VIDEO INPUT LAYER                            │
│  Multiple streams: Cam 1 (.mp4), Cam 2 (.mp4), ... Cam N       │
│  Each stream: frame sampling @ 4fps (configurable)              │
│  Stream metadata: camera_id, location_zone, time_sync_offset    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  ANALYSIS ROUTER (CLI)                            │
│  Routes each stream to analysis modes (parallel or sequential)   │
│  Modes: load | safety | security | timeline | correlate | full   │
└──────┬────────┬────────┬────────┬──────────────────────────────┘
       │        │        │        │
       ▼        ▼        ▼        ▼
┌──────────┐┌──────────┐┌──────────┐┌──────────┐
│  LOAD    ││  SAFETY  ││ SECURITY ││ TIMELINE │
│ PHYSICS  ││   PPE    ││  ACCESS  ││  EVENT   │
│ ANALYST  ││  AUDIT   ││ DETECTOR ││ LOCALIZE │
└──────┬───┘└──────┬───┘└──────┬───┘└──────┬───┘
       │           │           │           │
       ▼           ▼           ▼           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  COSMOS REASON 2 (vLLM)                          │
│  System prompt: "You are a helpful assistant."                   │
│  Reasoning: enabled (<think> blocks)                             │
│  Sampling (reasoning): temp=0.6, top_p=0.95, top_k=20            │
│                     presence_penalty=0.0, repetition_penalty=1.0 │
│  Media-first message ordering                                    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              PER-STREAM OUTPUT LAYER                              │
│  Structured JSON per mode per stream                             │
│  Severity scoring: SAFE / WARNING / CRITICAL                     │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│           MULTI-STREAM CORRELATION ENGINE                        │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  TEMPORAL     │  │   CAUSAL     │  │  PATTERN     │          │
│  │  ALIGNMENT    │  │   CHAIN      │  │  DETECTION   │          │
│  │              │  │   REASONER   │  │              │          │
│  │ Sync streams │  │ CR2 reasons  │  │ Recurring    │          │
│  │ to common    │  │ about cross- │  │ hotspots,    │          │
│  │ time axis    │  │ stream cause │  │ time-of-day  │          │
│  │              │  │ and effect   │  │ patterns     │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                 │                 │                    │
│         ▼                 ▼                 ▼                    │
│  ┌─────────────────────────────────────────────────────┐        │
│  │            TIMELINE CORRELATION VIEW                 │        │
│  │  Multi-lane timeline visualization (HTML/Streamlit)  │        │
│  │  Lanes: one per camera stream                        │        │
│  │  Events: color-coded by type + severity              │        │
│  │  Correlation arcs: connecting related cross-stream   │        │
│  │  events with causal reasoning annotations            │        │
│  └─────────────────────────────────────────────────────┘        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              FACILITY SAFETY REPORT                               │
│  Composite report + correlated timeline + recommendations        │
│  Exportable: JSON, HTML dashboard, PDF shift report              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3B. NVIDIA Prompt Guide Conventions (Authoritative)

This project follows the NVIDIA Cosmos Reason 2 prompt guide conventions:
- System prompt: `"You are a helpful assistant."`
- Media-first message ordering (video part before text part)
- Reasoning enabled by appending the standard reasoning suffix

Reference: https://nvidia-cosmos.github.io/cosmos-cookbook/core_concepts/prompt_guide/reason_guide.html

**Standard reasoning suffix (append verbatim):**
```
Answer the question using the following format:

<think>
Your reasoning.
</think>

Write your final answer immediately after the </think> tag.
```

**Media/text order (OpenAI-compatible `messages`):**
```json
[
  {
    "role": "system",
    "content": [
      { "type": "text", "text": "You are a helpful assistant." }
    ]
  },
  {
    "role": "user",
    "content": [
      { "type": "video_url", "video_url": "https://example.com/video.mp4" },
      { "type": "text", "text": "YOUR PROMPT HERE (with reasoning suffix appended)" }
    ]
  }
]
```

**Sampling parameters (recommended):**
- Without reasoning: `top_p=0.95`, `top_k=20`, `temperature=0.2`, `presence_penalty=0.0`, `repetition_penalty=1.0`
- With reasoning: `top_p=0.95`, `top_k=20`, `temperature=0.6`, `presence_penalty=0.0`, `repetition_penalty=1.0`

## 4. Analysis Modes — Detailed Prompt Engineering

All prompts follow the Cosmos Reason 2 prompt guide conventions:
- System prompt: `"You are a helpful assistant."`
- Media (video_url) listed BEFORE user text
- Reasoning enabled with the standard `<think>` suffix
- Sampling: `temperature=0.6, top_p=0.95, top_k=20, presence_penalty=0.0, repetition_penalty=1.0`

### 4A. Load Physics Analyst

**Capability from guide:** 2D Grounding (bounding box + weight/size estimation)

**Prompt template:**
```
Analyze this warehouse/industrial scene for load handling safety.

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

Answer the question using the following format:

<think>
Your reasoning.
</think>

Write your final answer immediately after the </think> tag.
```

**Expected model behavior:** Chain-of-thought reasons about material density, pallet size, packaging type, center of gravity, forklift rated capacity. Outputs structured JSON with bounding boxes that can be visualized.

**Evaluation criteria:** Does the model correctly distinguish overloaded vs. safe loads? Does weight estimation scale sensibly with visual cues?

---

### 4B. PPE Safety Audit

**Capability from guide:** Safety analysis (PPE detection with reasoning)

**Prompt template:**
```
You are a warehouse safety auditor. Analyze this video for PPE (Personal Protective Equipment) compliance.

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

Answer the question using the following format:

<think>
Your reasoning.
</think>

Write your final answer immediately after the </think> tag.
```

**Key differentiator from the guide's example:** We add *contextual reasoning* — the model doesn't just detect PPE, it reasons about what PPE *should* be present given the observed activities (e.g., operating a forklift requires different PPE than stacking shelves).

---

### 4C. Security Access Detector

**Capability from guide:** Security analysis (authorization reasoning)

**Prompt template:**
```
Analyze this warehouse video for potential unauthorized access or suspicious behavior.

Consider:
1. Is each person's attire consistent with authorized warehouse personnel (uniforms, badges, PPE)?
2. Are their movements consistent with normal warehouse operations or do they appear lost, hurried, or evasive?
3. Are they accessing areas that appear restricted (marked zones, locked areas, management offices)?
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

Answer the question using the following format:

<think>
Your reasoning.
</think>

Write your final answer immediately after the </think> tag.
```

---

### 4D. Incident Timeline Generator

**Capability from guide:** Temporal localization with JSON timestamps

**Prompt template:**
```
Analyze this warehouse video and generate a timestamped incident report of all safety-relevant events.

Safety-relevant events include:
- Near-misses (forklift near pedestrian, falling objects narrowly avoided)
- PPE violations (removal of equipment, entering zone without required gear)
- Improper material handling (overloaded pallets, unsafe stacking, dragging loads)
- Ergonomic risks (improper lifting posture, repetitive strain movements)
- Equipment misuse (speeding forklifts, blocked emergency exits)

Provide timestamps in mm:ss.ff format. Return as JSON:
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

Answer the question using the following format:

<think>
Your reasoning.
</think>

Write your final answer immediately after the </think> tag and include the timestamps.
```

---

### 4E. Full Shift Report (Composite Mode)

Runs all four modes sequentially on the same video, then generates a composite report:

```
You have analyzed a warehouse video segment. Here are the results from four analysis passes:

LOAD ANALYSIS: {load_json}
PPE AUDIT: {safety_json}
SECURITY SCAN: {security_json}
INCIDENT TIMELINE: {timeline_json}

Synthesize these into a single shift safety report. Include:
1. Executive summary (2-3 sentences)
2. Critical findings requiring immediate action
3. Overall safety score (0-100)
4. Top 3 recommendations

Return as JSON:
{
  "executive_summary": "string",
  "safety_score": number,
  "critical_findings": ["list"],
  "recommendations": ["list"],
  "shift_status": "NORMAL | ELEVATED_RISK | UNSAFE"
}

Answer the question using the following format:

<think>
Your reasoning.
</think>

Write your final answer immediately after the </think> tag.
```

This is a **second-pass CR2 call** (text-only) that synthesizes the four structured outputs into an executive report. This keeps the system strictly "one model, multiple reasoning tasks" while still demonstrating a multi-step reasoning pipeline.

---

### 4F. Multi-Stream Incident Correlator & Timeline View

This is the capstone feature. It takes incident timelines generated by Mode 4D from **multiple camera streams**, aligns them temporally, and uses Cosmos Reason 2 to reason about **causal chains** that span cameras. A forklift speeding in Aisle 3 (Camera 3) at 10:42 that causes a worker to jump out of the way in Aisle 4 (Camera 7) at 10:43 — these are separate events in separate video feeds. The correlator connects them.

#### Input Schema — Stream Registry

Each video feed is registered with metadata:

```json
{
  "streams": [
    {
      "stream_id": "cam_01",
      "label": "Dock Loading Bay A",
      "zone": "receiving",
      "video_path": "data/videos/cam01_shift_0800.mp4",
      "time_offset_seconds": 0,
      "analysis_modes": ["load", "safety", "timeline"]
    },
    {
      "stream_id": "cam_03",
      "label": "Aisle 3 — Heavy Equipment",
      "zone": "storage_heavy",
      "video_path": "data/videos/cam03_shift_0800.mp4",
      "time_offset_seconds": 2.4,
      "analysis_modes": ["safety", "security", "timeline"]
    },
    {
      "stream_id": "cam_07",
      "label": "Aisle 4 — Pedestrian Corridor",
      "zone": "pedestrian",
      "video_path": "data/videos/cam07_shift_0800.mp4",
      "time_offset_seconds": -0.8,
      "analysis_modes": ["safety", "timeline"]
    }
  ],
  "facility_layout": {
    "zone_adjacency": {
      "receiving": ["storage_heavy", "staging"],
      "storage_heavy": ["receiving", "pedestrian", "storage_light"],
      "pedestrian": ["storage_heavy", "storage_light", "shipping"]
    }
  }
}
```

The `time_offset_seconds` field handles camera clock drift — real warehouse systems never have perfectly synced clocks. The `zone_adjacency` map tells the correlator which cameras could plausibly observe causally linked events (a forklift in Receiving can't cause a near-miss in Shipping without traversing intermediate zones).

#### Step 1: Per-Stream Analysis

Run Mode 4D (Incident Timeline) on each stream independently. This produces a timestamped incident list per camera:

```json
{
  "stream_id": "cam_03",
  "incidents": [
    {
      "start": "00:42.10",
      "end": "00:44.80",
      "event_type": "equipment_misuse",
      "severity": "high",
      "description": "Forklift traveling above safe speed limit in storage aisle with limited visibility",
      "entities": ["forklift_01"],
      "physics_reasoning": "At estimated 12mph in a 5mph zone, stopping distance exceeds aisle intersection clearance by ~3m"
    }
  ]
}
```

#### Step 2: Temporal Alignment

Normalize all incident timestamps to facility-absolute time using `time_offset_seconds`:

```
absolute_time = stream_local_time + time_offset_seconds
```

Then build a **merged incident timeline** sorted by absolute time across all streams:

```json
[
  { "abs_time": "00:42.10", "stream": "cam_03", "event": "forklift_speeding", "severity": "high" },
  { "abs_time": "00:43.30", "stream": "cam_07", "event": "near_miss_pedestrian", "severity": "critical" },
  { "abs_time": "00:45.00", "stream": "cam_01", "event": "improper_load_drop", "severity": "medium" }
]
```

#### Step 3: Candidate Correlation — Windowed Proximity + Zone Adjacency

Before calling CR2 (expensive), apply cheap heuristic filters to identify **candidate event pairs** worth reasoning about:

```
CORRELATION CANDIDATES:
- Time window: events within ±30 seconds of each other
- Zone proximity: events in adjacent zones per facility_layout
- Entity tracking: same entity descriptor across streams (e.g., "forklift_01" in both)
- Severity escalation: lower severity → higher severity in temporal sequence
```

This keeps the CR2 correlation call focused. In a 12-camera warehouse with 50 events, you might have 200+ possible pairs but only 10-15 pass the heuristic filter.

#### Step 4: Causal Chain Reasoning (CR2)

**This is where CR2 earns its keep.** Feed the candidate pairs back into Cosmos Reason 2 as a text-only reasoning task (no video needed — the per-stream analysis already extracted the physics reasoning):

**Prompt template:**
```
You are a warehouse safety analyst. You have incident reports from multiple camera streams in the same facility. Analyze the following candidate event pairs for causal relationships.

FACILITY ZONE LAYOUT:
{zone_adjacency_json}

CANDIDATE EVENT PAIRS:
{candidate_pairs_json}

For each pair, determine:
1. Is there a plausible causal or contributing relationship?
2. What is the causal mechanism? (e.g., speeding vehicle → evasive action, dropped load → blocked aisle → rerouted traffic)
3. What is the confidence level (high/medium/low)?
4. If causal, what is the root cause and the cascade sequence?

Return as JSON:
{
  "correlations": [
    {
      "event_a": {"stream": "string", "abs_time": "string", "description": "string"},
      "event_b": {"stream": "string", "abs_time": "string", "description": "string"},
      "is_correlated": boolean,
      "causal_direction": "a_causes_b | b_causes_a | common_cause | coincidental",
      "causal_mechanism": "string",
      "confidence": "high | medium | low",
      "root_cause": "string or null",
      "cascade_sequence": ["ordered list of events in causal chain"]
    }
  ],
  "facility_hotspots": [
    {
      "zone": "string",
      "incident_density": number,
      "primary_risk_type": "string",
      "recommendation": "string"
    }
  ],
  "shift_narrative": "A 2-3 sentence plain-English summary of what happened across the facility during this period."
}

Answer the question using the following format:

<think>
Your reasoning.
</think>

Write your final answer immediately after the </think> tag.
```

**Why this works:** The per-stream analysis already did the hard vision work. The correlation step is *purely reasoning* — exactly what the `<think>` chain is built for. The model reasons about physics propagation (stopping distance, trajectory), spatial relationships (adjacent zones), and temporal plausibility (cause must precede effect, with realistic propagation delay).

#### Step 5: Timeline Correlation View — Visualization

The visual output is a **multi-lane swimlane timeline** rendered as an interactive HTML artifact or Streamlit component:

```
FACILITY TIMELINE — Shift 08:00-16:00
═══════════════════════════════════════════════════════════════════

Cam 01 │ ▰▰▰▰                    ▰▰          ▰▰▰▰▰▰
Dock A │ [load:ok]               [load:⚠]     [ppe:✗]

Cam 03 │           ▰▰▰▰▰▰▰▰                ▰▰▰▰
Aisle3 │           [equip:🔴]──────┐        [load:⚠]
                                    │ causal
Cam 07 │              ▰▰▰▰▰▰▰▰▰▰▰▰┘
Aisle4 │              [near_miss:🔴]

Cam 12 │     ▰▰                         ▰▰▰▰▰▰▰▰▰▰▰▰
Ship B │     [security:⚠]               [ppe:✗ → safety:🔴]

─────────┼────────────────────────────────────────────────────
         08:00    09:00    10:00    11:00    12:00    13:00
```

**Visual encoding:**
- **Lanes:** One horizontal lane per camera stream, labeled with camera ID + zone name
- **Event blocks:** Colored rectangles positioned by start/end time
  - Green = SAFE/low severity
  - Yellow/orange = WARNING/medium
  - Red = CRITICAL/high
- **Correlation arcs:** Curved lines connecting causally related events across lanes, with a label showing the causal mechanism
- **Hotspot shading:** Zone background color intensity proportional to incident density
- **Hover/click detail:** Expanding an event shows the full CR2 reasoning chain, including the `<think>` output

#### Implementation — HTML Timeline Component

```
src/visualization/
├── timeline_correlator.py    # Core correlation logic (Steps 2-4)
├── timeline_view.html        # Self-contained HTML timeline renderer
├── timeline_data.js          # JSON → D3.js timeline transformation
└── timeline_styles.css       # Color encoding, severity palette
```

**Technology choice:** D3.js for the timeline visualization, rendered as a standalone HTML file. Reasons:
- Self-contained (no server required for demo video)
- Visually striking for screen recording
- Interactive for live demo (hover to see reasoning chains)
- Exportable as screenshot for static presentation

**D3.js timeline structure:**
```javascript
// Each lane = one SVG group, positioned vertically
// Events = rect elements with color fill by severity
// Correlations = path elements (bezier curves) between event rects
// Hover popover = foreignObject with HTML content showing <think> chain

const laneHeight = 60;
const timeScale = d3.scaleTime()
  .domain([shiftStart, shiftEnd])
  .range([marginLeft, width - marginRight]);

// Event blocks
lanes.selectAll('.event')
  .data(d => d.incidents)
  .enter().append('rect')
  .attr('x', d => timeScale(d.abs_start))
  .attr('width', d => timeScale(d.abs_end) - timeScale(d.abs_start))
  .attr('fill', d => severityColor(d.severity));

// Correlation arcs between lanes
svg.selectAll('.correlation')
  .data(correlations.filter(c => c.is_correlated))
  .enter().append('path')
  .attr('d', d => bezierArc(
    timeScale(d.event_a.abs_time), laneY(d.event_a.stream),
    timeScale(d.event_b.abs_time), laneY(d.event_b.stream)
  ))
  .attr('stroke', d => confidenceColor(d.confidence))
  .attr('stroke-dasharray', d => d.confidence === 'low' ? '4,4' : 'none');
```

#### Output Artifacts

The correlator produces three output artifacts:

1. **`correlation_report.json`** — Full structured output from the CR2 correlation pass
2. **`timeline_view.html`** — Interactive D3.js timeline (open in browser, demo-ready)
3. **`shift_summary.md`** — Human-readable shift narrative with key findings

#### Example Correlation Output

```json
{
  "correlations": [
    {
      "event_a": {
        "stream": "cam_03",
        "abs_time": "10:42:10",
        "description": "Forklift traveling above safe speed in storage aisle"
      },
      "event_b": {
        "stream": "cam_07",
        "abs_time": "10:43:30",
        "description": "Pedestrian worker takes evasive action, stumbles near shelving"
      },
      "is_correlated": true,
      "causal_direction": "a_causes_b",
      "causal_mechanism": "Forklift exceeding speed limit in Aisle 3 entered intersection with Aisle 4 pedestrian corridor. At estimated 12mph, forklift was visible to pedestrian for <2 seconds before intersection. Worker reacted with lateral evasive movement, lost footing on smooth concrete surface.",
      "confidence": "high",
      "root_cause": "Forklift speed violation in Zone storage_heavy",
      "cascade_sequence": [
        "Forklift exceeds 5mph zone limit (cam_03, 10:42:10)",
        "Forklift enters Aisle 3/4 intersection (cam_03, 10:43:00)",
        "Worker detects approaching forklift (cam_07, 10:43:15)",
        "Worker takes evasive action (cam_07, 10:43:30)",
        "Worker stumbles near shelving unit (cam_07, 10:43:45)"
      ]
    }
  ],
  "facility_hotspots": [
    {
      "zone": "storage_heavy",
      "incident_density": 4.2,
      "primary_risk_type": "equipment_misuse",
      "recommendation": "Install speed monitoring sensors in Aisle 3. Consider physical speed bumps at zone intersections."
    }
  ],
  "shift_narrative": "During the 08:00-16:00 shift, 14 incidents were detected across 4 camera streams. The most significant finding is a causal chain originating from repeated forklift speed violations in the heavy storage zone, which contributed to 3 separate pedestrian near-misses in the adjacent corridor. The receiving dock showed intermittent PPE compliance gaps during shift change at 12:00."
}
```

---

## 5. Video Data Sources

### Data Strategy: Why Dataset Choice is Critical

The correlation feature lives or dies on having **multi-camera video from the same facility at the same time** with events that genuinely propagate across camera views. Random YouTube clips stitched together will look fake to judges. We need a reputable, citable dataset where:
- Multiple cameras observe the same physical space simultaneously
- Cameras are GPS/NTP time-synced (or sync metadata is provided)
- A site map with camera positions and fields-of-view exists
- Activity annotations are available (saves labeling time)
- Licensing permits public use (CC-BY or similar)

### Primary Dataset: MEVA (Multiview Extended Video with Activities)

**Source:** [mevadata.org](https://mevadata.org) — Kitware / IARPA DIVA program
**License:** CC-BY-4.0
**Download:** Free via AWS S3 (AWS Public Dataset Program, no cost)
**Citation:** Corona et al., "MEVA: A Large-Scale Multiview, Multimodal Video Dataset for Activity Detection," WACV 2021

| Property | Detail |
|---|---|
| **Total video** | 9,300+ hours (328 hours publicly released as KF1) |
| **Camera count** | 29 ground cameras (EO + thermal IR) + 2 DJI drones |
| **View topology** | Overlapping AND non-overlapping fields of view, indoor + outdoor |
| **Time sync** | NAS clocks synchronized via GPS; 5-minute clip boundaries |
| **Annotations** | 184 hours annotated for 37 activity types with bounding boxes |
| **Site map** | PDF with camera locations, approximate FOVs, zone layout |
| **3D model** | Dense 3D point cloud of outdoor scene |
| **Camera models** | Geo-registration parameters for outdoor cameras |
| **Actors** | ~100 actors performing scripted + spontaneous activities |
| **Format** | MP4, various resolutions (commodity CCTV cameras) |

**Why MEVA is the right choice:**

1. **Multi-camera correlation is native.** Activities were explicitly scripted to occur across overlapping and non-overlapping camera views. The same individual performs activities in different cameras — exactly what our correlator needs.
2. **Site map = facility layout.** The PDF with camera positions and FOVs maps directly to our `zone_adjacency` graph. We don't have to fabricate the spatial relationships.
3. **Time-synchronized clips.** GPS-synced NAS clocks mean our `time_offset_seconds` calculations are grounded in real clock drift, not guesswork.
4. **Pre-existing annotations.** 37 activity types already labeled saves massive ground truth effort. We can map relevant activities to our safety event taxonomy.
5. **Academic credibility.** WACV-published, IARPA-funded, NIST ActEV challenge benchmark. Judges see a reputable dataset, not cobbled YouTube clips.
6. **CC-BY-4.0.** Clean licensing for public GitHub repo and demo video.

**MEVA clip selection strategy:**

We don't need all 328 hours. We curate a **focused scenario package** of 15-25 clips (5 min each):

| Scenario | Clips | Cameras | What We Show |
|---|---|---|---|
| **Cross-view activity chain** | 3-4 overlapping clips from same time window | 3-4 cameras with overlapping/adjacent FOVs | Person/vehicle moves across camera views — correlator tracks the causal chain |
| **Simultaneous multi-zone activity** | 4-6 clips, same time window, different zones | Spatially separated cameras | Independent events happening in parallel — correlator correctly identifies NO causal link (false positive suppression) |
| **Indoor-outdoor transition** | 2-3 clips spanning indoor/outdoor boundary | Indoor + outdoor cameras | Activity begins inside (e.g., loading), continues outside — correlator bridges the transition |
| **Safety-relevant scenarios** | 4-6 clips with identifiable safety events | Various | PPE gaps, vehicle-pedestrian proximity, access control situations — per-stream analysis modes |

**Data download & prep workflow:**

```bash
# Download specific clips from AWS S3 (no cost)
aws s3 cp s3://mevadata-public-01/drops-123-r13/ data/meva/ \
  --recursive --exclude "*" \
  --include "2018-03-11.*G328*" \
  --include "2018-03-11.*G329*" \
  --include "2018-03-11.*G330*" \
  --no-sign-request

# Download site map and camera metadata
aws s3 cp s3://mevadata-public-01/drops-123-r13/site-map.pdf data/meva/ --no-sign-request

# Download annotations for selected clips
git clone https://gitlab.kitware.com/meva/meva-data-repo.git data/meva/annotations/
```

### Supplementary: Domain-Specific Safety Datasets (Per-Stream Modes)

MEVA provides the multi-camera backbone for correlation. For per-stream analysis modes that need warehouse-specific content (forklifts, PPE, heavy loads), supplement with:

| Dataset | Source | License | Use Case |
|---|---|---|---|
| **SH17 Dataset** | [github.com/ahmadmughees/sh17dataset](https://github.com/ahmadmughees/sh17dataset) | Academic | 8,099 images, 17 PPE classes from manufacturing environments. Reference for PPE analysis ground truth |
| **Construction-PPE** | [Ultralytics/construction-ppe](https://docs.ultralytics.com/datasets/detect/construction-ppe/) | AGPL-3.0 | Helmet, vest, gloves, boots detection + "missing" classes. Useful for PPE mode validation |
| **Industrial Safety Video Dataset** | [ScienceDirect — Eskişehir facility](https://www.sciencedirect.com/science/article/pii/S235234092400756X) | Academic | 691 clips from real factory security cameras. 8 behavior classes including "Carrying Overload with Forklift" and "Unauthorized Intervention" — directly maps to our load physics + security modes |
| **VIRAT** | [viratdata.org](https://viratdata.org) | DARPA/public | Multi-site surveillance with vehicle-person interactions. Useful for security analysis mode |

### Tertiary: Synthetic (Isaac Sim) — Stretch Goal

If time permits, generate 2-3 controlled synthetic clips in Isaac Sim:
- Forklift approaching overloaded pallet (known physics violation)
- Robot arm stacking with deliberate instability
- Worker navigating around autonomous mobile robot

These provide controlled test cases with exact ground truth but are NOT required for the core submission.

### Clip Specifications

- **Duration:** 5-minute clips (MEVA native format); trim to 30-60s segments for per-stream analysis
- **Resolution:** Varies by camera (commodity CCTV, typically 1280x720 to 1920x1080)
- **FPS:** Source at native rate, sampled at 4fps for CR2 inference (per prompt guide recommendation)
- **Format:** MP4 (H.264)
- **Target corpus:** 15-25 MEVA clips + 4-6 supplementary domain clips
- **Correlation scenarios:** Minimum 3 multi-stream scenarios with 3-4 cameras each

---

## 5B. GPU Cost Optimization Strategy

### Principle: Develop Offline, Infer in Bursts

The Nebius H100 instance costs real money per hour. We do NOT keep it running throughout the 7-day development cycle. The vast majority of the work — code, prompts, data curation, visualization, evaluation harness, documentation — is CPU-only. GPU time is needed only for CR2 inference passes.

**Development split estimate:**
- ~85% of work is offline (code, data prep, viz, docs)
- ~15% requires GPU (inference runs against CR2 via vLLM)

### Workflow: GPU Burst Sessions

```
DEVELOPMENT CYCLE (repeating)

┌──────────────────────────────────────────────────┐
│           OFFLINE PHASE (local machine)            │
│                                                    │
│  • Write / refine prompt templates                 │
│  • Build / update output parsers                   │
│  • Curate & prep video clips (download, trim)      │
│  • Build evaluation harness + ground truth labels  │
│  • Build visualization components (D3.js, etc.)    │
│  • Write correlation logic (alignment, filtering)  │
│  • Write documentation, README, demo script        │
│  • Review previous inference outputs               │
│  • Queue up the exact inference jobs to run         │
│                                                    │
│  Deliverable: batch_run_managed.sh — a script that │
│  ALL queued inference jobs sequentially             │
└──────────────────────┬─────────────────────────────┘
                       │
                       │  "Ready for GPU"
                       ▼
┌──────────────────────────────────────────────────┐
│           GPU BURST SESSION (Nebius H100)           │
│                                                    │
│  1. Sid spins up the instance                      │
│  2. Pull latest code from repo                     │
│  3. Verify the vLLM endpoint is ready              │
│  4. Run batch_run_managed.sh                       │
│     → Per-stream analysis on all queued clips      │
│     → Correlation passes on all scenarios          │
│     → Evaluation suite against ground truth        │
│  5. Collect all outputs to data/results/           │
│  6. Push results to repo                           │
│  7. Shut down the instance                         │
│                                                    │
│  Target: 1-3 hours per burst session               │
│  Total GPU sessions: 4-5 across the 7-day cycle    │
└──────────────────────┬─────────────────────────────┘
                       │
                       │  "Results available"
                       ▼
┌──────────────────────────────────────────────────┐
│           OFFLINE REVIEW (local machine)            │
│                                                    │
│  • Inspect inference outputs (JSON, reasoning)     │
│  • Score against ground truth                      │
│  • Identify prompt weaknesses                      │
│  • Update prompts, parsers, filtering logic        │
│  • Prepare next batch of inference jobs             │
│  • Loop back to Offline Phase                      │
└──────────────────────────────────────────────────┘
```

### GPU Session Plan (Projected)

| Session | Day | Duration | Purpose |
|---|---|---|---|
| **GPU-1** | Day 2 (Feb 27) | ~2 hrs | Smoke test: run load_physics + ppe_safety prompts on 4-6 clips. Validate vLLM setup, output parsing, reasoning quality. Kill early if prompts need rework |
| **GPU-2** | Day 3 (Feb 28) | ~2 hrs | Full per-stream pass: all 4 analysis modes on full clip corpus. First timeline generation runs. Capture baseline metrics |
| **GPU-3** | Day 4 (Mar 1) | ~2 hrs | Correlation pipeline: run incident timelines on multi-stream scenarios, then run correlation reasoning pass. First end-to-end pipeline test |
| **GPU-4** | Day 5 (Mar 2) | ~2 hrs | Prompt-tuned re-run: updated prompts based on GPU-2/3 review. Full evaluation suite. Generate final outputs for demo video |
| **GPU-5** | Day 6 (Mar 3) | ~1 hr | Polish pass: re-run any clips where output quality wasn't demo-ready. Generate final pre-baked outputs for demo recording |

**Estimated total GPU time: 8-10 hours** across 5 sessions (vs. 168 hours if left running all week).

### Batch Runner Design

All inference jobs are queued as a declarative manifest so Sid can review before spinning up:

```yaml
# batch_manifest.yaml — review before GPU session
session: gpu-3
description: "First correlation pipeline test"

jobs:
  # Per-stream analysis (must run first — outputs feed into correlation)
  - type: per_stream
    mode: timeline
    clips:
      - { stream_id: cam_G328, path: data/meva/2018-03-11.G328.clip01.mp4 }
      - { stream_id: cam_G329, path: data/meva/2018-03-11.G329.clip01.mp4 }
      - { stream_id: cam_G330, path: data/meva/2018-03-11.G330.clip01.mp4 }
    output_dir: data/results/gpu-3/per_stream/

  - type: per_stream
    mode: safety
    clips:
      - { stream_id: cam_G328, path: data/meva/2018-03-11.G328.clip01.mp4 }
    output_dir: data/results/gpu-3/per_stream/

  # Correlation pass (runs after per-stream completes)
  - type: correlation
    scenario: data/streams/scenario_meva_01.json
    per_stream_results: data/results/gpu-3/per_stream/
    output_dir: data/results/gpu-3/correlation/

  # Evaluation
  - type: evaluation
    results_dir: data/results/gpu-3/
    ground_truth_dir: data/ground_truth/
    output: data/results/gpu-3/eval_report.json
```

```bash
# batch_run_managed.sh — executed against Nebius-managed vLLM (no server flags to tweak)
#!/bin/bash
set -euo pipefail

# Verify lessons_learned.md exists (runbook + known issues)
if [ ! -f "lessons_learned.md" ]; then
  echo "ERROR: lessons_learned.md not found in repo root. Aborting."
  exit 1
fi

if [ -z "${NEBIUS_VLLM_BASE_URL:-}" ] || [ -z "${NEBIUS_VLLM_API_KEY:-}" ]; then
  echo "ERROR: NEBIUS_VLLM_BASE_URL / NEBIUS_VLLM_API_KEY not set. Aborting."
  exit 1
fi

echo "Running batch manifest: $1"
python -m src.cli batch --manifest "$1"

echo "Results saved. Push to repo and shut down instance."
```

### Pre-GPU Checklist (run before every session)

- [ ] `.env` updated with current VM public IP (from Nebius Console)
- [ ] Port 8000 reachability verified; `/v1/models` returns 200 with API key (401 without key is expected)
- [ ] `lessons_learned.md` is in repo root and has been read by the implementing agent
- [ ] If self-hosting vLLM (optional): `scripts/start_server.sh` matches the intended vLLM launch command
- [ ] `client.py` uses the API config and workarounds from `lessons_learned.md`
- [ ] `batch_manifest.yaml` reviewed — only jobs that need GPU are included
- [ ] All video clips pre-downloaded and in `data/` (no downloading on GPU time)
- [ ] All code changes committed and pushed (pull on instance, don't code there)
- [ ] Output directories exist and are clean
- [ ] Previous session results backed up
- [ ] Estimated runtime calculated (# clips × ~30s per inference + overhead)

---

## 6. Evaluation Framework

### Quantitative Metrics (Per Mode)

**Load Physics:**
- Weight estimation accuracy (within ±30% of labeled ground truth)
- Bounding box IoU against manual annotations
- Binary overload detection accuracy (overloaded vs. safe)

**PPE Compliance:**
- Per-item detection accuracy (hard hat, vest, gloves — binary per item)
- Activity-appropriate PPE reasoning accuracy (does model correctly infer required PPE from context?)

**Security:**
- Binary authorized/unauthorized classification accuracy
- Behavioral indicator relevance (manual scoring 1-5)

**Timeline:**
- Temporal localization accuracy (±2 seconds of ground truth event boundaries)
- Event type classification accuracy
- False positive rate (spurious events)

**Cross-Stream Correlation:**
- Causal pair precision: Of correlations the model identifies, how many are genuine? (target: >70%)
- Causal pair recall: Of known causal links in ground truth, how many does the model find? (target: >60%)
- Causal direction accuracy: When a link is correctly identified, is the direction right? (target: >80%)
- Spurious correlation rate: How many "coincidental" events does the model incorrectly flag as causal?
- Hotspot zone agreement: Does the model identify the same high-risk zones as ground truth?

### Qualitative Metrics

- **Reasoning quality:** Are `<think>` chains physically grounded? Do they reference real physics concepts (center of gravity, load moment, friction)?
- **Causal mechanism plausibility:** When the model explains *why* two events are linked, does the physics narrative make sense? (e.g., "stopping distance exceeded clearance" vs. vague "these events are related")
- **Cross-mode consistency:** When run in full-report mode, do the five analyses agree or contradict?
- **Cascade sequence coherence:** Are the ordered steps in a causal chain temporally and spatially consistent?
- **Actionability:** Are recommendations specific enough to act on?

### Test Set

Build a labeled test set:

**Per-stream clips (8-12 clips):**
- 3 clips with known load physics scenarios (1 safe, 1 marginal, 1 overloaded)
- 3 clips with PPE scenarios (1 compliant, 1 partial, 1 non-compliant)
- 2 clips with security scenarios (1 authorized worker, 1 ambiguous)
- 2-4 clips with mixed scenarios for timeline generation

**Multi-stream correlation scenarios (2-3 scenarios):**
- Scenario A: 3 streams, 1 obvious causal chain (forklift speed → near-miss), 1 coincidental pair
- Scenario B: 4 streams, 2 independent causal chains, overlapping time windows (tests discrimination)
- Scenario C: 3 streams, no true causal links (tests false positive suppression)

Each clip and scenario gets a hand-labeled ground truth JSON matching the output schema.

---

## 7. Demo Video Script (< 3 minutes)

### MVP Demo — "The Reasoning is the Product"

The demo video's single job: make a judge think "CR2 is doing real physics reasoning, not just describing video." Every second of screen time should feature CR2 output — the `<think>` chain or the structured JSON. Minimize architecture diagrams, minimize future work, maximize the model talking.

**[0:00 - 0:20] THE PROBLEM**
- Text overlay: "Warehouse injuries cost $15 billion/year in the US"
- Quick montage: safety footage, OSHA statistic
- Voiceover: "Current systems detect objects. They don't understand physics. They can't tell you *why* something is dangerous."

**[0:20 - 0:35] THE THESIS — CR2 IS THE SYSTEM**
- Simple text card (not a complex architecture diagram): "One model. Cosmos Reason 2. Four safety reasoning tasks. Zero custom CV models."
- Brief CLI command flash: `python -m src.cli analyze --mode load --video forklift.mp4`
- Voiceover: "We give Cosmos Reason 2 a video and a safety question. It reasons through the physics and returns a structured judgment."

**[0:35 - 1:10] MODE 1 — LOAD PHYSICS (35 seconds)**

This gets the most time because it's the most visually striking CR2 capability.

- Show the video clip (forklift approaching loaded pallet)
- **The star: `<think>` chain scrolling on screen** — CR2 reasoning about estimated pallet weight based on material/packaging, center of gravity position relative to fork tines, rated capacity of the forklift model observed, stability margin
- JSON output appears: bounding box coordinates, estimated weight, `stability_assessment: "marginal"`, `equipment_limit_exceeded: true`
- Voiceover: "The model isn't just detecting objects. It's estimating weight from visual cues, calculating whether the load exceeds the forklift's rated capacity, and reasoning about tipping risk."

**[1:10 - 1:40] MODE 2 — PPE SAFETY AUDIT (30 seconds)**

This mode shows CR2's contextual reasoning — the differentiator from simple object detection.

- Show video of worker near heavy equipment
- **`<think>` chain on screen** — CR2 identifying what the worker IS wearing, then reasoning about what they SHOULD be wearing given the observed activity (near forklift = hard hat required, handling materials = gloves required)
- JSON output: `observed_ppe: ["vest"]`, `required_ppe: ["vest", "hard_hat", "gloves"]`, `compliant: false`
- Voiceover: "It doesn't just check for a helmet. It reasons about what PPE is *required* based on the activity it observes. That's physics-aware safety reasoning."

**[1:40 - 2:00] MODE 3 — SECURITY ACCESS (20 seconds)**

Shorter — shows CR2 reasoning about behavioral cues.

- Video of person in facility
- **`<think>` chain** — reasoning about attire consistency, movement patterns, area authorization
- JSON output with authorization assessment and behavioral indicators
- Voiceover: "Same model, different safety question. CR2 reasons about whether behavior matches authorized personnel patterns."

**[2:00 - 2:20] MODE 4 — INCIDENT TIMELINE (20 seconds)**

Shows temporal localization capability directly from the prompt guide.

- Longer video clip plays
- JSON timeline output with `mm:ss.ff` timestamps, event types, severity levels
- Voiceover: "From a single video, CR2 generates a timestamped incident report — temporal localization with physics-aware event classification."

**[2:20 - 2:35] EVALUATION RESULTS (15 seconds)**

Quick credibility hit — show numbers.

- Table/overlay with evaluation metrics across modes
- Highlight reasoning quality: "X% of `<think>` chains reference specific physics concepts"
- Voiceover: "Tested against [N] curated clips from the MEVA multi-camera dataset, with hand-labeled ground truth."

**[2:35 - 3:00] FUTURE VISION + CLOSE (25 seconds)**

- "Four tasks, one model. But this is just the beginning."
- Quick mention: multi-camera correlation (Tier 2), NVIDIA Metropolis for edge deployment, Omniverse for digital twins
- "Cosmos Reason 2 doesn't just see the warehouse. It understands the physics."
- End card: GitHub link, "Built for the NVIDIA Cosmos Cookoff"

### Enhancement: If Tier 2 is Complete, Modify the Demo

If the correlation engine is working by Day 6, compress Modes 3+4 (save 15s) and insert a 30-second correlation segment at [2:00 - 2:30] showing:
- "Now watch what happens when we connect the streams."
- Timeline Correlation View with correlation arcs
- This becomes the climax — but only if it's actually working and polished

**Do NOT sacrifice Mode 1 or Mode 2 screen time for the correlation.** The per-stream CR2 reasoning is the core submission. The correlation is bonus points.

### Production Notes

- **`<think>` chains are the visual centerpiece.** Display them as semi-transparent text overlaying the video, or as a scrolling sidebar. They should feel like watching CR2 "think out loud."
- Screen recordings of actual terminal/CLI output for authenticity
- Clean terminal theme (dark background, syntax-highlighted JSON output)
- Keep motion graphics minimal — let the model's output speak
- Background music: subtle, corporate-tech (royalty-free)
- **Pre-bake all outputs.** The demo video shows real CR2 output, but don't run live inference during recording. Use saved results from GPU-4.

---

## 8. Repo Structure

```
warehouse-ops-center/
├── README.md                    # Setup, usage, architecture overview
├── lessons_learned.md            # REQUIRED: Prior project handoff — read before any implementation
├── LICENSE
├── requirements.txt
├── setup.sh                     # One-command environment setup
│
├── src/
│   ├── __init__.py
│   ├── cli.py                   # Main entry point: `python -m src.cli analyze`
│   ├── client.py                # vLLM / OpenAI-compatible API client
│   ├── prompts/
│   │   ├── load_physics.py      # Prompt templates + output parsers
│   │   ├── ppe_safety.py
│   │   ├── security_access.py
│   │   ├── incident_timeline.py
│   │   ├── causal_correlation.py  # Cross-stream causal reasoning prompt
│   │   └── composite_report.py
│   ├── correlation/
│   │   ├── stream_registry.py   # Multi-stream config + metadata management
│   │   ├── temporal_align.py    # Clock sync + absolute time normalization
│   │   ├── candidate_filter.py  # Heuristic pre-filter (time window, zone adjacency, entity match)
│   │   ├── correlator.py        # Orchestrator: align → filter → CR2 reason → output
│   │   └── facility_layout.py   # Zone adjacency graph + spatial reasoning helpers
│   ├── evaluation/
│   │   ├── evaluator.py         # Run test suite against labeled data
│   │   ├── metrics.py           # Accuracy, IoU, temporal overlap
│   │   └── report.py            # Generate evaluation summary
│   └── visualization/
│       ├── bbox_overlay.py      # Draw bounding boxes on frames
│       ├── timeline_plot.py     # Simple Matplotlib timeline (single stream)
│       ├── timeline_view/       # Multi-stream correlation timeline (D3.js)
│       │   ├── index.html       # Self-contained interactive timeline
│       │   ├── timeline.js      # D3.js rendering logic
│       │   ├── styles.css       # Severity palette, lane layout
│       │   └── generate.py      # Python: JSON results → inject into HTML template
│       └── dashboard.py         # (Optional) Streamlit multi-panel view
│
├── data/
│   ├── meva/                    # MEVA dataset clips (downloaded from AWS S3)
│   │   ├── site-map.pdf         # Camera positions + FOVs
│   │   ├── annotations/         # MEVA activity annotations repo
│   │   └── clips/               # Selected 5-min clips, organized by camera
│   ├── supplementary/           # Domain-specific clips (SH17, Industrial Safety)
│   ├── videos/                  # Trimmed clips ready for inference (30-60s)
│   ├── streams/                 # Multi-stream scenario configs
│   │   ├── scenario_meva_01.json
│   │   └── scenario_meva_02.json
│   ├── ground_truth/            # Labeled JSON ground truth per clip + per scenario
│   └── results/                 # Model outputs organized by GPU session
│       ├── gpu-1/
│       ├── gpu-2/
│       └── ...
│
├── batch/                       # GPU burst session management
│   ├── batch_manifest_gpu1.yaml # Jobs for each GPU session (review before spinning up)
│   ├── batch_manifest_gpu2.yaml
│   ├── batch_run_managed.sh     # Executor: run manifest against Nebius-managed vLLM endpoint, collect outputs
│   └── pre_gpu_checklist.md     # Checklist to run before every GPU session
│
├── configs/
│   ├── server.yaml              # vLLM server configuration
│   ├── evaluation.yaml          # Eval suite configuration
│   └── correlation.yaml         # Correlation params (time window, severity thresholds)
│
├── scripts/
│   ├── start_server.sh          # Optional: launch self-hosted vLLM with CR2 (Nebius-managed deployments already run vLLM)
│   ├── run_evaluation.sh        # Full eval pipeline
│   ├── run_correlation.sh       # Multi-stream correlation pipeline
│   └── generate_demo.sh         # Generate demo outputs for video
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── PROMPTING_STRATEGY.md    # Detailed prompt eng documentation
│   ├── CORRELATION_DESIGN.md    # Multi-stream correlation deep dive
│   └── EVALUATION_RESULTS.md    # Results + analysis
│
└── demo/
    ├── demo_outputs/            # Pre-generated outputs for demo video
    ├── demo_timeline.html       # Pre-built correlation timeline for screen recording
    └── demo_script.md           # Shot-by-shot demo video plan
```

---

## 9. Implementation Plan (7 days → March 5)

> **Key principle 1:** All code, data prep, visualization, and documentation happen OFFLINE. Nebius H100 spins up only for inference bursts. See Section 5B.
>
> **Key principle 2: MVP first.** Days 1-4 are exclusively Tier 1 (CR2 reasoning quality). Tier 2 work only begins if the MVP gate is passed. A polished Tier 1 submission beats a half-baked Tier 1+2 submission every time.

### Day 1 (Feb 26): Data Acquisition + Foundation — OFFLINE [TIER 1]

**Prerequisites (before anything else):**
- [ ] `lessons_learned.md` generated from previous project and placed in repo root
- [ ] Verify it covers: Nebius access, volatile IP + SOP, vLLM launch command, reasoning_content workaround, sampling params, API client patterns, auth separation
- [ ] Any agent assigned to this repo reads `lessons_learned.md` as first action

**Data acquisition:**
- [ ] Download MEVA KF1 clips from AWS S3 (targeted subset — focus on clips with clear activity annotations)
- [ ] Download MEVA site map PDF, camera metadata, annotations repo
- [ ] Select 8-12 clips for per-stream analysis across the 4 MVP modes
- [ ] Trim clips to 30-60s segments for CR2 inference
- [ ] Begin hand-labeling ground truth for selected clips

**Foundation (informed by lessons_learned.md):**
- [ ] Set up repo structure
- [ ] Port vLLM client code using exact config from `lessons_learned.md`
- [ ] Port `reasoning_content` null workaround
- [ ] Port sampling parameter defaults
- [ ] Optional (self-host only): write `scripts/start_server.sh` from `lessons_learned.md`

### Day 2 (Feb 27): All 4 CR2 Modes + GPU-1 — OFFLINE → GPU [TIER 1]

**OFFLINE (morning):**
- [ ] Implement `load_physics.py` prompt + parser
- [ ] Implement `ppe_safety.py` prompt + parser
- [ ] Implement `security_access.py` prompt + parser
- [ ] Implement `incident_timeline.py` prompt + parser
- [ ] Prepare `batch_manifest_gpu1.yaml` — all 4 modes on 4-6 clips each

**GPU-1 (~2 hrs, afternoon):**
- [ ] Spin up Nebius H100, pull code, verify the vLLM endpoint is up
- [ ] Run all 4 modes across test clips
- [ ] Collect outputs, push to repo, shut down instance

**OFFLINE (evening):**
- [ ] **Critical review: Are the `<think>` chains doing real physics reasoning?**
- [ ] Score each output: Does it reference specific physics concepts (CoG, force, friction, load moment) or is it generic description?
- [ ] Identify which modes produce strong reasoning vs. which need prompt rework
- [ ] Label ground truth for all test clips

### Day 3 (Feb 28): Prompt Iteration + Evaluation + GPU-2 — OFFLINE → GPU [TIER 1]

**OFFLINE (morning):**
- [ ] Rewrite prompts for any modes that produced weak reasoning in GPU-1
- [ ] Add physics scaffolding to prompts if needed (e.g., explicit rubric: "Consider: center of gravity, rated capacity, moment arm...")
- [ ] Implement `composite_report.py` (synthesis pass — also a CR2 call)
- [ ] Build evaluation harness (`evaluator.py`, `metrics.py`)
- [ ] Complete ground truth labeling for full clip corpus
- [ ] Prepare `batch_manifest_gpu2.yaml` — all modes, full corpus, with updated prompts

**GPU-2 (~2 hrs, afternoon):**
- [ ] Full per-stream pass with refined prompts on all curated clips
- [ ] Composite report generation on best clips
- [ ] Run evaluation against ground truth
- [ ] Collect outputs, push, shut down

**OFFLINE (evening):**
- [ ] Score evaluation results
- [ ] Review composite report quality
- [ ] **Assess: Are 3+ modes producing demo-quality `<think>` reasoning?**

### ═══════════════ MVP TIER GATE — End of Day 3 ═══════════════

**Decision point.** Review GPU-2 outputs and answer honestly:

✅ **GATE PASSED — Proceed to Tier 2 on Day 4** if:
- At least 3 of 4 modes produce `<think>` chains with specific physics reasoning (not generic descriptions)
- JSON outputs parse cleanly and contain plausible structured data
- Evaluation metrics are defensible (not perfect, but grounded)
- You have at least 2 clips per mode that would look good in a demo video

❌ **GATE FAILED — Stay in Tier 1 on Day 4** if:
- `<think>` chains are generic ("this looks unsafe") rather than physics-grounded
- JSON parsing is unreliable (need to fix output format issues)
- Only 1-2 modes produce good output (others need prompt rework)
- No single clip produces output you'd be proud to show a judge

If the gate fails, Day 4 becomes another prompt iteration + GPU cycle. The MVP must be solid before adding complexity.

### Day 4 (Mar 1): [TIER 1 continued OR TIER 2 start] — OFFLINE → GPU

**If GATE PASSED — Tier 2: Correlation Engine**

OFFLINE (morning):
- [ ] Implement correlation pipeline: `stream_registry.py`, `temporal_align.py`, `candidate_filter.py`, `correlator.py`
- [ ] Build zone adjacency from MEVA site map
- [ ] Implement `causal_correlation.py` prompt (CR2 text-only reasoning on structured outputs)
- [ ] Select 2-3 multi-camera MEVA clip groupings for correlation scenarios
- [ ] Prepare `batch_manifest_gpu3.yaml`

GPU-3 (~2 hrs, afternoon):
- [ ] Per-stream timelines on correlation scenario clips
- [ ] Correlation reasoning pass
- [ ] Collect outputs, push, shut down

OFFLINE (evening):
- [ ] Review correlation quality — do causal chains make sense?
- [ ] If good: proceed to Tier 2 visualization on Day 5
- [ ] If weak: drop correlation, revert to MVP-only demo plan

**If GATE FAILED — Tier 1 continued: Prompt Tuning**

OFFLINE (morning):
- [ ] Deep prompt engineering iteration on weak modes
- [ ] Try alternative prompt strategies: few-shot examples, explicit physics rubrics, constrained output formats
- [ ] Test prompts against mock outputs offline before GPU
- [ ] Prepare `batch_manifest_gpu3.yaml` — focused re-test of problem modes

GPU-3 (~2 hrs, afternoon):
- [ ] Re-run revised prompts
- [ ] Re-run evaluation
- [ ] Collect outputs, push, shut down

OFFLINE (evening):
- [ ] Final assessment — is the MVP demo-quality now?

### Day 5 (Mar 2): MVP Polish + [Optional Tier 2 Viz] — OFFLINE → GPU

**Regardless of tier path, Day 5 priorities are:**

1. **MVP outputs locked.** Select the best output per mode for the demo video. These are the "hero clips."
2. **Evaluation documented.** Final metrics captured, written up.
3. **GPU-4: Final inference pass** (~2 hrs) with any last prompt tweaks. Generate the outputs that will appear in the demo.

**If Tier 2 is in play:**
- [ ] Build D3.js Timeline Correlation View (or simpler Matplotlib fallback)
- [ ] Generate timeline HTML from correlation outputs
- [ ] Assess: does it enhance the demo or distract from CR2 reasoning?

**OFFLINE (evening):**
- [ ] All demo outputs selected and saved to `demo/demo_outputs/`
- [ ] Begin demo script finalization based on actual outputs (not hypothetical)

### Day 6 (Mar 3): Demo Video Production — OFFLINE → GPU-5 (if needed)

- [ ] Attend AMA session (9 AM)
- [ ] Record Mode 1 (Load Physics) demo — show `<think>` chain prominently
- [ ] Record Mode 2 (PPE Safety) demo — show contextual reasoning
- [ ] Record Mode 3 (Security) demo
- [ ] Record Mode 4 (Timeline) demo
- [ ] If Tier 2: record correlation segment
- [ ] GPU-5 (~1 hr): only if a specific clip needs re-running for demo quality
- [ ] Edit demo video (target 2:50)
- [ ] Write final README

### Day 7 (Mar 4): Polish + Submit — OFFLINE

- [ ] Final README polish — tested in clean environment
- [ ] All docs finalized (ARCHITECTURE.md, PROMPTING_STRATEGY.md)
- [ ] Verify all demo outputs committed
- [ ] Push to public GitHub
- [ ] Submit via Luma participation guide
- [ ] Buffer for anything that slipped

### GPU Budget Summary

| Session | Day | Tier | Est. Duration | Purpose |
|---|---|---|---|---|
| **GPU-1** | Day 2 | MVP | ~2 hrs | All 4 modes on test clips — first reasoning quality check |
| **GPU-2** | Day 3 | MVP | ~2 hrs | Refined prompts, full corpus, evaluation baseline |
| **GPU-3** | Day 4 | MVP or Tier 2 | ~2 hrs | Either prompt tuning re-run OR correlation pipeline |
| **GPU-4** | Day 5 | MVP lock | ~2 hrs | Final outputs for demo video |
| **GPU-5** | Day 6 | Polish | ~1 hr | Only if needed for specific demo clips |
| **Total** | | | **~9 hrs** | **vs. 168 hrs always-on → ~95% savings** |

---

## 10. Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| CR2 struggles with warehouse-specific physics reasoning | Medium | High | Pre-test with 2-3 clips before committing. Fall back to more constrained prompts with explicit physics rubrics if needed |
| `reasoning_content` null issue (known from current project) | High | Medium | Workaround documented in `lessons_learned.md`. Port the fallback parser for `<think>` tokens in raw output directly — do not re-derive |
| Video quality/resolution too low for grounding | Medium | Medium | Pre-filter clips for minimum 720p. Increase frame sampling rate if needed |
| Demo video takes too long to produce | Medium | Medium | Pre-record terminal sessions early. Use simple screen recording + voiceover, skip fancy motion graphics if time-crunched |
| Evaluation metrics look weak | Medium | High | Frame as "reference implementation" not "SOTA benchmark." Emphasize reasoning quality and multi-mode architecture over raw accuracy numbers |
| Isaac Sim synthetic clips don't materialize in time | High | Low | These are "nice to have" for cross-domain demo. YouTube/stock footage is sufficient for all core functionality |
| CR2 correlation reasoning hallucinates causal links | Medium | High | Tight candidate filtering (time window + zone adjacency) reduces noise input. Add confidence thresholds — suppress "low" confidence correlations in the visualization. Worst case: curate scenario videos that have obvious causal links |
| D3.js timeline visualization takes too long to build | Medium | Medium | Fallback: static Matplotlib multi-lane timeline (less interactive but still visually clear). The correlation JSON output is the real deliverable; the viz is polish |
| Multi-stream scenario doesn't produce correlatable events | Medium | High | MEVA was designed with overlapping FOVs and cross-camera scripted activities — this is its strength. Pre-screen clips by watching them before GPU runs. Select clips from the same time window where activity annotations show concurrent events across cameras |
| MEVA content is outdoor/military-facility, not warehouse | Medium | Medium | Frame as "facility safety" not strictly "warehouse." The physics reasoning (vehicle-pedestrian, access control, PPE) transfers directly. Supplement with domain-specific clips from SH17/Industrial Safety dataset for warehouse-specific per-stream demos |
| MEVA download is slow or clips are too large | Low | Medium | Pre-download on Day 1 (offline). MEVA is on AWS S3 with no-cost sponsorship. Selective download via --include filters, not full 328hrs. Each 5-min clip is ~100MB |
| GPU burst session reveals broken code, wastes GPU time | Medium | Medium | Pre-GPU checklist (Section 5B) enforced before every session. All code tested with mock/dummy outputs offline. batch_manifest reviewed before spinning up. First session (GPU-1) is deliberately small (4-6 clips) as a smoke test |
| `lessons_learned.md` is incomplete or missing critical config | Medium | High | Day 1 prerequisite gate: verify file covers all sections listed in Section 2B before any code is written. If gaps exist, consult previous repo directly or re-derive from Nebius/vLLM docs. Block GPU-1 until the file is validated |

---

## 11. Competitive Positioning

### What wins this contest

The email is clear: "Cosmos Reason 2 demonstrably integrated into the core reasoning or decision-making loop." The judges want to see CR2 doing something impressive. Everything else is context.

**What a judge needs to see in 3 minutes:**
1. CR2 producing `<think>` chains that contain real physics reasoning — force, mass, stability, trajectory, not just "this looks unsafe"
2. Structured JSON output that proves the reasoning isn't just narration but produces actionable, parseable judgments
3. Multiple distinct reasoning tasks proving CR2's versatility (not one trick pony)
4. Clean code they can clone and run

### What makes this different from "just a video QA chatbot"

1. **Physics-grounded reasoning** — The `<think>` chains reference physical concepts (center of gravity, load moment, material density), not just visual descriptions. This is what the model was built for
2. **Multi-task prompt architecture** — Four distinct reasoning modes from one model through prompt engineering. Shows CR2's range, not just depth
3. **Structured output pipeline** — Not freeform chat responses. Typed JSON schemas that could plug into a safety management system
4. **Real dataset, real evaluation** — MEVA multi-camera dataset with hand-labeled ground truth, not cherry-picked examples
5. **Direct NVIDIA stack alignment** — Every future work connection maps to a real NVIDIA product

### What judges will remember

- The `<think>` reasoning chain where CR2 estimates a pallet's weight from visual cues and calculates it exceeds the forklift's rated capacity — that's the money shot
- The PPE mode where CR2 reasons about what's *required*, not just what's *present* — contextual safety reasoning
- Clean CLI: `python -m src.cli analyze --mode load --video clip.mp4` → physics judgment in JSON
- Professional repo with evaluation metrics, not just a demo script

---

## 12. Scope Tiers — Detailed

### Tier 2 — Enhancement (if MVP gate passes)

All Tier 2 items are documented in detail in Section 4F of this spec. Summary:

- **Multi-stream correlation engine** — temporal alignment, candidate filtering, CR2 causal reasoning across camera feeds
- **D3.js Timeline Correlation View** — interactive multi-lane swimlane visualization
- **Facility layout / zone adjacency** — spatial reasoning graph from MEVA site map
- **Composite shift report** — synthesis of per-stream + correlation outputs

These are valuable because the correlation step is itself a CR2 reasoning task (text-only, operating on structured per-stream outputs). It demonstrates CR2 doing causal reasoning, not just perception. But it's additive — the MVP must be solid first.

### Tier 3 — Stretch (mention in demo, don't build)

- **Streamlit dashboard** — Unified view: video playback + analysis + correlation timeline
- **Isaac Sim synthetic clips** — Controlled scenarios with known ground truth
- **Real-time streaming mode** — WebSocket-based live video processing
- **Confidence calibration** — Reliability metrics per analysis type
- **NeMoGuard integration** — Guardrail validation on safety-critical outputs
- **Comparative analysis** — GPT-4V vs. CR2 head-to-head on same clips
- **PDF shift report export** — Printable regulatory compliance reports
- **Omniverse digital twin overlay** — 3D warehouse model with incident heatmaps
