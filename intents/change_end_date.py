from datetime import datetime
from typing import Dict, Optional, Tuple
from approval_store import save_approval_request


def handle_change_end_date(
    session: Dict,
    message: str
) -> Tuple[Optional[Dict], str, str]:

    msg = message.strip()
    state = session.get("workflow_state")
    session.setdefault("data", {})

    # 1️⃣ Ask for client phone number
    if state is None:
        session["workflow_state"] = "ask_phone"
        return (
            session,
            "Please share the client's phone number.",
            "ask_phone"
        )

    # 2️⃣ Capture phone number → ask reason
    if state == "ask_phone":
        session["data"]["phone"] = msg
        session["workflow_state"] = "ask_reason"
        return (
            session,
            "Please mention the reason for changing the end date.",
            "ask_reason"
        )

    # 3️⃣ Capture reason → ask new end date
    if state == "ask_reason":
        session["data"]["reason"] = msg
        session["workflow_state"] = "ask_new_date"
        return (
            session,
            "Please select the new end date using the calendar.",
            "ask_single_date"
        )

    # 4️⃣ Capture new end date → raise approval request
    if state == "ask_new_date":
        try:
            new_end_date = datetime.strptime(msg, "%Y-%m-%d").date()

            save_approval_request({
                "client_name": "Aditya",
                "contact": session["data"]["phone"],
                "request_type": "Change of End Date",
                "order_by": "Abhishek",
                "approval_owner": "Aayush",
                "reason": session["data"]["reason"],
                "new_end_date": str(new_end_date),
                "status": "Pending",
                "remarks": "",
                "created_at": datetime.utcnow().isoformat()
            })

            session.clear()
            return (
                None,
                "Your request has been raised.\n\n"
                "You can check the approval status below.",
                "show_approval_status_button"
            )

        except ValueError:
            return (
                session,
                "Invalid date selected. Please choose again using the calendar.",
                "ask_single_date"
            )

    # 🧯 Safety fallback
    session.clear()
    return (
        None,
        "Something went wrong. Let's start again.",
        "restart"
    )
