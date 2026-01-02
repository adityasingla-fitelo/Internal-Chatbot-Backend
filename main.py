from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from embeddings_store import generate_intent_embeddings
from intent_matcher import match_intent
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 This runs ONCE when Render starts the service
intent_embeddings = generate_intent_embeddings()

@app.post("/chat")
async def chat_endpoint(message: str = Form(...)):
    result = match_intent(message, intent_embeddings)

    return {
        "reply": "Hi, thanks for reaching out.",
        "detected_intent": result["intent"],
        "confidence": result["confidence"]
    }
