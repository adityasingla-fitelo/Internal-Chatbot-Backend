# approval_store.py
from typing import Dict, List

APPROVALS: List[Dict] = []


def save_approval_request(payload: Dict):
    payload["id"] = len(APPROVALS) + 1
    APPROVALS.append(payload)


def get_all_approvals():
    return APPROVALS


def update_approval_status(approval_id: int, status: str, remarks: str):
    for item in APPROVALS:
        if item["id"] == approval_id:
            item["status"] = status
            item["remarks"] = remarks
            return item
    return None
