from intents.pause_facility import handle_pause_facility
from intents.app_not_working import handle_app_not_working
from intents.change_start_date import handle_change_start_date
from intents.client_email_update import handle_client_email_update
from intents.app_stuck_on_logo import handle_app_stuck_on_logo


INTENT_HANDLERS = {
    "pause_facility": handle_pause_facility,
    "app_not_working": handle_app_not_working,
    "change_start_date": handle_change_start_date,
    "client_email_update": handle_client_email_update,
    "app_stuck_on_logo": handle_app_stuck_on_logo,
}

def route_intent(intent, session, message):
    handler = INTENT_HANDLERS.get(intent)

    if not handler:
        session.clear()
        return (
            None,
            "This intent is not supported yet. Please tell me your query again.",
            "restart"
        )

    return handler(session, message)
