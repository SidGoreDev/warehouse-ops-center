#!/usr/bin/env bash
set -euo pipefail

if [ ! -f "lessons_learned.md" ]; then
  echo "ERROR: lessons_learned.md not found in repo root. Aborting."
  exit 1
fi

if [ -z "${NEBIUS_VLLM_BASE_URL:-}" ] || [ -z "${NEBIUS_VLLM_API_KEY:-}" ]; then
  echo "ERROR: NEBIUS_VLLM_BASE_URL / NEBIUS_VLLM_API_KEY not set. Aborting."
  exit 1
fi

MANIFEST="${1:-}"
if [ -z "$MANIFEST" ]; then
  echo "Usage: batch/batch_run_managed.sh <manifest.yaml>"
  exit 1
fi

python -m src.cli batch --manifest "$MANIFEST"
