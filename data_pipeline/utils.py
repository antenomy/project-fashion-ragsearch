from data_pipeline.config.constants import BASE_PRODUCT_PRICES

def extract_ids_from_raw(input_file: str) -> list:
    export_ids = list()

    with open(input_file, 'r') as file:
        raw_data_split = file.read().strip().split('\n')

    for data in raw_data_split:
        if (len(data) == 7 or len(data) == 10) and data.isnumeric():
            export_ids.append(data)
    
    return export_ids

def save_to_id_file(ids: list, export_file: str, step: str):

    with open(f'{export_file}/{step}.txt', 'w') as file:
        file.write(','.join(ids))


def raw_to_structured_json(input_data : dict, product_id : str, variant_id: str) -> dict:

    basic_info = input_data.get('basicInfo', None)
    basic_info_property_whitelist = [
        'Concept',
        'Brand'
    ]

    presentation_info = input_data.get('presentationInfo', None)
    presentation_info_property_blacklist = [
        'Customer Group',
        'Travel Size',
        'Palette',
        'Presentation Product Type',
        'Presentation Product Group',
        'External Brand'
    ]

    try:
        variant = input_data['variants'][variant_id]
        image_object = variant['image_url'].removesuffix('data_pipeline/data/2_refine') + '.jpg?imwidth=1536'

        size_object = basic_info.get('Size', None)

        if size_object:
            size_object = size_object.split(',')
        
        colors = variant['color'].split('/')
        color_object = [color.strip().lower() for color in colors]


        # Set Price if Non Existant
        price_object = input_data.get('Price', None)

        if price_object:
            price_object = price_object.strip().split()[0]
        else:
            if presentation_info['Presentation Product Type'] in BASE_PRODUCT_PRICES:
                price_object = BASE_PRODUCT_PRICES[presentation_info['Presentation Product Type']]
            else:
                if ',' in basic_info['Product Name']:
                    price_object = '44.99'
                else:
                    price_object = '14.99'


        # Create Json String Description
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

        return{
            'article_id': product_id + variant_id,
            'name': basic_info['Product Name'],
            'image_url': image_object,
            'price': price_object,
            'product_type': presentation_info['Presentation Product Type'].lower(),
            'product_group': presentation_info.get('Presentation Product Group', None),
            'external_brand': presentation_info.get('External Brand', None),
            'product_description': basic_info['Description'],
            'json_description': json_string,
            'color': color_object,
            'size': size_object,
        }

    except Exception as err:
        print(f'{input_data.get('articleId', {})} failed! Error:\n{err}')
        return False
    
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