from pydantic import BaseModel, Field, ConfigDict
from backend.database.model import ProductBM

from backend.database.model import Product
from typing import List


class Outfit(BaseModel):
    model_config = ConfigDict(extra='allow')

    clothing_types: List[str] = Field(default_factory=list)

    def __init__(self, clothing_types: List[str]):
        dynamic_data = {ct: [] for ct in clothing_types}
        super().__init__(clothing_types=clothing_types, **dynamic_data)
    

    def add_product(self, clothing_type: str, product: Product):

        if clothing_type not in self.clothing_types:
            print(f"Clothing type '{clothing_type}' not in outfit.")
        else:
            slot = getattr(self, clothing_type)
            slot.append(product)