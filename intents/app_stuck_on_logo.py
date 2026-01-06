from typing import Dict, Optional, Tuple
import re


def normalize_phone(phone: str) -> Optional[str]:
    phone = phone.strip()
    if not re.search(r"\d", phone):
        return None

    digits = re.sub(r"\D", "", phone)

    if digits.startswith("91") and len(digits) == 12:
        return digits[2:]
    if digits.startswith("0") and len(digits) == 11:
        return digits[1:]
    if len(digits) == 10:
        return digits

    return None


def handle_app_stuck_on_logo(
    session: Dict,
    message: str
) -> Tuple[Optional[Dict], str, str]:

    msg = message.strip().lower()
    state = session.get("workflow_state")
    session.setdefault("data", {})

    # 1️⃣ Apology + troubleshooting steps
    if state is None:
        session["workflow_state"] = "await_fix_confirmation"

        return (
            session,
            (
                "Sorry to hear that your client is facing this issue.\n\n"
                "Please ask your client to try the following steps one by one:\n\n"
                "1. Clear App Cache:\n"
                "   - Go to Phone Settings\n"
                "   - Open Apps\n"
                "   - Select Fitelo App\n"
                "   - Tap on Storage\n"
                "   - Clear Cache\n\n"
                "2. Uninstall and Reinstall the App:\n"
                "   - Uninstall the Fitelo app\n"
                "   - Restart the phone\n"
                "   - Reinstall the app from Play Store or App Store\n\n"
                "3. Restart the Phone:\n"
                "   - A simple restart can often fix stuck loading issues\n\n"
                "Once these steps are completed, please confirm:\n"
                "Is the app working now? (Yes / No)"
            ),
            "confirm_fix"
        )


    # 2️⃣ Check if issue resolved
    if state == "await_fix_confirmation":
        if msg == "yes":
            session.clear()
            return (
                None,
                "Great! Glad to hear the app is working now. 😊\n\nHave a nice day!",
                "end"
            )

        if msg == "no":
            session["workflow_state"] = "ask_phone"
            return (
                session,
                "Thanks for confirming. Please share your client's phone number so that we can raise a ticket with the tech support team.",
                "ask_phone"
            )

        return (
            session,
            "Please reply with Yes or No.",
            "confirm_fix"
        )

    # 3️⃣ Capture phone number & raise ticket
    if state == "ask_phone":
        phone = normalize_phone(message)

        if not phone:
            return (
                session,
                "Invalid phone number. Please enter a valid 10-digit numeric phone number.",
                "ask_phone"
            )

        session["data"]["phone"] = phone
        session["workflow_state"] = "ticket_raised"

        return (
            session,
            (
                "Thank you. A ticket has been successfully raised with the tech support team "
                "for your client. Our team will look into this on priority.\n\n"
                "Is there anything else I can help you with? (Yes / No)"
            ),
            "exit_or_restart"
        )

    # 4️⃣ Restart or exit
    if state == "ticket_raised":
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
                "Thank you for reaching out. Have a nice day! 😊",
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
