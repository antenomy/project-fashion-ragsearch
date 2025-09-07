from data_pipeline.utils import extract_ids_from_raw, save_to_id_file
from data_pipeline.config.constants import DATA_PATH, RUN_NAME #, REMEMBER TO NOT OVERWRITE EXPORT_FOLDER

INPUT_FILE = DATA_PATH + '/0_preprocessing/raw_data.txt'
OLD_FILE = DATA_PATH + '/0_preprocessing/old_ids.txt'


def preprocessing(input_file: str, old_file: str, export_file: str):
    print('Preprocessing raw data...')

    raw_ids = extract_ids_from_raw(input_file)
        
    if old_file:
        with open(old_file, 'r') as file:
            old_ids = file.read().split(',')

    raw_ids.extend(old_ids)

    ids_adjusted_length = list()

    for id in raw_ids:
        if len(id) >= 7:
            ids_adjusted_length.append(id[:7])

    product_ids = list(set(ids_adjusted_length))

    print(f'Extracted {len(product_ids)} from:\n{input_file}\n{old_file}')

    save_to_id_file(product_ids, export_file, 'preprocessing')


preprocessing(INPUT_FILE, OLD_FILE, EXPORT_FOLDER)