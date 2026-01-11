from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_service import extract_pages
from app.services.embedding_service import embedding_local
from app.utils.token_utils import count_tokens
from app.schemas.embed_request import EmbedURLRequest
import requests

router = APIRouter()


@router.post("/embed-pdf")
async def embed_pdf(document_id: int, pdf: UploadFile = File(...)):
    file_bytes = await pdf.read()

    temp_path = "temp_uploaded.pdf"
    with open(temp_path, "wb") as f:
        f.write(file_bytes)

    pages = extract_pages(temp_path)

    results = []
    for page_idx, content in enumerate(pages):
        if not content.strip():
            continue

        token_count = count_tokens(content)
        vector = embedding_local(content)

        results.append({
            "document_id": document_id,
            "chunk_index": page_idx,
            "content": content,
            "token_count": token_count,
            "embedding_dim": len(vector),
            "embedding": vector
        })

    return {"message": "success", "chunks": results}


# ================================================================
#   FIXED embed-url → gunakan body JSON (document_id + url)
# ================================================================
@router.post("/embed-url")
async def embed_url(body: EmbedURLRequest):
    document_id = body.document_id
    url = body.url

    try:
        res = requests.get(url, timeout=15)
        if res.status_code != 200:
            raise HTTPException(400, "Failed to download PDF")
    except:
        raise HTTPException(400, "Invalid URL or unreachable")

    temp_path = "temp_downloaded.pdf"
    with open(temp_path, "wb") as f:
        f.write(res.content)

    pages = extract_pages(temp_path)

    results = []
    for page_idx, content in enumerate(pages):
        if not content.strip():
            continue

        token_count = count_tokens(content)
        vector = embedding_local(content)

        results.append({
            "document_id": document_id,
            "chunk_index": page_idx,
            "content": content,
            "token_count": token_count,
            "embedding_dim": len(vector),
            "embedding": vector
        })

    return {"message": "success", "chunks": results}
