import re
from typing import Dict, Optional, Tuple


def normalize_phone(phone: str) -> Optional[str]:
    phone = phone.strip()

    if not re.search(r"\d", phone):
        return None

    digits = re.sub(r"\D", "", phone)

    # +91XXXXXXXXXX
    if digits.startswith("91") and len(digits) == 12:
        return digits[2:]

    # 0XXXXXXXXXX
    if digits.startswith("0") and len(digits) == 11:
        return digits[1:]

    # XXXXXXXXXX
    if len(digits) == 10:
        return digits

    return None



def handle_app_not_working(
    session: Dict,
    message: str
) -> Tuple[Optional[Dict], str, str]:
    msg = message.strip().lower()
    state = session.get("workflow_state")
    session.setdefault("data", {})

    # 1️⃣ Ask phone number
    if state is None:
        session["workflow_state"] = "ask_phone"
        return session, "Please share your client's phone number.", "ask_phone"

    # 2️⃣ Validate & process phone number
    if state == "ask_phone":
        phone = normalize_phone(message)

        if not phone:
            return (
                session,
                "Invalid phone number. Please enter a valid 10-digit number.",
                "ask_phone"
            )

        session["data"]["phone"] = phone
        session["workflow_state"] = "otp_refreshed"

        return (
            session,
            "OTP limit for your client has been refreshed.\n\n"
            "Is there anything else I can help you with? (Yes / No)",
            "exit_or_restart"
        )

    # 3️⃣ Restart or exit
    if state == "otp_refreshed":
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
                "Alright. Feel free to reach out anytime.",
                "end"
            )

        return (
            session,
            "Please reply with Yes or No.",
            "exit_or_restart"
        )

    # 🧯 Fallback
    session.clear()
    return (
        None,
        "Something went wrong. Let's start again. Please tell me your query.",
        "restart"
    )
