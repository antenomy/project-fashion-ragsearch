from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, Numeric, String, Identity
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import ARRAY

from pydantic import BaseModel
from typing import List, Optional



Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, server_default=Identity())
    article_id = Column(String, nullable = False)
    name = Column(String, nullable = False)
    image_url = Column(String, nullable = False)
    price = Column(Numeric(10, 2), nullable = False)

    product_type = Column(String, nullable = False)
    product_group = Column(String)

    external_brand = Column(String)
    product_description = Column(String)
    json_description = Column(String)

    color = Column(ARRAY(String))
    size = Column(ARRAY(String))

    embedding = Column(Vector(3072))


class ProductBM(BaseModel):
    id: Optional[int]
    article_id: str
    name: str
    image_url: str
    price: float

    product_type: str
    product_group: Optional[str]

    external_brand: Optional[str]
    product_description: Optional[str]
    json_description: Optional[str]

    color: Optional[List[str]]
    size: Optional[List[str]]

    embedding: Optional[List[float]]