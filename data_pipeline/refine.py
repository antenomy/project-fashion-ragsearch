import json, os

from data_pipeline.utils import save_to_id_file, raw_to_structured_json
from data_pipeline.config.constants import EXPORT_FOLDER

IMPORT_FOLDER = 'data_pipeline/data/2_refine'

# Check for correct fields
# Save bad products
# Create articles from 


# 4. Refine for non-nullable field
#     - Add fake price if non-existant
#     - Add fake type if non-existant
# 5. Transform to product json structure

product_jsons = list()

refined_ids = list()
refine_fail_ids = list()

for filename in os.listdir(IMPORT_FOLDER):
    if filename.endswith('.json'):
        file_id = filename.removesuffix('.json')

        try:
            with open(os.path.join(IMPORT_FOLDER, filename), 'r') as file:
                data = json.load(file)
        
            if 'articleId' in data and 'variants' in data:
                product_id = data['articleId']
                
                if len(data['variants']) >= 1:
                    for variant_code in data['variants']:
                        product_object = raw_to_structured_json(data, product_id, variant_code)

                        if product_object:
                            print("sucess!!")
                            refined_ids.append(product_object['article_id'])
                            product_jsons.append(product_object)
        except Exception as e:
            # print(e)
            pass


save_to_id_file(refined_ids, EXPORT_FOLDER, 'refine')

shortened_refined = list(set([id[:7] for id in refined_ids]))

with open(f'{EXPORT_FOLDER}/preprocessing.txt', 'r') as file:
    all_ids = file.read().split(',')

for id in all_ids:
    if id not in shortened_refined:
        refine_fail_ids.append(id)

save_to_id_file(refine_fail_ids, EXPORT_FOLDER, 'refine_fail')

for product in product_jsons:
    with open(f'{EXPORT_FOLDER}/refine/{product['article_id']}.json', 'w') as file:
        json.dump(product, file, indent=2)
