from datetime import datetime
from typing import Dict, Optional, Tuple
from approval_store import save_approval_request


def handle_change_start_date(
    session: Dict,
    message: str
) -> Tuple[Optional[Dict], str, str]:

    msg = message.strip()
    state = session.get("workflow_state")
    session.setdefault("data", {})

    if state is None:
        session["workflow_state"] = "ask_phone"
        return session, "Please share the client's phone number.", "ask_phone"

    if state == "ask_phone":
        session["data"]["phone"] = msg
        session["workflow_state"] = "ask_reason"
        return session, "Please mention the reason for changing the start date.", "ask_reason"

    if state == "ask_reason":
        session["data"]["reason"] = msg
        session["workflow_state"] = "ask_new_date"
        return session, "Please select the new start date using the calendar.", "ask_single_date"

    if state == "ask_new_date":
        new_start_date = datetime.strptime(msg, "%Y-%m-%d").date()

        save_approval_request({
            "client_name": "Aditya",
            "contact": session["data"]["phone"],
            "request_type": "Change of Start Date",
            "order_by": "Abhishek",
            "approval_owner": "Aayush",
            "reason": session["data"]["reason"],
            "new_start_date": str(new_start_date),
            "status": "Pending",
            "remarks": "",
            "created_at": datetime.utcnow().isoformat()
        })

        session.clear()
        return (
            None,
            "Your request has been raised.\n\nYou can check the approval status below.",
            "show_approval_status_button"
        )
