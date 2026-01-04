import json
import numpy as np

def load_intent_embeddings():
    """
    Loads precomputed intent embeddings from JSON
    """
    with open("intent_embeddings.json", "r") as f:
        raw_embeddings = json.load(f)

    # Convert lists → numpy arrays
    intent_embeddings = {
        intent: np.array(vector)
        for intent, vector in raw_embeddings.items()
    }

    return intent_embeddings
