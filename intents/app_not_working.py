import re
from typing import Tuple, Optional, Dict

def normalize_phone(phone: str) -> Optional[str]:
    digits = re.sub(r"\D", "", phone)

    if digits.startswith("91") and len(digits) == 12:
        return digits[2:]
    if digits.startswith("0") and len(digits) == 11:
        return digits[1:]
    if len(digits) == 10:
        return digits

    return None


def handle_app_not_working(
    session: Dict,
    message: str
) -> Tuple[Optional[Dict], str]:
    msg = message.strip().lower()
    state = session.get("workflow_state")

    if state is None:
        session["workflow_state"] = "ask_phone"
        return session, "Please share your client's phone number."

    if state == "ask_phone":
        phone = normalize_phone(message)

        if not phone:
            return session, "Invalid phone number. Please enter a valid 10-digit number."

        session["data"]["phone"] = phone
        session["workflow_state"] = "otp_refreshed"

        return session, (
            "OTP limit for your client has been refreshed.\n\n"
            "Is there anything else I can help you with? (Yes / No)"
        )

    if state == "otp_refreshed":
        if msg == "yes":
            session["workflow_state"] = None
            session["final_intent"] = None
            session["data"] = {}
            return session, "Sure. Please tell me your query."

        if msg == "no":
            return None, "Alright. Feel free to reach out anytime."

        return session, "Please reply with Yes or No."

    return None, "Something went wrong."
