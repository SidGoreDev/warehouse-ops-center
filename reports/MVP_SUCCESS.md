# MVP Success: Warehouse Ops Center Prototype

Date: `2026-03-04`

This document captures proof that the prototype is working end-to-end: ingest short surveillance clips, run multimodal analysis (load/safety/security/timeline) via Nebius vLLM, parse structured JSON, and generate a human-readable markdown report.

## What “MVP Working” Means Here

- We can call the Nebius OpenAI-compatible endpoint successfully with auth.
- We can run analysis on a small batch of video clips on GPU.
- Each mode returns machine-parseable JSON saved to disk.
- We can compile those JSON results into a readable markdown “test report”.

## Evidence (Artifacts In Repo)

- Batch manifest used for the successful run:
  - `batch/batch_manifest_meva_school_selected_30s_copy.yaml`
- Markdown report generator:
  - `scripts/make_md_report.py`
- Generated report from the run (human-readable):
  - `reports/test_report_meva_school_selected_30s.md`

Notes:
- The underlying raw videos + per-clip JSON outputs are not committed (they live under `data/` and `outputs/`).
- We trimmed source videos with stream-copy (no re-encode) to avoid “ghosting/blurry” artifacts from MediaFoundation H.264 encoding.

## How To Reproduce (From Scratch)

1. Set `.env` (do not commit secrets):
   - `NEBIUS_VLLM_BASE_URL=http://89.169.114.226:8000`
   - `NEBIUS_VLLM_API_KEY=...`
   - `NEBIUS_VLLM_MODEL=nvidia/Cosmos-Reason2-8B`

2. Validate connectivity + auth:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\check_nebius_access.ps1 -Ip 89.169.114.226
```

3. Run the 5-clip batch (4 modes per clip):

```powershell
python -m src.cli batch --manifest batch\batch_manifest_meva_school_selected_30s_copy.yaml --force
```

4. Generate the markdown report from saved JSON outputs:

```powershell
python scripts\make_md_report.py --results-dir outputs\auto\per_stream --out reports\test_report_meva_school_selected_30s.md
```

## Known Runtime Compatibility Quirk (Handled)

On this Nebius/vLLM deployment, sending `mm_processor_kwargs` caused a `400` with an error mentioning `Qwen3VLProcessor`.

The pipeline now:
- Tries the NVIDIA-recommended `mm_processor_kwargs` first.
- Automatically retries without `mm_processor_kwargs` if that specific processor error occurs.

This keeps the MVP runnable without requiring server-side flag changes.

## Dataset Note: Better Clips Exist Than The “School” Picks

Yes—MEVA’s public bucket includes an `examples/` section with many small, labeled clips (often only a few MB each). These are typically much better for demos than randomly sampling hour-long site/camera footage.

Recommended starting points for warehouse-ops-adjacent behavior:
- `examples/videos/ex027-heavy-carry.mp4` (and `ex028`, `ex029`)
- `examples/videos/ex033-load-vehicle.mp4` (and `ex034`, `ex035`)
- `examples/videos/ex086-unload-vehicle.mp4` (and `ex087`, `ex088`)
- `examples/videos/ex097-vehicle-reversing.mp4` (and `ex098`, `ex099`, `ex100`)
- `examples/videos/ex000-abandon-package.mp4` (security-relevant)
- `examples/videos/ex085-theft.mp4` (security-relevant)

To explore what’s available without downloading the full dataset:

```powershell
python scripts\meva_s3.py ls --s3-uri s3://mevadata-public-01/examples/videos/ --all
```

## Next Step (Suggested)

Run the same 4-mode batch + markdown report on ~10 curated `examples/videos/*.mp4` clips to produce a stronger demo report with clearer events.

