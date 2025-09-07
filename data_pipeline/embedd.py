import asyncio, json, os, time
from tqdm import tqdm

from backend.database.engine import SessionLocal
from backend.database.model import ProductBM

from data_pipeline.config.constants import BATCH_SIZE, EXPORT_FOLDER

from backend.app.routers.dev import embedd_and_save_product
from backend.utils import json_to_product, base_to_base_model

from backend.app.datatypes.EmbeddingId import EmbeddingId

IMPORT_FOLDER = 'data_pipeline/data/3_embedd'


# Batch by 500

filenames = os.listdir(IMPORT_FOLDER)
success_list = list()
fail_list = list()

for iteration in tqdm(range(len(filenames))):
    filename = filenames[iteration]

    if filename.endswith('.json'):
        try:
            with open(f'{IMPORT_FOLDER}/{filename}', 'r') as file:
                data = json.load(file)
                productBM = base_to_base_model(json_to_product(data))

                asyncio.run(embedd_and_save_product(productBM))
                success_list.append(filename.removesuffix('.json'))
        
        except Exception as e:
            print(e)
            fail_list.append(filename.removesuffix('.json'))
        
    
    # if (iteration+1) % BATCH_SIZE == 0:
    #     time.sleep(45)

with open(f'{EXPORT_FOLDER}/embedd.txt', 'w') as file:
    file.write(','.join(success_list))

with open(f'{EXPORT_FOLDER}/embedd_fail.txt', 'w') as file:
    file.write(','.join(fail_list))