from fastapi import FastAPI, Form, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware

from upload import save_upload
from embeddings_store import load_intent_embeddings
from intent_matcher import match_intent
from intent_router import route_intent
from session_store import get_session, save_session, clear_session
from approval_store import get_all_approvals, update_approval_status

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

intent_embeddings = load_intent_embeddings()

# ================= CHAT =================
@app.post("/chat")
async def chat(session_id: str = Form(...), message: str = Form(...)):
    session = get_session(session_id)
    msg = message.strip().lower()

    session.setdefault("pending_intent", None)
    session.setdefault("final_intent", None)
    session.setdefault("awaiting_confirmation", False)
    session.setdefault("workflow_state", None)
    session.setdefault("data", {})

    # 🔥 ACTIVE WORKFLOW
    if session["final_intent"]:
        updated_session, reply, stage = route_intent(
            session["final_intent"], session, message
        )

        if updated_session is None:
            clear_session(session_id)
        else:
            save_session(session_id, updated_session)

        return {"reply": reply, "stage": stage}

    # 🔥 INTENT CONFIRMATION
    if session["awaiting_confirmation"]:
        if msg == "yes":
            session["final_intent"] = session["pending_intent"]
            session["pending_intent"] = None
            session["awaiting_confirmation"] = False

            # 🔥 CRITICAL RESET
            session["workflow_state"] = None
            session["data"] = {}

            save_session(session_id, session)

            updated_session, reply, stage = route_intent(
                session["final_intent"], session, ""
            )

            if updated_session:
                save_session(session_id, updated_session)

            return {"reply": reply, "stage": stage}

        if msg == "no":
            clear_session(session_id)
            return {"reply": "Please rephrase your query.", "stage": "restart"}

        return {"reply": "Reply Yes or No.", "stage": "awaiting_confirmation"}

    # 🔍 INTENT DETECTION
    result = match_intent(message, intent_embeddings)
    session["pending_intent"] = result["intent"]
    session["awaiting_confirmation"] = True
    save_session(session_id, session)

    return {
        "reply": f"I understand your query is regarding '{result['intent']}'. Should I proceed? (Yes / No)",
        "stage": "intent_confirmation"
    }


# ================= FILE UPLOAD =================
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    path = await save_upload(file)
    return {"file_path": path}


# ================= APPROVAL APIs =================
@app.get("/approvals")
def get_approvals():
    return get_all_approvals()


@app.post("/approvals/update")
def update_approval(payload: dict = Body(...)):
    updated = update_approval_status(
        payload["id"],
        payload["status"],
        payload.get("remarks", "")
    )
    return {"success": True, "data": updated}
