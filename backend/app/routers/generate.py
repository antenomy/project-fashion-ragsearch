from datetime import datetime
from fastapi import APIRouter, HTTPException
import requests, json

from backend.database.model import ProductBM
from backend.app.datatypes.ChatHistory import ChatHistory
from typing import List

from backend.config.constants import HEADERS, AZURE_LLM_URL, LARGE_LANGUAGE_MODEL
from backend.config.constants import PRODUCT_GENERATION_MAX_TOKENS, PRODUCT_GENERATION_TEMPERATURE, PRODUCT_GENERATION_SCHEMA, GENERATED_PRODUCT_PATH
from backend.config.constants import DECOMPOSITION_GENERATION_SCHEMA, DECOMPOSITION_TEMPERATURE, DECOMPOSITION_MAX_TOKENS


from backend.utils import format_generated_product, product_to_json, product_to_base_model
# from

router = APIRouter()


@router.post('/prompt_to_product')
async def prompt_to_product(payload: ChatHistory) -> ProductBM:
    # Input: Previous chat history (list)
    # Output: Response json

    messages = [msg.model_dump() for msg in payload.messages]

    prompt = {
        'messages': messages,
        'tools': [PRODUCT_GENERATION_SCHEMA],
        'tool_choice': {
            'type': 'function',
            'function': {
                'name': 'get_product_info'
            }
        },
        'model': LARGE_LANGUAGE_MODEL,
        'temperature': PRODUCT_GENERATION_TEMPERATURE,
        'max_tokens': PRODUCT_GENERATION_MAX_TOKENS
    }



    try:
        response = requests.post(AZURE_LLM_URL, headers=HEADERS, json=prompt)
        response.raise_for_status()
        
        args_str = response.json()['choices'][0]['message']['tool_calls'][0]['function']['arguments']
        args_json = json.loads(args_str)

        product = format_generated_product(args_str)

        write_list = [args_json, product_to_json(product)]

        # SAVE FOR REFERENCE
        now = datetime.now()
        filename = now.strftime('%Y%m%d_%H%M%S_%f') + '.json'

        with open(f'{GENERATED_PRODUCT_PATH}/{filename}', 'w') as file:
            json.dump(write_list, file, indent=2)
        # ==== #
        

    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))


    return product_to_base_model(product)





@router.post('/decompose_question')
async def decompose_question(payload: ChatHistory) -> List[str]:

    messages = [msg.model_dump() for msg in payload.messages]

    print(messages)

    prompt = {
        'messages': messages,
        'tools': [DECOMPOSITION_GENERATION_SCHEMA],
        'tool_choice': {
            'type': 'function',
            'function': {
                'name': 'split_questions'
            }
        },
        'model': LARGE_LANGUAGE_MODEL,
        'temperature': DECOMPOSITION_TEMPERATURE,
        'max_tokens': DECOMPOSITION_MAX_TOKENS
    }


    try:
        response = requests.post(AZURE_LLM_URL, headers=HEADERS, json=prompt)
        response.raise_for_status()
        
        # print('response:')
        # print(response.json())
        exact_response = response.json()['choices'][0]['message']['tool_calls'][0]['function']['arguments']
        print(exact_response)

        if type(exact_response) is str:
            return_json = json.loads(exact_response)['questions']
        if type(exact_response) is dict:
            return_json = exact_response['questions']


        # product = 

    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return return_json



@router.post('/question_response')
async def question_response(message: ChatHistory, found_products: List[ProductBM]) -> str:

    user_question = message.messages[0].model_dump()

    product_string = '\n'.join([f'{prd.name}, {prd.color}, {prd.product_description}' for prd in found_products])

    system_prompt = {
        'role': 'system',
        'content': f'''You are a fashion advice and product search tool which is recieving a question and giving products as response.
You have retrieved products for their question and now have to give a very short response where you mention what they asked for and what you retrieved (not in detail).

Remember to mention the [product requested] and both the found products and personalise each response, if anyone is mentioned remember to maybe add them for context

Question:
{user_question}

Retrieved products:
{product_string}

Response:
'''
    }

    messages = [system_prompt, user_question]


    prompt = {
        'messages': messages,
        'model': LARGE_LANGUAGE_MODEL,
        'temperature': 0.5,
        'max_tokens': 150
    }

    try:
        response = requests.post(AZURE_LLM_URL, headers=HEADERS, json=prompt)
        response.raise_for_status()
        
        # print('response:')
        # print(response.json())
        exact_response = response.json()['choices'][0]['message']['content']
        # print(exact_response)

        # if type(exact_response) is str:
        #     return_json = json.loads(exact_response)['questions']
        # if type(exact_response) is dict:
        #     return_json = exact_response['questions']


        # product = 

    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return exact_response
    