# RUNBOOK (Nebius + vLLM)

This repo assumes a Nebius-managed vLLM endpoint serving `nvidia/Cosmos-Reason2-8B`.

## Session-Start SOP

1. In Nebius Console: confirm VM is running and note the current public IP.
2. Update `.env`:
   - `NEBIUS_VLLM_BASE_URL=http://<ip>:8000`
   - `NEBIUS_VLLM_API_KEY=...`
3. Verify the endpoint:
   - `powershell -File scripts/check_nebius_access.ps1 -Ip <ip>`

## Common Failures

- IP changed → update `.env` and clear `known_hosts` if SSHing.
- `/v1/models` returns 401 → endpoint reachable; API key missing/wrong.
- `reasoning_content` is null → expected on Nebius-managed templates; parse `<think>` from raw output.
