import requests
from fastapi import HTTPException

def download_pdf(url: str) -> bytes:
    try:
        res = requests.get(url, timeout=15)
        if res.status_code != 200:
            raise HTTPException(400, f"Failed to download PDF: {res.status_code}")
        return res.content
    except Exception as e:
        raise HTTPException(400, f"Error downloading PDF: {str(e)}")
