from intents.pause_facility import handle_pause_facility
from intents.app_not_working import handle_app_not_working
from intents.change_start_date import handle_change_start_date
from intents.client_email_update import handle_client_email_update
from intents.app_stuck_on_logo import handle_app_stuck_on_logo
from intents.sales_amount_discrepancy import handle_sales_amount_discrepancy
from intents.referral_amount_discrepancy import handle_referral_amount_discrepancy


INTENT_HANDLERS = {
    "pause_facility": handle_pause_facility,
    "app_not_working": handle_app_not_working,
    "change_start_date": handle_change_start_date,
    "client_email_update": handle_client_email_update,
    "app_stuck_on_logo": handle_app_stuck_on_logo,
    "sales_amount_discrepancy": handle_sales_amount_discrepancy,
    "referral_amount_discrepancy": handle_referral_amount_discrepancy,
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
