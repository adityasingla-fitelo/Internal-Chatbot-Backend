# approval_store.py
from typing import Dict, List

# 🔥 SINGLE IN-MEMORY STORE (TEMP)
_APPROVALS: List[Dict] = []


def save_approval_request(payload: Dict):
    payload["id"] = len(_APPROVALS) + 1

    # Ensure all optional fields exist
    payload.setdefault("status", "Pending")
    payload.setdefault("remarks", "")
    payload.setdefault("reason", "")
    payload.setdefault("requested_plan", None)
    payload.setdefault("pause_days_requested", None)

    _APPROVALS.append(payload)
    return payload


def get_all_approvals():
    # Return COPY to avoid mutation issues
    return [dict(item) for item in _APPROVALS]


def update_approval_status(id: int, status: str, remarks: str):
    for item in _APPROVALS:
        if item["id"] == id:
            item["status"] = status
            item["remarks"] = remarks
            return item
    return None
