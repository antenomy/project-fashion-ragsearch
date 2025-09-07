import asyncio

from torch import cosine_similarity, from_numpy

from backend.database.engine import SessionLocal
from backend.database.model import Product


async def similar_entries():
    db = SessionLocal()

    try:
        # Select only the article_id column from the Product table
        products = db.query(Product).all()
    except Exception as e:
        print(f'Error: {e}')
    finally:
        db.close()
    
    tuple_list = []

    for product_a in products:
        for product_b in products:
            if product_a.name != product_b.name:
                emb_a = from_numpy(product_a.embedding).unsqueeze(0)
                emb_b = from_numpy(product_b.embedding).unsqueeze(0)

                try:
                    sim = cosine_similarity(emb_a, emb_b).item()
                    tuple_list.append((sim, product_a, product_b))
                except Exception as e:
                    print(f'Error computing similarity between {product_a.article_id} and {product_b.article_id}: {e}')
    

    tuple_list.sort(key = lambda x: x[0])

    print('LOWEST SIMILARITY\n','\n'.join([f'''{round(tuple_list[-(1 + iteration)][0], 4)}
{tuple_list[-(1 + iteration)][1].name} {tuple_list[-(1 + iteration)][1].article_id}
{tuple_list[-(1 + iteration)][2].name} {tuple_list[-(1 + iteration)][2].article_id}''' for iteration in range(5)]), '\n')
    
    print('HIGHEST SIMILARITY\n','\n'.join([f'''{round(tuple_list[iteration][0], 4)}
{tuple_list[iteration][1].name} {tuple_list[iteration][1].article_id}
{tuple_list[iteration][2].name} {tuple_list[iteration][2].article_id}''' for iteration in range(5)]))

asyncio.run(similar_entries())

#  1261757001
#  1254480001
#  1290806001
#  1250094001
#  1272508001
#  1262096001
#  1250735001
