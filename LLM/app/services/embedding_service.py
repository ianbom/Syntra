import requests

OLLAMA_URL = "http://localhost:11434/api/embeddings"
MODEL_NAME = "nomic-embed-text"


def embedding_local(text: str):
    payload = {
        "model": MODEL_NAME,
        "prompt": text
    }

    res = requests.post(OLLAMA_URL, json=payload)

    print("\nRAW:", res.text[:150])

    if res.status_code != 200:
        raise Exception(f"Embedding generation failed: {res.text}")

    data = res.json()
    embedding = data.get("embedding", None)

    if embedding is None:
        return []

    return embedding
