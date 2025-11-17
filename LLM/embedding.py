import requests
from pypdf import PdfReader
import tiktoken


# ============================================================
# CONFIG: Local LLM via OLLAMA
# ============================================================
OLLAMA_EMBEDDING_URL = "http://localhost:11434/api/embeddings"
MODEL_NAME = "nomic-embed-text"


# ============================================================
# TOKEN COUNTER
# ============================================================
def count_tokens(text: str) -> int:
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))


# ============================================================
# READ PDF PER PAGE
# ============================================================
def extract_pages(pdf_path: str):
    try:
        reader = PdfReader(pdf_path)
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        pages.append(text.strip())

    return pages


# ============================================================
# EMBEDDING USING OLLAMA LOCAL MODEL  (FIXED)
# ============================================================
def embedding_local(text: str):
    payload = {
        "model": MODEL_NAME,
        "prompt": text  # Wajib pakai PROMPT, bukan input!
    }

    res = requests.post(OLLAMA_EMBEDDING_URL, json=payload)

    # Debug respons
    print("\nRAW RESPONSE:", res.text[:200])

    if res.status_code != 200:
        raise Exception(f"Embedding error: {res.status_code} → {res.text}")

    data = res.json()

    # Pastikan ada field 'embedding'
    embedding = data.get("embedding", None)

    if embedding is None:
        print("⚠️ WARNING: embedding kosong atau respons tidak sesuai")
        return []

    return embedding  # vector array


# ============================================================
# MAIN: PDF → CHUNKS → EMBEDDINGS
# ============================================================
def generate_document_embeddings(document_id: int, pdf_path: str):
    pages = extract_pages(pdf_path)
    print(f"Found {len(pages)} pages in PDF.")

    results = []

    for page_idx, content in enumerate(pages):
        if not content.strip():
            print(f"Page {page_idx}: empty, skipping...")
            continue

        print(f"\n=== Creating embedding for page {page_idx} ===")

        token_count = count_tokens(content)

        # Generate embedding vector
        vector = embedding_local(content)

        results.append({
            "document_id": document_id,
            "chunk_index": page_idx,
            "content": content,
            "token_count": token_count,
            "embedding": vector
        })

    return results


# ============================================================
# EXAMPLE USAGE
# ============================================================
if __name__ == "__main__":
    document_id = 1
    pdf_path = "tes.pdf"  # Ganti sesuai file PDF

    result = generate_document_embeddings(document_id, pdf_path)

    print("\n=== FINAL RESULT ===")
    for chunk in result:
        print({
            "document_id": chunk["document_id"],
            "chunk_index": chunk["chunk_index"],
            "token_count": chunk["token_count"],
            "embedding_dim": len(chunk["embedding"]),
            "content_preview": chunk["content"][:60] + "..."
        })
