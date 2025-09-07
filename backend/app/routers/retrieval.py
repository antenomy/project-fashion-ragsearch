from fastapi import APIRouter
import webbrowser

from torch import Tensor, cosine_similarity, from_numpy

from backend.database.engine import SessionLocal
from backend.database.model import Product, ProductBM
from backend.app.datatypes.EmbeddingString import EmbeddingString
from backend.app.datatypes.ChatHistory import ChatHistory
from backend.app.datatypes.ProductRanking import ProductRanking
from typing import List

from backend.config.constants import AZURE_KEY, AZURE_EMBEDDING_URL

from backend.utils import product_to_embedding_string, base_model_to_product, product_to_base_model
from backend.app.routers.generate import prompt_to_product
from backend.app.routers.embedding import embedd_string

router = APIRouter()

@router.post('/from_product')
async def on_product(input_product: ProductBM) -> List[ProductRanking]:
    # Input: ProductBM
    # Output: List of tuples with similarity and id to each product

    db = SessionLocal()

    try:
        products = db.query(Product).all()
    except Exception as e:
        raise e
    finally:
        db.close()
    
    similarities = []

    try:
        generated_embedding_string = product_to_embedding_string(input_product)

        embedding = await embedd_string(EmbeddingString(input = generated_embedding_string))
        embedding_a = Tensor(embedding).unsqueeze(0)

        for product in products:
            # if product.product_type == generated_product.product_type:
                # print('found red clothing')
                
            embedding_b = from_numpy(product.embedding).unsqueeze(0)

            sim = cosine_similarity(embedding_a, embedding_b).item()
            similarities.append(ProductRanking(similarity = float(sim), product = product_to_base_model(product)))

        similarities.sort(key = lambda product_ranking: product_ranking.similarity)

    except Exception as e:
        raise e

    return similarities


@router.post('/from_prompt')
async def on_prompt(payload: ChatHistory):
    # Input: Chat logs
    # Output: List of tuples with similarity and id to each product

    db = SessionLocal()

    try:
        products = db.query(Product).all()
    except Exception as e:
        # print(f'Error: {e}')
        raise e
    finally:
        db.close()
    
    similarities = []

    try:
        generated_product = base_model_to_product(await prompt_to_product(payload))
        generated_embedding_string = product_to_embedding_string(generated_product)

        print(generated_embedding_string)

        embedding = await embedd_string(EmbeddingString(input = generated_embedding_string))
        embedding_a = Tensor(embedding).unsqueeze(0)

        for product in products:
            # if product.product_type == generated_product.product_type:
                # print('found red clothing')
                
            embedding_b = from_numpy(product.embedding).unsqueeze(0)

            sim = cosine_similarity(embedding_a, embedding_b).item()
            similarities.append((sim, product.article_id, product.image_url))

        similarities.sort(key = lambda x: x[0])

    except Exception as e:
        raise e

    if similarities and len(similarities[-1]) > 1:
        for sim in similarities[-3:]:
            webbrowser.open(sim[2])
        return [f'{sim[1]} {round(sim[0] * 100, 2)}%' for sim in similarities[-3:]]
    else:
        return 'none found'
