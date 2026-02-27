# RUNBOOK (Nebius + vLLM)

This repo assumes a Nebius-managed vLLM endpoint serving `nvidia/Cosmos-Reason2-8B`.

## Session-Start SOP

1. In Nebius Console: confirm VM is running and note the current public IP.
2. Update `.env`:
   - `NEBIUS_VLLM_BASE_URL=http://<ip>:8000`
   - `NEBIUS_VLLM_API_KEY=...`
3. Verify the endpoint:
   - `powershell -File scripts/check_nebius_access.ps1 -Ip <ip>`

## GPU Day Command Sequence (Minimal, Repeatable)

1. Endpoint sanity:
   - `powershell -File scripts/check_nebius_access.ps1 -Ip <ip>`
2. Single-clip smoke test (pick a 10-20s clip first):
   - `python -m src.cli analyze --mode load --video data/videos/clip01.mp4 --force`
   - Confirm `outputs/*.json` parses and `<think>` exists in `outputs/*.think.txt`.
3. Run the batch manifest:
   - `powershell -File batch/batch_run_managed.ps1 -Manifest batch/batch_manifest_gpu1.yaml`
4. If results look good, move to full corpus:
   - `powershell -File batch/batch_run_managed.ps1 -Manifest batch/batch_manifest_gpu2.yaml`

## Stop Conditions (Don’t Burn GPU Time)

- JSON parse failure rate > 20% on the smoke test → fix prompts/parsing offline first.
- `<think>` traces are generic (“this looks unsafe”) across modes → tighten prompts before scaling.
- Base64 payloads are too large / requests time out → trim clips shorter (10-20s) and retry.

## Common Failures

- IP changed → update `.env` and clear `known_hosts` if SSHing.
- `/v1/models` returns 401 → endpoint reachable; API key missing/wrong.
- `reasoning_content` is null → expected on Nebius-managed templates; parse `<think>` from raw output.
