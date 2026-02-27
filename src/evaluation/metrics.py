from __future__ import annotations

from typing import Any, Dict, List, Optional

from ..parsing import parse_mmssff_to_seconds


def _eq_ci(a: Optional[str], b: Optional[str]) -> float:
    if a is None or b is None:
        return 0.0
    return 1.0 if str(a).strip().lower() == str(b).strip().lower() else 0.0


def load_overall_risk_accuracy(pred: Dict[str, Any], gt: Dict[str, Any]) -> float:
    return _eq_ci(pred.get("overall_risk"), gt.get("overall_risk"))


def load_overload_any_accuracy(pred: Dict[str, Any], gt: Dict[str, Any]) -> float:
    def any_over(d: Dict[str, Any]) -> bool:
        loads = d.get("loads", [])
        if not isinstance(loads, list):
            return False
        return any(bool(x.get("equipment_limit_exceeded")) for x in loads if isinstance(x, dict))

    return 1.0 if any_over(pred) == any_over(gt) else 0.0


def ppe_overall_compliance_accuracy(pred: Dict[str, Any], gt: Dict[str, Any]) -> float:
    return _eq_ci(pred.get("overall_compliance"), gt.get("overall_compliance"))


def _jaccard(a: List[str], b: List[str]) -> float:
    sa = {str(x).strip().lower() for x in a if x is not None}
    sb = {str(x).strip().lower() for x in b if x is not None}
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / len(sa | sb) if (sa | sb) else 0.0


def ppe_worker_set_metrics(pred: Dict[str, Any], gt: Dict[str, Any]) -> Dict[str, float]:
    """
    Average set similarity across workers for observed_ppe and required_ppe.
    Workers are matched by worker_id when possible; otherwise by index.
    """
    pw = pred.get("workers", [])
    gw = gt.get("workers", [])
    if not isinstance(pw, list) or not isinstance(gw, list):
        return {"observed_ppe_jaccard": 0.0, "required_ppe_jaccard": 0.0, "worker_compliant_accuracy": 0.0}

    gt_by_id = {w.get("worker_id"): w for w in gw if isinstance(w, dict) and w.get("worker_id") is not None}

    obs_scores: List[float] = []
    req_scores: List[float] = []
    comp_scores: List[float] = []

    for idx, w in enumerate(pw):
        if not isinstance(w, dict):
            continue
        wid = w.get("worker_id")
        gw_match = gt_by_id.get(wid) if wid in gt_by_id else (gw[idx] if idx < len(gw) else None)
        if not isinstance(gw_match, dict):
            continue

        obs_scores.append(_jaccard(w.get("observed_ppe", []) or [], gw_match.get("observed_ppe", []) or []))
        req_scores.append(_jaccard(w.get("required_ppe", []) or [], gw_match.get("required_ppe", []) or []))
        comp_scores.append(1.0 if bool(w.get("compliant")) == bool(gw_match.get("compliant")) else 0.0)

    def avg(xs: List[float]) -> float:
        return sum(xs) / len(xs) if xs else 0.0

    return {
        "observed_ppe_jaccard": avg(obs_scores),
        "required_ppe_jaccard": avg(req_scores),
        "worker_compliant_accuracy": avg(comp_scores),
    }


def security_overall_accuracy(pred: Dict[str, Any], gt: Dict[str, Any]) -> float:
    return _eq_ci(pred.get("overall_security"), gt.get("overall_security"))


def security_person_auth_accuracy(pred: Dict[str, Any], gt: Dict[str, Any]) -> float:
    pp = pred.get("persons", [])
    gp = gt.get("persons", [])
    if not isinstance(pp, list) or not isinstance(gp, list):
        return 0.0
    gt_by_id = {p.get("person_id"): p for p in gp if isinstance(p, dict) and p.get("person_id") is not None}
    scores: List[float] = []
    for idx, p in enumerate(pp):
        if not isinstance(p, dict):
            continue
        pid = p.get("person_id")
        gp_match = gt_by_id.get(pid) if pid in gt_by_id else (gp[idx] if idx < len(gp) else None)
        if not isinstance(gp_match, dict):
            continue
        scores.append(_eq_ci(p.get("authorization_assessment"), gp_match.get("authorization_assessment")))
    return sum(scores) / len(scores) if scores else 0.0


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
