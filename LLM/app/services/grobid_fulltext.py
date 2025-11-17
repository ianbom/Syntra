import requests
from lxml import etree
from fastapi import HTTPException
from app.config import GROBID_URL_FULLTEXT

def extract_relations(file_bytes: bytes):
    response = requests.post(
        GROBID_URL_FULLTEXT,
        files={'input': ("doc.pdf", file_bytes)},
        headers={'Accept': 'application/xml'},
        timeout=25
    )

    if response.status_code != 200:
        return []

    try:
        root = etree.fromstring(response.text.encode("utf-8"))
    except:
        return []

    ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    return root.xpath("//tei:listBibl//tei:title/text()", namespaces=ns)
