from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..parsing import parse_mmssff_to_seconds


def _eq_ci(a: Optional[str], b: Optional[str]) -> float:
    if a is None or b is None:
        return 0.0
    return 1.0 if str(a).strip().lower() == str(b).strip().lower() else 0.0


def load_overall_risk_accuracy(pred: Dict[str, Any], gt: Dict[str, Any]) -> float:
    return _eq_ci(pred.get("overall_risk"), gt.get("overall_risk"))


def ppe_overall_compliance_accuracy(pred: Dict[str, Any], gt: Dict[str, Any]) -> float:
    return _eq_ci(pred.get("overall_compliance"), gt.get("overall_compliance"))


def security_overall_accuracy(pred: Dict[str, Any], gt: Dict[str, Any]) -> float:
    return _eq_ci(pred.get("overall_security"), gt.get("overall_security"))


def _event_key(e: Dict[str, Any]) -> str:
    # Use event_type + severity as a rough key.
    return f"{e.get('event_type','')}|{e.get('severity','')}".lower()


def timeline_event_metrics(pred: List[Dict[str, Any]], gt: List[Dict[str, Any]], *, tol_s: float = 2.0) -> Dict[str, float]:
    """
    Very lightweight timeline scoring:
    - match by (event_type, severity) and overlap within tol_s on start/end.
    Returns precision/recall/F1.
    """
    if not isinstance(pred, list) or not isinstance(gt, list):
        return {"precision": 0.0, "recall": 0.0, "f1": 0.0}

    gt_used = [False] * len(gt)
    tp = 0
    fp = 0

    for pe in pred:
        try:
            ps = parse_mmssff_to_seconds(pe["start"])
            pe_ = parse_mmssff_to_seconds(pe["end"])
        except Exception:  # noqa: BLE001
            fp += 1
            continue
        pk = _event_key(pe)

        matched = False
        for i, ge in enumerate(gt):
            if gt_used[i]:
                continue
            if _event_key(ge) != pk:
                continue
            try:
                gs = parse_mmssff_to_seconds(ge["start"])
                ge_ = parse_mmssff_to_seconds(ge["end"])
            except Exception:  # noqa: BLE001
                continue
            if abs(ps - gs) <= tol_s and abs(pe_ - ge_) <= tol_s:
                matched = True
                gt_used[i] = True
                break
        if matched:
            tp += 1
        else:
            fp += 1

    fn = gt_used.count(False)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}
