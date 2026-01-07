# approval_store.py
from typing import Dict, List

_APPROVALS: List[Dict] = []

def save_approval_request(payload: Dict):
    payload["id"] = len(_APPROVALS) + 1
    _APPROVALS.append(payload)

def get_all_approvals():
    return _APPROVALS

def update_approval_status(id: int, status: str, remarks: str):
    for item in _APPROVALS:
        if item["id"] == id:
            item["status"] = status
            item["remarks"] = remarks
            return item
    return None
