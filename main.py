from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from embeddings_store import load_intent_embeddings
from intent_matcher import match_intent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict later
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load intent embeddings ONCE at startup
intent_embeddings = load_intent_embeddings()

@app.post("/chat")
async def chat_endpoint(message: str = Form(...)):
    result = match_intent(message, intent_embeddings)

    return {
        "reply": "Hi, thanks for reaching out.",
        "detected_intent": result["intent"],
        "confidence": result["confidence"],
        "low_confidence": result["low_confidence"]
    }

