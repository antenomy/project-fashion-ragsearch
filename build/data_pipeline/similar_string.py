import asyncio
import webbrowser
from tqdm import tqdm

from torch import cosine_similarity, from_numpy, Tensor

from backend.database.engine import SessionLocal
from backend.database.model import Product

from backend.app.datatypes.EmbeddingString import EmbeddingString

from backend.app.routers.embedding import embedd_string


async def similar_string():

    input_string = input()

    db = SessionLocal()

    try:
        # Select only the article_id column from the Product table
        products = db.query(Product).all()
    except Exception as e:
        print(f'Error: {e}')
    finally:
        db.close()
    
    similarity = []
    

    input_embedding = await embedd_string(EmbeddingString(input=input_string))

    emb_a = Tensor(input_embedding).unsqueeze(0)

    for iteration in tqdm(range(len(products))):
        product = products[iteration]

        emb_b = from_numpy(product.embedding).unsqueeze(0)

        try:
            sim = cosine_similarity(emb_a, emb_b).item()
            similarity.append((sim, product.article_id, product.image_url))
        except Exception as e:
            print(f'Error computing similarity between {product.article_id} and {input_string}: {e}')
    

    similarity.sort(key = lambda x: x[0])

    print('HIGHEST SIMILARITY\n','\n'.join([f'''{round(similarity[-(1 + iteration)][0], 4)}
{similarity[-(1 + iteration)][1]}''' for iteration in range(5)]), '\n')
    
#     print('LOWEST SIMILARITY\n','\n'.join([f'''{round(tuple_list[iteration][0], 4)}
# {tuple_list[iteration][1].name} {tuple_list[iteration][1].article_id}''' for iteration in range(5)]))

    webbrowser.open(similarity[-1][2])

asyncio.run(similar_string())

#hello i am looking for a pair of turquoise jeans for a casual setting tomorrow