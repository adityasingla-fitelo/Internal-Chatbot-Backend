sessions = {}

def get_session(session_id):
    return sessions.get(session_id, {
        "pending_intent": None,
        "awaiting_confirmation": False,
        "final_intent": None,
        "workflow_state": None,
        "data": {}
    })

def save_session(session_id, session):
    sessions[session_id] = session

def clear_session(session_id):
    sessions.pop(session_id, None)
