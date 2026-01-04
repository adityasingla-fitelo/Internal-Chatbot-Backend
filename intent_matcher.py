import numpy as np
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def match_intent(query, intent_embeddings, low_conf_threshold=0.65):
    """
    Always returns the closest intent.
    Marks low confidence instead of returning 'unknown'.
    """

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    query_embedding = np.array(response.data[0].embedding)

    best_intent = None
    best_score = -1.0

    for intent, emb in intent_embeddings.items():
        score = cosine_similarity(query_embedding, emb)
        if score > best_score:
            best_score = score
            best_intent = intent

    confidence = round(best_score, 3)

    return {
        "intent": best_intent,
        "confidence": confidence,
        "low_confidence": confidence < low_conf_threshold
    }
