from datetime import datetime
from typing import Dict, Optional, Tuple
from approval_store import save_approval_request


AVAILABLE_PAUSE_DAYS = 5  # 🔥 TEMP (can be fetched later)


def handle_add_pause_days(
    session: Dict,
    message: str
) -> Tuple[Optional[Dict], str, str]:

    msg = message.strip().lower()
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
        session["data"]["phone"] = message.strip()
        session["workflow_state"] = "confirm_continue"

        return (
            session,
            f"Client Aditya has {AVAILABLE_PAUSE_DAYS} pause days available.\n\n"
            "Do you wish to continue? (Yes / No)",
            "confirm_continue"
        )

    # 3️⃣ Confirmation
    if state == "confirm_continue":
        if msg == "no":
            session.clear()
            return (
                None,
                "Okay, the request has been cancelled.\n\n"
                "Is there anything else I can help you with? (Yes / No)",
                "exit_or_restart"
            )

        if msg == "yes":
            session["workflow_state"] = "ask_reason"
            return (
                session,
                "Please mention the reason for adding pause days.",
                "ask_reason"
            )

        return (
            session,
            "Please reply with Yes or No.",
            "confirm_continue"
        )

    # 4️⃣ Capture reason → ask pause days count
    if state == "ask_reason":
        if not message.strip():
            return (
                session,
                "Please provide a valid reason for adding pause days.",
                "ask_reason"
            )

        session["data"]["reason"] = message.strip()
        session["workflow_state"] = "ask_pause_days"

        return (
            session,
            "Please enter the number of pause days to be added.",
            "ask_pause_days"
        )

    # 5️⃣ Capture pause days → raise approval
    if state == "ask_pause_days":
        try:
            pause_days = int(message.strip())

            if pause_days <= 0:
                raise ValueError

            approval_request = {
                "client_name": "Aditya",  # 🔥 temp
                "contact": session["data"]["phone"],
                "request_type": "Add Pause Days",
                "order_by": "Abhishek",
                "approval_owner": "Aayush",
                "reason": session["data"]["reason"],
                "pause_days_requested": pause_days,
                "status": "Pending",
                "remarks": "",
                "created_at": datetime.utcnow().isoformat()
            }

            save_approval_request(approval_request)

            session.clear()
            return (
                None,
                "Your request has been raised to the concerned authorities.\n\n"
                "You can check the approval status below.",
                "show_approval_status_button"
            )

        except ValueError:
            return (
                session,
                "Please enter a valid number of pause days.",
                "ask_pause_days"
            )

    # 🧯 Fallback
    session.clear()
    return (
        None,
        "Something went wrong. Let's start again. Please tell me your query.",
        "restart"
    )
