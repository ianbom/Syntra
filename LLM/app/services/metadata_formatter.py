from datetime import datetime

def format_for_database(md, relations):
    authors = md.get("authors", [])
    keywords = md.get("keywords", [])

    creator = authors[0] if authors else None
    contributor = ", ".join(authors[1:]) if len(authors) > 1 else None

    # Format date
    raw_date = md.get("publication_date")
    date_iso = None
    if raw_date:
        for fmt in ["%d %B %Y", "%Y", "%Y-%m-%d"]:
            try:
                date_iso = datetime.strptime(raw_date, fmt).isoformat()
                break
            except:
                continue

    return {
        "title": md.get("title"),
        "creator": creator,
        "keywords": ", ".join(keywords) if keywords else None,
        "description": md.get("abstract"),
        "publisher": md.get("publisher"),
        "contributor": contributor,
        "date": date_iso,
        "type": "Text",
        "format": "application/pdf",
        "identifier": md.get("doi"),
        "source": md.get("journal"),
        "language": "en",
        "relation": ", ".join(relations) if relations else None,
        "coverage": "global",
        "rights": f"Copyright © {md.get('publisher')}" if md.get("publisher") else None,
        "doi": md.get("doi"),
        "abstract": md.get("abstract"),
        "citation_count": len(relations)
    }
