from pydantic import BaseModel

class EmbedURLRequest(BaseModel):
    document_id: int
    url: str
