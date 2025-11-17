import requests
from lxml import etree
from fastapi import HTTPException
from app.config import GROBID_URL_HEADER

def extract_header(file_bytes: bytes):
    response = requests.post(
        GROBID_URL_HEADER,
        files={'input': ("doc.pdf", file_bytes)},
        data={'consolidateHeader': 1},
        headers={'Accept': 'application/xml'},
        timeout=25
    )

    if response.status_code != 200:
        raise HTTPException(500, "GROBID header extraction failed")

    try:
        root = etree.fromstring(response.text.encode("utf-8"))
    except:
        raise HTTPException(500, "Invalid XML returned by GROBID")

    ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    title = root.xpath("//tei:titleStmt/tei:title/text()", namespaces=ns)
    authors_xml = root.xpath("//tei:author/tei:persName", namespaces=ns)

    authors = []
    for a in authors_xml:
        fn = "".join(a.xpath("tei:forename/text()", namespaces=ns)) or ""
        ln = "".join(a.xpath("tei:surname/text()", namespaces=ns)) or ""
        full = (fn + " " + ln).strip()
        if full:
            authors.append(full)

    return {
        "title": title[0] if title else None,
        "authors": authors,
        "doi": root.xpath("//tei:idno[@type='DOI']/text()", namespaces=ns)[0] if root.xpath("//tei:idno[@type='DOI']/text()", namespaces=ns) else None,
        "publication_date": root.xpath("//tei:date/text()", namespaces=ns)[0] if root.xpath("//tei:date/text()", namespaces=ns) else None,
        "publisher": root.xpath("//tei:publicationStmt/tei:publisher/text()", namespaces=ns)[0] if root.xpath("//tei:publicationStmt/tei:publisher/text()", namespaces=ns) else None,
        "journal": root.xpath("//tei:sourceDesc//tei:title/text()", namespaces=ns)[0] if root.xpath("//tei:sourceDesc//tei:title/text()", namespaces=ns) else None,
        "abstract": root.xpath("//tei:profileDesc/tei:abstract/tei:p/text()", namespaces=ns)[0] if root.xpath("//tei:profileDesc/tei:abstract/tei:p/text()", namespaces=ns) else None,
        "keywords": root.xpath("//tei:keywords//tei:term/text()", namespaces=ns)
    }
