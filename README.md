# Warehouse Ops Center — Physical AI Safety Reasoning

Cosmos Reason 2 (CR2) is the system: one model, multiple safety reasoning tasks on video, delivered as structured JSON + `<think>` reasoning traces.

This repo is driven by:
- `warehouse-ops-center-spec.md` (project spec)
- `lessons_learned.md` (Nebius/vLLM operational runbook and gotchas)

## Requirements

- Python 3.11+
- Nebius-managed vLLM endpoint serving `nvidia/Cosmos-Reason2-8B`

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` with your Nebius endpoint IP and API key.

## CLI

Analyze a single video:

```powershell
python -m src.cli analyze --mode load --video .\data\videos\clip.mp4
```

Modes: `load`, `safety`, `security`, `timeline`, `full`

Run a batch manifest:

```powershell
python -m src.cli batch --manifest .\batch\batch_manifest_example.yaml
```

Run evaluation (offline, against hand-labeled ground truth):

```powershell
python -m src.cli eval --results .\outputs --ground-truth .\data\ground_truth --out .\outputs\eval_report.json
```

Run tests:

```powershell
python -m unittest discover -s tests
```

## Nebius Notes

- Assume `reasoning_content` is not available. We parse `<think>...</think>` from the raw assistant message.
- We do not assume we can change vLLM startup flags on Nebius-managed deployments.

## Prompting Convention

We follow the NVIDIA Cosmos reason prompt guide (see `warehouse-ops-center-spec.md` Section 3B): media-first ordering + the standard reasoning suffix appended to the user prompt.
