from pydantic import BaseModel
from backend.database.model import ProductBM

class ProductRanking(BaseModel):
    similarity : float
    product: ProductBM