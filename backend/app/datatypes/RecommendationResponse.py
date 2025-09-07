from pydantic import BaseModel
from backend.database.model import ProductBM
from typing import List

class RecommendationResponse(BaseModel):
    products : List[ProductBM]
    message: str