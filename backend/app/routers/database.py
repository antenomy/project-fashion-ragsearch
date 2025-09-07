from fastapi import APIRouter, HTTPException

from backend.database.engine import SessionLocal
from backend.database.model import Product, ProductBM

from backend.utils import product_to_base_model

router = APIRouter()



@router.get('/id_get/{article_id}')
async def db_id_get(article_id : str):
    db = SessionLocal()

    try:
        item = db.query(Product).filter(Product.article_id == article_id).first()
        return product_to_base_model(item).model_dump()
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.get('/category_get/{category}')
async def db_category_get(category : str):
    db = SessionLocal()

    try:
        items = db.query(Product).all().filter(ProductBM.product_type == category)
        return [product_to_base_model(item).model_dump() for item in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.get('/get_all')
async def db_get_all():
    db = SessionLocal()

    try:
        items = db.query(Product).all()
        return [product_to_base_model(item).model_dump() for item in items]
    except Exception as e:
        print(f"Error in db_get_all: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@router.get('/get_count/page{page_number}/{count}')
async def get_count(page_number: int, count: int):
    db = SessionLocal()

    try:
        items = (db.query(Product)
            .offset(page_number * count)
            .limit(count)
            .all()
        )

        return [product_to_base_model(item).model_dump() for item in items]
    except Exception as e:
        print(f"Error in db_get_all: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()