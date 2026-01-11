from fastapi import APIRouter, UploadFile, File
from app.services.pdf_downloader import download_pdf
from app.services.grobid_header import extract_header
from app.services.grobid_fulltext import extract_relations
from app.services.metadata_formatter import format_for_database
from app.schemas.extract_url_request import ExtractURLRequest

router = APIRouter()

@router.post("/extract")
async def extract_metadata(pdf: UploadFile = File(...)):
    file_bytes = await pdf.read()
    header = extract_header(file_bytes)
    relations = extract_relations(file_bytes)
    return {
        "filename": pdf.filename,
        "metadata": format_for_database(header, relations)
    }

@router.post("/extract-url")
def extract_from_url(payload: ExtractURLRequest):
    file_bytes = download_pdf(payload.url)

    header = extract_header(file_bytes)
    relations = extract_relations(file_bytes)
    metadata = format_for_database(header, relations)

    return {
        "document_id": payload.document_id,
        "source_url": payload.url,
        "metadata": metadata
    }
