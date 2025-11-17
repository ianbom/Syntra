from fastapi import FastAPI
from app.routers import extract

app = FastAPI(title="Syntra GROBID Service")

app.include_router(extract.router)

@app.get("/")
def home():
    return {"message": "Syntra GROBID API is running"}
