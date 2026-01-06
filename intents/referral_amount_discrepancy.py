import re
import os
from typing import Dict, Optional, Tuple
from utils.send_referral_email import send_referral_email

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"


def is_valid_email(email: str) -> bool:
    return re.match(EMAIL_REGEX, email) is not None


def is_valid_file_ref(msg: str) -> Optional[str]:
    """
    Validates FILE_REF and ensures file exists
    """
    if not msg.startswith("FILE_REF::"):
        return None

    path = msg.replace("FILE_REF::", "").strip()
    if not path or not os.path.exists(path):
        return None

    return path


def handle_referral_amount_discrepancy(
    session: Dict,
    message: str
) -> Tuple[Optional[Dict], str, str]:

    msg = message.strip()
    state = session.get("workflow_state")
    session.setdefault("data", {})

    # 1️⃣ Ask dietician email
    if state is None:
        session["workflow_state"] = "ask_email"
        return (
            session,
            "Please share your valid email ID so we can keep you in the loop.",
            "ask_email"
        )

    # 2️⃣ Validate email
    if state == "ask_email":
        if not is_valid_email(msg):
            return (
                session,
                "Please enter a valid email ID.",
                "ask_email"
            )

        session["data"]["email"] = msg
        session["workflow_state"] = "ask_description"

        return (
            session,
            "Please explain the referral issue in detail so it can be forwarded to the concerned authorities.",
            "ask_description"
        )

    # 3️⃣ Capture issue description
    if state == "ask_description":
        if not msg:
            return (
                session,
                "Please describe the referral issue in detail.",
                "ask_description"
            )

        session["data"]["description"] = msg
        session["workflow_state"] = "ask_payment_screenshot"

        return (
            session,
            "Please upload the payment screenshot. This step is mandatory.",
            "ask_payment_screenshot"
        )

    # 4️⃣ Capture payment screenshot
    if state == "ask_payment_screenshot":
        path = is_valid_file_ref(msg)
        if not path:
            return (
                session,
                "Payment screenshot is mandatory. Please upload the screenshot.",
                "ask_payment_screenshot"
            )

        session["data"]["payment_screenshot"] = path
        session["workflow_state"] = "ask_referral_screenshot"

        return (
            session,
            "Please upload the referral sheet screenshot. This step is mandatory.",
            "ask_referral_screenshot"
        )

    # 5️⃣ Capture referral sheet screenshot
    if state == "ask_referral_screenshot":
        path = is_valid_file_ref(msg)
        if not path:
            return (
                session,
                "Referral sheet screenshot is mandatory. Please upload the screenshot.",
                "ask_referral_screenshot"
            )

        session["data"]["referral_screenshot"] = path

        # 🔔 SEND EMAIL EXACTLY ONCE
        send_referral_email(session["data"])

        # Mark flow complete
        session.clear()

        return (
            None,
            "Your referral issue has been raised with the concerned authorities.\n\n"
            "Thank you.\n\n"
            "Is there anything else I can help you with? (Yes / No)",
            "exit_or_restart"
        )

    # 🧯 Fallback
    session.clear()
    return (
        None,
        "Something went wrong. Let's start again. Please tell me your query.",
        "restart"
    )
