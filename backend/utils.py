import tiktoken, json, re

from collections import defaultdict
from backend.database.model import Product, ProductBM
from backend.app.datatypes import ChatHistory

from backend.config.constants import MAX_TOKENS, EMBEDDING_MODEL, PRODUCT_GENERATION_TEMPERATURE, PRODUCT_GENERATION_MAX_TOKENS, CHAT_SYSTEM_PROMPT, PRODUCT_GENERATION_SYSTEM_PROMPT
from decimal import Decimal

def count_tokens(text: str, model: str = EMBEDDING_MODEL) -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def product_to_json(product: Product) -> dict:
    try:
        return {
            'id': product.id,
            'article_id': product.article_id,
            'name': product.name,
            'image_url': product.image_url,
            'price': product.price,
            'product_type': product.product_type,
            'product_group': product.product_group,
            'external_brand': product.external_brand,
            'product_description': product.product_description,
            'json_description': product.json_description,
            'color': product.color,
            'size': product.size,
            'embedding' : product.embedding
        }
    except Exception as e:
        print(f'Error converting {product.article_id} to json. Error:\n{e}')


def json_to_product(json: dict) -> Product:
    try:
        return Product(
            id=json.get('id'),
            article_id=json['article_id'],
            name=json['name'],
            image_url=json['image_url'],
            price=json['price'],
            product_type=json['product_type'],
            product_group=json.get('product_group'),
            external_brand=json.get('external_brand'),
            product_description=json.get('product_description'),
            json_description=json.get('json_description'),
            color=json.get('color'),
            size=json.get('size'),
            embedding=json.get('embedding')
        )
    except Exception as e:
        print(f'Error converting {json} to base. Error:\n{e}')


def product_to_base_model(product: Product):
    size_object = product.size if type(product.size) is list() else ['']

    return ProductBM(
        id = product.id,
        article_id = product.article_id,
        name = product.name,
        image_url = product.image_url,
        price = float(product.price),

        product_type = product.product_type,
        product_group = product.product_group,

        external_brand = product.external_brand,
        product_description = product.product_description,
        json_description = product.json_description,

        color = product.color,
        size = size_object,

        embedding = product.embedding
    )

def base_model_to_product(product: ProductBM):
    return Product(
        id = product.id,
        article_id = product.article_id,
        name = product.name,
        image_url = product.image_url,
        price = product.price,

        product_type = product.product_type,
        product_group = product.product_group,

        external_brand = product.external_brand,
        product_description = product.product_description,
        json_description = product.json_description,

        color = product.color,
        size = product.size,

        embedding = list(product.embedding) if product.embedding is not None else None
    )

def product_to_embedding_string(product: Product):
    fields = []

    try:
        fields.append(f'Name: {product.name}')

        if isinstance(product.price, Decimal):
            fields.append(f'Price: {product.price:.2f} GBP')
        else:
            fields.append(f'Price: {float(product.price):.2f} GBP')

        fields.append(f'Type: {product.product_type}')

        # Optional fields (conditionally included)
        if product.product_group:
            fields.append(f'Group: {product.product_group}')

        if product.product_description:
            fields.append(f'Description: {product.product_description}')
        
        if product.external_brand:
            fields.append(f'External Brand: {product.external_brand}')

        if product.color:
            colors = ', '.join(product.color)
            fields.append(f'Colors: {colors}')

        if product.json_description:
            json_description = product.json_description.replace(',', '\n').replace('"', '').replace(' :', ':')
            fields.append(json_description)

        for iteration in range(len(fields)):
            return_string = '\n'.join(fields)
            if count_tokens(return_string) <= MAX_TOKENS:
                break
            else:
                fields.pop(-1)
        
        return '\n'.join(fields)
    
    except Exception as e:
        print(f'Error converting {product} to embedding string. Error:\n{e}')


def parse_json_combining_duplicates(json_str: str) -> dict:

    def combine_duplicates(pairs):
        combined = defaultdict(lambda: None)

        for key, value in pairs:
            existing = combined[key]

            if isinstance(value, str):
                combined[key] = f'{existing or ''} {value}'
                combined[key] = combined[key].strip()
            elif isinstance(value, list):
                combined[key] = (existing or []) + value
            else:
                combined[key] = value
        return dict(combined)

    return json.loads(json_str, object_pairs_hook=combine_duplicates)


def format_generated_product(product: str ) -> Product:
    try:
        product_json = parse_json_combining_duplicates(product)

        product_json['article_id'] = '0000000000'
        product_json['image_url'] = 'dummyurl'
        product_json['price'] = re.sub(r'[^0-9.]', '', product_json['price'])
        
        color_save = list()

        if product_json['color']:
            if type(product_json['color']) is list:
                for color in product_json['color']:
                    if type(color) is str:
                        color_save.append(color.lower())
        
                product_json['color'] = color_save


        return json_to_product(product_json)
    except Exception as e:
        print(e)