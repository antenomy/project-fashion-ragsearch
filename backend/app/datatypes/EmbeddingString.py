from pydantic import BaseModel

class EmbeddingString(BaseModel):
    input: str