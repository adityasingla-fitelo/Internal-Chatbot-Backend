import re
from typing import Dict, Optional, Tuple


EMAIL_REGEX = re.compile(
    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
)


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email))


def handle_client_email_update(
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
            "Your client Aditya's registered email is "
            "adityasingla121@gmail.com.\n\n"
            "Do you wish to continue? (Yes / No)",
            "confirm_continue"
        )

    # 3️⃣ Confirm continuation
    if state == "confirm_continue":
        if msg == "no":
            session.clear()
            return (
                None,
                "Thank you. Email update request has been cancelled.",
                "end"
            )

        if msg == "yes":
            session["workflow_state"] = "ask_new_email"
            return (
                session,
                "Please enter the new email address for the client.",
                "ask_new_email"
            )

        return (
            session,
            "Please reply with Yes or No.",
            "confirm_continue"
        )

    # 4️⃣ Validate & update new email
    if state == "ask_new_email":
        new_email = message.strip()

        if not is_valid_email(new_email):
            return (
                session,
                "Invalid email address. Please enter a valid email ID.",
                "ask_new_email"
            )

        session["data"]["new_email"] = new_email
        session["workflow_state"] = "completed"

        return (
            session,
            f"Email address has been successfully updated to {new_email}.\n\n"
            "Is there anything else I can help you with? (Yes / No)",
            "exit_or_restart"
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
