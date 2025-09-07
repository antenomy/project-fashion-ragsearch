import json
import os
from sqlalchemy.orm import sessionmaker


from backend.config.constants import DATA_FILE
# from backend.utils import measurement_to_json

from backend.database.engine import engine  # your SQLAlchemy engine
from backend.database.model import Base, Product

from backend.database.model import Product
from backend.utils import product_to_json

import_folder = 'backend/database/json-rewriter/import'
export_folder = 'backend/database/json-rewriter/export'

# from backend.utils import product_json_to_db_object

def raw_json_to_db_object(input_data : dict, id : str):

    basic_info = input_data.get('basicInfo', {})
    basic_info_property_whitelist = [
        'Concept',
        'Brand'
    ]

    presentation_info = input_data.get('presentationInfo', {})
    presentation_info_property_blacklist = [
        'Customer Group',
        'Travel Size',
        'Palette'
        'Presentation Product Type',
        'Presentation Product Group',
        'External Brand'
    ]

    image_object = input_data.get('images', {})

    size_object = basic_info.get('Size', None)

    if size_object:
        size_object = size_object.split(',')


    try:
        json_string = ''

        # Basic Info Json Description
        for key in basic_info_property_whitelist:
            value = basic_info.get(key, None)
            if value:
                json_string += f'"{key}" : "{value}",\n'

        # Presentation Info Json Description
        for key, value in presentation_info.items():
            if key not in presentation_info_property_blacklist:
                json_string += f'"{key}" : "{value}",\n'
        json_string = json_string.removesuffix(',\n')

        return Product(
            # General
            article_id = id,
            color = input_data.get('color', {}),
            image_url = image_object[0]['imageUrl'],

            # Basic Info
            name = basic_info['Product Name'],
            product_description = basic_info['Description'],
            json_description = json_string,
            size = size_object,
            price = basic_info['Price'].split()[0] ,

            # Presentation Info
            external_brand = presentation_info.get('External Brand', None),
            product_type = presentation_info.get('Presentation Product Type', None),
            product_group = presentation_info.get('Presentation Product Group', None)
        )
    except Exception as err:
        print(f'{input_data.get('articleId', {})} failed! Error:\n{err}')
        return False


product_list = list()

for filename in os.listdir(import_folder):
    if filename.endswith('.json'):
        with open(os.path.join(import_folder, filename), 'r') as file:
            data = json.load(file)
        
        article_id = filename[:-5]
        product_object = raw_json_to_db_object(data, article_id)

        if product_object:
            product_list.append(product_object) 

            # json_object = product_to_json(product_object)

            # with open(os.path.join(export_folder, filename), 'w') as file:
            #     file.write(json.dumps(json_object, indent=2))
        
        # break



Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

db = SessionLocal()

for product in product_list:
    try: 
        exists = db.query(Product).filter_by(article_id=product.article_id).first() is not None
        if not exists:            
            db.add(product)
            db.commit()
    except Exception as e:
        db.rollback()
        print(f'error id: {product.article_id}')
        # print(e)

db.close()

    






#presentationInfo
# Presentation Product Type
# Presentation Product Group
# External Brand

# Rest goes to custom description except for:

# DONT
# Customer Group
# Travel Size
# Palette



#basicInfo:
# Name
# Description
# Size
# Price

#Goes to custom description:
# Concept
# Brand
