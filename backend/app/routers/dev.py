from fastapi import APIRouter, HTTPException
import requests

from backend.config.constants import AZURE_KEY, AZURE_EMBEDDING_URL

from backend.database.engine import SessionLocal
from backend.database.model import Product, ProductBM
from backend.app.datatypes.EmbeddingId import EmbeddingId

from backend.utils import base_model_to_product, product_to_embedding_string

router = APIRouter()


@router.post('/embedd_and_save_product')
async def embedd_and_save_product(payload : ProductBM):
    headers = {
        'Content-Type' : 'application/json',
        'api-key': AZURE_KEY
    }

    # print(f'Embedding and Saving {payload.article_id}.')

    db = SessionLocal()

    exists = db.query(Product).filter_by(article_id=payload.article_id).first() is not None

    if not exists:
        try:
            new_product = base_model_to_product(payload)
            product_embedding = product_to_embedding_string(new_product)

            data = {
                'input': product_embedding
            }

            response = requests.post(AZURE_EMBEDDING_URL, headers=headers, json=data)
            response.raise_for_status()

            new_product.embedding = response.json()['data'][0]['embedding']

            db.add(new_product)
            db.commit()
            db.refresh(new_product)
        
        except requests.exceptions.HTTPError as e:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=str(e))
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            db.close()

        return response.json()
    else:
        db.close()

@router.post('/embedd_existing')
async def embedd_existing(payload: EmbeddingId):
    headers = {
        'Content-Type' : 'application/json',
        'api-key': AZURE_KEY
    }

    try:
        db = SessionLocal()
        edit_product = db.query(Product).filter(Product.article_id == payload.id).first()

        product_embedd_string = product_to_embedding_string(edit_product)

        data = {
            'input': product_embedd_string
        }

        response = requests.post(AZURE_EMBEDDING_URL, headers=headers, json=data)
        response.raise_for_status()

        embedding = response.json()['data'][0]['embedding']

        if not hasattr(edit_product, 'embedding'):
            raise AttributeError('Field "embedding" does not exist on object.')
        
        setattr(edit_product, 'embedding', embedding)
        db.commit()

    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

    return response.json()