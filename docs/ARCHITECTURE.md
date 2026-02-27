# Architecture (MVP)

Tier 1 MVP = 4 CR2 video reasoning modes + optional composite synthesis.

Data flow:
1. `src/cli.py` dispatches
2. `src/pipeline.py` builds a mode prompt and calls Nebius-managed vLLM (`src/client.py`)
3. Raw output is persisted; `<think>` and JSON are extracted (`src/parsing.py`)
4. Outputs are saved as `*.json` for downstream visualization/eval

We assume Nebius-managed deployments may not provide `reasoning_content`. `<think>` is the reasoning trace.
