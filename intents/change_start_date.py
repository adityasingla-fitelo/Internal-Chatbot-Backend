from datetime import datetime
from typing import Dict, Optional, Tuple


def handle_change_start_date(
    session: Dict,
    message: str
) -> Tuple[Optional[Dict], str, str]:
    msg = message.strip().lower()
    state = session.get("workflow_state")
    session.setdefault("data", {})

    # 1️⃣ Ask for phone number
    if state is None:
        session["workflow_state"] = "ask_phone"
        return (
            session,
            "Please share your client's phone number.",
            "ask_phone"
        )

    # 2️⃣ Capture phone number
    if state == "ask_phone":
        session["data"]["phone"] = message.strip()
        session["workflow_state"] = "confirm_continue"

        return (
            session,
            "Your client Aditya is associated with a 3-Month Weight Loss program "
            "starting from 31-01-2026.\n\n"
            "Do you wish to continue? (Yes / No)",
            "confirm_continue"
        )

    # 3️⃣ Confirm continuation
    if state == "confirm_continue":
        if msg == "no":
            session.clear()
            return (
                None,
                "Thank you. The request has been cancelled.",
                "end"
            )

        if msg == "yes":
            session["workflow_state"] = "ask_new_date"
            return (
                session,
                "Please select the new start date using the calendar.",
                "ask_single_date"   # 🔥 frontend renders single-date calendar
            )

        return (
            session,
            "Please reply with Yes or No.",
            "confirm_continue"
        )

    # 4️⃣ Handle calendar date (single date)
    if state == "ask_new_date":
        try:
            # message = YYYY-MM-DD
            new_start_date = datetime.strptime(message, "%Y-%m-%d").date()

            session["data"]["new_start_date"] = new_start_date
            session["workflow_state"] = "completed"

            return (
                session,
                f"Start date has been successfully updated to {new_start_date}.\n\n"
                "Is there anything else I can help you with? (Yes / No)",
                "exit_or_restart"
            )

        except ValueError:
            return (
                session,
                "Invalid date selected. Please choose a valid date using the calendar.",
                "ask_single_date"
            )

    # 5️⃣ Restart or exit
    if state == "completed":
        if msg == "yes":
            session.clear()
            return (
                None,
                "Sure. Please tell me your query.",
                "restart"
            )

        if msg == "no":
            session.clear()
            return (
                None,
                "Have a great day! 😊",
                "end"
            )

        return (
            session,
            "Please reply with Yes or No.",
            "exit_or_restart"
        )

    # 🧯 Fallback safety
    session.clear()
    return (
        None,
        "Something went wrong. Let's start again. Please tell me your query.",
        "restart"
    )
