import json
import numpy as np
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


intent_embeddings = {}

def load_intents():
    with open("intents.json", "r") as f:
        return json.load(f)

def generate_intent_embeddings():
    global intent_embeddings

    intents = load_intents()

    for intent, text in intents.items():
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        intent_embeddings[intent] = np.array(response.data[0].embedding)

    return intent_embeddings
