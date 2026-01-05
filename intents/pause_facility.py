from datetime import datetime

AVAILABLE_PAUSE_DAYS = 30


def handle_pause_facility(session, message):
    msg = message.strip().lower()
    state = session.get("workflow_state")
    session.setdefault("data", {})

    # 1️⃣ Ask for phone number
    if state is None:
        session["workflow_state"] = "ask_phone"
        return session, "Please share your client's phone number.", "ask_phone"

    # 2️⃣ Capture phone number
    if state == "ask_phone":
        session["data"]["phone"] = message.strip()
        session["workflow_state"] = "confirm_days"

        return (
            session,
            "Client Aditya has 30 pause days available. "
            "Do you wish to continue? (Yes / No)",
            "confirm_days"
        )

    # 3️⃣ Confirm continuation
    if state == "confirm_days":
        if msg == "no":
            session.clear()
            return (
                None,
                "Okay, pause request cancelled.\n\n"
                "Is there anything else I can help you with? (Yes / No)",
                "exit_or_restart"
            )

        if msg == "yes":
            session["workflow_state"] = "ask_dates"
            return (
                session,
                "Please select pause start date and end date using the calendar.",
                "ask_dates"  # 🔥 frontend renders calendar
            )

        return session, "Please reply with Yes or No.", "confirm_days"

    # 4️⃣ Handle calendar date selection
    if state == "ask_dates":
        try:
            # Expected format: YYYY-MM-DD|YYYY-MM-DD
            start_str, end_str = message.split("|")

            start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_str, "%Y-%m-%d").date()

            if end_date < start_date:
                return (
                    session,
                    "End date cannot be before start date. Please select again.",
                    "ask_dates"
                )

            days = (end_date - start_date).days + 1

            if days > AVAILABLE_PAUSE_DAYS:
                session.clear()
                return (
                    None,
                    "Sorry, your requested pause days exceed the available quota.\n\n"
                    "Is there anything else I can help you with? (Yes / No)",
                    "exit_or_restart"
                )

            session["workflow_state"] = "completed"
            session["data"]["start_date"] = start_date
            session["data"]["end_date"] = end_date

            return (
                session,
                f"Your client's subscription has been paused "
                f"from {start_date} to {end_date}.\n\n"
                "Is there anything else I can help you with? (Yes / No)",
                "exit_or_restart"
            )

        except Exception:
            return (
                session,
                "Invalid date selection. Please try again using the calendar.",
                "ask_dates"
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
                "Have a nice day! 😊",
                "end"
            )

        return session, "Please reply with Yes or No.", "exit_or_restart"

    # 🧯 Fallback (never crash)
    session.clear()
    return (
        None,
        "Something went wrong. Let's start again. Please tell me your query.",
        "restart"
    )
