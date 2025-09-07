import os, json
from tqdm import tqdm

from data_pipeline.config.constants import TYPE_BLACKLIST

import_folder = 'data_pipeline/data/alpha/refine'

filenames = os.listdir(import_folder)

for iteration in tqdm(range(len(filenames))):
    filename = filenames[iteration]

    if filename.endswith('.json'):
        file_path = f'{import_folder}/{filename}'
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            if data['product_type'] in TYPE_BLACKLIST:
                os.remove(file_path)
        except Exception as e:
            print(e)

