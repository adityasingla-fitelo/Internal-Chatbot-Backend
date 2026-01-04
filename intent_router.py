from intents.pause_facility import handle_pause_facility
from intents.app_not_working import handle_app_not_working

INTENT_HANDLERS = {
    "pause_facility": handle_pause_facility,
    "app_not_working": handle_app_not_working
}

def route_intent(intent, session, message):
    handler = INTENT_HANDLERS.get(intent)
    if not handler:
        return None, "This intent is not supported yet."

    return handler(session, message)
