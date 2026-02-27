from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .metrics import (
    load_overall_risk_accuracy,
    ppe_overall_compliance_accuracy,
    security_overall_accuracy,
    timeline_event_metrics,
)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate_results(*, results_dir: str, ground_truth_dir: str) -> Dict[str, Any]:
    """
    Offline evaluation against hand-labeled JSON.

    Conventions:
    - Results are files named: <video>__<mode>.json
    - Ground truth layout: <ground_truth_dir>/<video>/<mode>.json
      where <video> is the local video filename (including extension).
    """
    res_dir = Path(results_dir)
    gt_dir = Path(ground_truth_dir)

    report: Dict[str, Any] = {"results_dir": str(res_dir), "ground_truth_dir": str(gt_dir), "modes": {}}

    for mode in ("load", "safety", "security", "timeline", "full"):
        report["modes"][mode] = {"files": 0, "scored": 0, "metrics": {}}

    for p in res_dir.rglob("*.json"):
        name = p.name
        if "__" not in name:
            continue
        video, mode_ext = name.split("__", 1)
        mode = mode_ext.rsplit(".", 1)[0]
        if mode not in report["modes"]:
            continue
        report["modes"][mode]["files"] += 1

        gt_path = gt_dir / video / f"{mode}.json"
        if not gt_path.exists():
            continue

        pred = _load_json(p)
        gt = _load_json(gt_path)
        report["modes"][mode]["scored"] += 1

        if mode == "load":
            report["modes"][mode]["metrics"].setdefault("overall_risk_accuracy", []).append(
                load_overall_risk_accuracy(pred, gt)
            )
        elif mode == "safety":
            report["modes"][mode]["metrics"].setdefault("overall_compliance_accuracy", []).append(
                ppe_overall_compliance_accuracy(pred, gt)
            )
        elif mode == "security":
            report["modes"][mode]["metrics"].setdefault("overall_security_accuracy", []).append(
                security_overall_accuracy(pred, gt)
            )
        elif mode == "timeline":
            m = timeline_event_metrics(pred, gt)
            for k, v in m.items():
                report["modes"][mode]["metrics"].setdefault(k, []).append(v)

    # Reduce lists to averages
    for mode, md in report["modes"].items():
        for k, values in list(md["metrics"].items()):
            if not values:
                md["metrics"][k] = None
                continue
            md["metrics"][k] = sum(values) / len(values)

    return report
