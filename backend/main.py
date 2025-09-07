from fastapi import FastAPI

from backend.database.engine import engine
from backend.database.model import Base

from backend.app.datatypes.RecommendationResponse import RecommendationResponse
from backend.app.datatypes.ChatHistory import ChatHistory
# from backend.app.datatypes.ProductRanking import ProductRanking
from backend.app.datatypes.Outfit import Outfit
from typing import List

# from backend.app.routers.generate import 

from backend.app.routers import embedding, database, dev, generate, retrieval


# === Initial App&DB Setup === #

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(embedding.router, prefix='/embedding')
app.include_router(database.router, prefix='/database')
app.include_router(dev.router, prefix='/dev')
app.include_router(generate.router, prefix='/generate')
app.include_router(retrieval.router, prefix='/retrieval')

# === Initial App&DB Setup === #



# LAYOUT

# /embedding
#   /embedd_string
#

# /database
#   /get_all
#   /id_get/{article_id}
#   /category_get/{category}

# /dev
#   /embedd_and_save_product
#   /embedd_existing


@app.post("/recommend_products")
async def recommend_products(payload: ChatHistory) -> List[RecommendationResponse]:
    # Input: ChatHistory object from user and system chatting
    # Output: A list of RecommendationResponse objects, one for each user request, with 1-2 article IDs and a NL response.

    responses = list()

    # Decomposition
    # ChatHistory -> List(str)
    print('Decomposing query..')
    try:
        decomposed_questions = await generate.decompose_question(payload)
    except Exception as e:
        print(e)
        decomposed_questions = [payload]

    print(f'Decomposed to:\n{'\n'.join(decomposed_questions)}')

    for question in decomposed_questions:

        # Convert message to ChatHistory object
        if type(question) is str:
            message = ChatHistory.from_str(question)
        elif type(question) is ChatHistory:
            message = question
        else:
            continue

        # HyDE
        # ChatHistory -> ProductBM
        print(f'Converting question "{question}" to product...')
        product = await generate.prompt_to_product(message)

        # Retreival
        # ProductBM -> [ProductRanking]
        print(f'Running retrieval on mock product: "{product.name}"...')
        products_with_similarity = await retrieval.on_product(product)

        # Ranking
        # [ProductRanking] -> [ProductRanking]
        print('Ranking resuts...')
        products_ranked = products_with_similarity

        try:
            top_products = [products_ranked[-1].product, products_ranked[-2].product]

            # response_ids = [prd.article_id for prd in top_products]
            response_message = await generate.question_response(message, top_products)
            # POTENTIAL FEATURE: ADD MESSAGES REGARDING MISSING TYPE, COLOUR, etc. PROMPT LLM TO COMPARE AND GIVE RESPONSE
            # POTENTIAL FEATURE: ADD PREVIOUS MESSAGES TO CONTEXT TO AVOID REPETITION

            responses.append(
                RecommendationResponse(
                    products = top_products,
                    message = response_message if response_message else 'Here is what I found:'
                )
            )
        except Exception as e:
            raise e
    
    return responses


@app.post("/recommend_outfit")
async def recommend_outfit(payload: ChatHistory) -> Outfit:
    # Input: ChatHistory object from user and system chatting
    # Output: A list of RecommendationResponse objects, one for each user request, with 1-2 article IDs and a NL response.

    responses = list()

    # Decomposition
    # ChatHistory -> List(str)
    print('Decomposing query..')
    try:
        decomposed_questions = await generate.decompose_question(payload)
    except Exception as e:
        print(e)
        decomposed_questions = [payload]

    print(f'Decomposed to:\n{'\n'.join(decomposed_questions)}')

    for question in decomposed_questions:

        # Convert message to ChatHistory object
        if type(question) is str:
            message = ChatHistory.from_str(question)
        elif type(question) is ChatHistory:
            message = question
        else:
            continue

        # HyDE
        # ChatHistory -> ProductBM
        print(f'Converting question "{question}" to product...')
        product = await generate.prompt_to_product(message)

        # Retreival
        # ProductBM -> [ProductRanking]
        print(f'Running retrieval on mock product: "{product.name}"...')
        products_with_similarity = await retrieval.on_product(product)

        # Ranking
        # [ProductRanking] -> [ProductRanking]
        print('Ranking resuts...')
        products_ranked = products_with_similarity

        try:
            top_products = [products_ranked[-1].product, products_ranked[-2].product]

            # response_ids = [prd.article_id for prd in top_products]
            response_message = await generate.question_response(message, top_products)
            # POTENTIAL FEATURE: ADD MESSAGES REGARDING MISSING TYPE, COLOUR, etc. PROMPT LLM TO COMPARE AND GIVE RESPONSE
            # POTENTIAL FEATURE: ADD PREVIOUS MESSAGES TO CONTEXT TO AVOID REPETITION

            responses.append(
                RecommendationResponse(
                    products = top_products,
                    message = response_message if response_message else 'Here is what I found:'
                )
            )
        except Exception as e:
            raise e
    
    return responses