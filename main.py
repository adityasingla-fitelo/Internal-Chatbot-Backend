from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware

from embeddings_store import load_intent_embeddings
from intent_matcher import match_intent
from intent_router import route_intent
from session_store import get_session, save_session, clear_session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load precomputed embeddings
intent_embeddings = load_intent_embeddings()


@app.post("/chat")
async def chat(
    session_id: str = Form(...),
    message: str = Form(...)
):
    session = get_session(session_id)
    msg = message.strip().lower()

    # --------------------------------
    # 0️⃣ SAFETY: Ensure required keys
    # --------------------------------
    session.setdefault("pending_intent", None)
    session.setdefault("final_intent", None)
    session.setdefault("awaiting_confirmation", False)
    session.setdefault("workflow_state", None)
    session.setdefault("data", {})

    # --------------------------------
    # 1️⃣ ACTIVE WORKFLOW → ROUTE ONLY
    # --------------------------------
    if session["final_intent"]:
        updated_session, reply, stage = route_intent(
            session["final_intent"],
            session,
            message
        )

        if updated_session is None:
            clear_session(session_id)
        else:
            save_session(session_id, updated_session)

        return {
            "reply": reply,
            "stage": stage
        }

    # --------------------------------
    # 2️⃣ WAITING FOR INTENT CONFIRMATION
    # --------------------------------
    if session["awaiting_confirmation"]:
        if msg == "yes":
            session["final_intent"] = session["pending_intent"]
            session["pending_intent"] = None
            session["awaiting_confirmation"] = False
            save_session(session_id, session)

            # ⬇️ Immediately enter workflow
            updated_session, reply, stage = route_intent(
                session["final_intent"],
                session,
                message=""
            )

            if updated_session:
                save_session(session_id, updated_session)

            return {
                "reply": reply,
                "stage": stage
            }

        if msg == "no":
            clear_session(session_id)
            return {
                "reply": "No problem. Please state your query more clearly.",
                "stage": "rephrase"
            }

        return {
            "reply": "Please reply with Yes or No.",
            "stage": "awaiting_confirmation"
        }

    # --------------------------------
    # 3️⃣ NEW CONVERSATION → DETECT INTENT
    # --------------------------------
    result = match_intent(message, intent_embeddings)

    session["pending_intent"] = result["intent"]
    session["awaiting_confirmation"] = True
    save_session(session_id, session)

    return {
        "reply": (
            f"Thanks for reaching out. I understand your query is regarding "
            f"'{result['intent']}'. Please enter Yes or No."
        ),
        "stage": "intent_confirmation"
    }


