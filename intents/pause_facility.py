from datetime import datetime

AVAILABLE_PAUSE_DAYS = 30

def handle_pause_facility(session, message):
    msg = message.strip().lower()
    state = session.get("workflow_state")

    # 1️⃣ Ask phone number
    if state is None:
        session["workflow_state"] = "ask_phone"
        return session, "Please share your client's phone number."

    if state == "ask_phone":
        session["data"]["phone"] = message.strip()
        session["workflow_state"] = "confirm_days"
        return session, (
            "Client Aditya has 30 pause days available. "
            "Do you wish to continue? (Yes / No)"
        )

    if state == "confirm_days":
        if msg == "no":
            return None, "Okay, pause request cancelled."

        if msg == "yes":
            session["workflow_state"] = "ask_start_date"
            return session, "Please enter pause start date (YYYY-MM-DD)."

        return session, "Please reply with Yes or No."

    if state == "ask_start_date":
        try:
            session["data"]["start_date"] = datetime.strptime(message, "%Y-%m-%d").date()
            session["workflow_state"] = "ask_end_date"
            return session, "Please enter pause end date (YYYY-MM-DD)."
        except ValueError:
            return session, "Invalid date format. Use YYYY-MM-DD."

    if state == "ask_end_date":
        try:
            end_date = datetime.strptime(message, "%Y-%m-%d").date()
            start_date = session["data"]["start_date"]

            days = (end_date - start_date).days + 1
            if days > AVAILABLE_PAUSE_DAYS:
                return None, "Sorry, your requested pause days exceed the available quota."

            return None, (
                f"Your client's subscription has been paused "
                f"from {start_date} to {end_date}."
            )
        except ValueError:
            return session, "Invalid date format. Use YYYY-MM-DD."

    return None, "Something went wrong."
