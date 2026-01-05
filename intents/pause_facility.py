from datetime import datetime

AVAILABLE_PAUSE_DAYS = 30


def handle_pause_facility(session, message):
    msg = message.strip().lower()
    state = session.get("workflow_state")
    session.setdefault("data", {})

    # 1️⃣ Ask for phone number
    if state is None:
        session["workflow_state"] = "ask_phone"
        return session, {
            "reply": "Please share your client's phone number.",
            "stage": "ask_phone"
        }

    # 2️⃣ Capture phone number
    if state == "ask_phone":
        session["data"]["phone"] = message.strip()
        session["workflow_state"] = "confirm_days"

        return session, {
            "reply": (
                "Client Aditya has 30 pause days available. "
                "Do you wish to continue? (Yes / No)"
            ),
            "stage": "confirm_days"
        }

    # 3️⃣ Confirm continuation
    if state == "confirm_days":
        if msg == "no":
            session.clear()
            return session, {
                "reply": (
                    "Okay, pause request cancelled.\n\n"
                    "Is there anything else I can help you with? (Yes / No)"
                ),
                "stage": "exit_or_restart"
            }

        if msg == "yes":
            session["workflow_state"] = "ask_dates"
            return session, {
                "reply": "Please select pause start date and end date using the calendar.",
                "stage": "ask_dates"   # 🔥 frontend will show calendar
            }

        return session, {
            "reply": "Please reply with Yes or No.",
            "stage": "confirm_days"
        }

    # 4️⃣ Handle calendar date selection
    if state == "ask_dates":
        try:
            # Expected format: YYYY-MM-DD|YYYY-MM-DD
            start_str, end_str = message.split("|")

            start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_str, "%Y-%m-%d").date()

            if end_date < start_date:
                return session, {
                    "reply": "End date cannot be before start date. Please select again.",
                    "stage": "ask_dates"
                }

            days = (end_date - start_date).days + 1

            if days > AVAILABLE_PAUSE_DAYS:
                session.clear()
                return session, {
                    "reply": (
                        "Sorry, your requested pause days exceed the available quota.\n\n"
                        "Is there anything else I can help you with? (Yes / No)"
                    ),
                    "stage": "exit_or_restart"
                }

            session["workflow_state"] = "completed"
            session["data"]["start_date"] = start_date
            session["data"]["end_date"] = end_date

            return session, {
                "reply": (
                    f"Your client's subscription has been paused "
                    f"from {start_date} to {end_date}.\n\n"
                    "Is there anything else I can help you with? (Yes / No)"
                ),
                "stage": "exit_or_restart"
            }

        except Exception:
            return session, {
                "reply": "Invalid date selection. Please try again using the calendar.",
                "stage": "ask_dates"
            }

    # 5️⃣ Restart intent identification or exit
    if state == "completed":
        if msg == "yes":
            session.clear()
            return session, {
                "reply": "Sure. Please tell me your query.",
                "stage": "restart"
            }

        if msg == "no":
            session.clear()
            return session, {
                "reply": "Have a nice day! 😊",
                "stage": "end"
            }

        return session, {
            "reply": "Please reply with Yes or No.",
            "stage": "exit_or_restart"
        }

    # Fallback
    session.clear()
    return session, {
        "reply": "Something went wrong. Let's start again. Please tell me your query.",
        "stage": "restart"
    }
