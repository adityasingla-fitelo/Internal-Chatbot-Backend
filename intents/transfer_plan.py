from datetime import datetime
from typing import Dict, Optional, Tuple
from approval_store import save_approval_request


def handle_transfer_plan(
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

    # 2️⃣ Capture phone → confirm continuation
    if state == "ask_phone":
        session["data"]["phone"] = msg
        session["workflow_state"] = "confirm_continue"

        return (
            session,
            "Your client Aditya is currently enrolled in a 4 Weeks Fitness Plan.\n\n"
            "Do you wish to continue? (Yes / No)",
            "confirm_continue"
        )

    # 3️⃣ Confirm continuation
    if state == "confirm_continue":
        if msg.lower() == "no":
            session.clear()
            return (
                None,
                "Okay, the request has been cancelled.\n\n"
                "Is there anything else I can help you with? (Yes / No)",
                "exit_or_restart"
            )

        if msg.lower() == "yes":
            session["workflow_state"] = "ask_new_plan"
            return (
                session,
                "Please mention the new plan name the client wants to switch to.",
                "ask_new_plan"
            )

        return (
            session,
            "Please reply with Yes or No.",
            "confirm_continue"
        )

    # 4️⃣ Capture new plan name
    if state == "ask_new_plan":
        session["data"]["new_plan"] = msg
        session["workflow_state"] = "ask_reason"

        return (
            session,
            "Please mention the reason for changing the plan.",
            "ask_reason"
        )

    # 5️⃣ Capture reason → raise approval
    if state == "ask_reason":
        session["data"]["reason"] = msg

        save_approval_request({
            "client_name": "Aditya",
            "contact": session["data"]["phone"],
            "request_type": "Transfer Plan",
            "requested_plan": session["data"]["new_plan"],  # 🔥 KEY FIELD
            "order_by": "Abhishek",
            "approval_owner": "Aayush",
            "reason": session["data"]["reason"],
            "status": "Pending",
            "remarks": "",
            "created_at": datetime.utcnow().isoformat()
        })

        session.clear()

        return (
            None,
            "Your request has been raised with the concerned authorities.\n\n"
            "You can check the approval status below.",
            "show_approval_status_button"
        )

    # 🧯 Safety fallback
    session.clear()
    return (
        None,
        "Something went wrong. Let's start again. Please tell me your query.",
        "restart"
    )
