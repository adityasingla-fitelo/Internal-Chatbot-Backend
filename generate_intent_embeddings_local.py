import json
import numpy as np
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load intents
with open("intents.json", "r") as f:
    intents = json.load(f)

intent_embeddings = {}

for intent, text in intents.items():
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    intent_embeddings[intent] = response.data[0].embedding

# Save embeddings to JSON
with open("intent_embeddings.json", "w") as f:
    json.dump(intent_embeddings, f)

print("✅ Intent embeddings generated and saved to intent_embeddings.json")
