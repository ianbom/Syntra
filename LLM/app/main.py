from fastapi import FastAPI
from app.routers import extract
from app.routers.embeddings import router as embedding_router

app = FastAPI(title="Syntra GROBID Service")

app.include_router(extract.router, prefix="/api", tags=["Extraction"])
app.include_router(embedding_router, prefix="/api", tags=["Embeddings"])

@app.get("/")
def home():
    return {"message": "Syntra GROBID API is running"}
