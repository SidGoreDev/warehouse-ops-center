#!/usr/bin/env bash
set -euo pipefail

RESULTS_DIR="${1:-outputs}"
GT_DIR="${2:-data/ground_truth}"
OUT="${3:-outputs/eval_report.json}"

python -m src.cli eval --results "$RESULTS_DIR" --ground-truth "$GT_DIR" --out "$OUT"
