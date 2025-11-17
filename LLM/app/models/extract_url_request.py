from pydantic import BaseModel

class ExtractURLRequest(BaseModel):
    document_id: int
    url: str
