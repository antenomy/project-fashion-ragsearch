import json, os
from tqdm import tqdm

from backend.utils import base_to_embedding_string, json_to_product, count_tokens

import_folder = 'data_pipeline/data/3_embedd'

token_count_list = []

filenames = os.listdir(import_folder)

# with open(f'{import_folder}/{filenames[1]}', 'r') as file:
#     data = json.load(file)

# product = json_to_product(data)

# with open('embedd_string_template.json', 'w') as file:
#     file.write(base_to_embedding_string(product))

# filenames = [int(filename[:10]) for filename in filenames]

# average = sum(filenames) / len(filenames)

# print(average)

for iteration in tqdm(range(len(filenames))):
    filename = filenames[iteration]

    if filename.endswith('.json'):
        with open(f'{import_folder}/{filename}', 'r') as file:
            data = json.load(file)

            product = json_to_product(data)

            if product:
                embedding_string = base_to_embedding_string(product)

                if embedding_string:
                    token_count = count_tokens(embedding_string)

                    # print(embedding_string)
                    # print(f'Token Count: {token_count}')
                    token_count_list.append((token_count, embedding_string, data.get('article_id')))

total = sum([pair[0] for pair in token_count_list])
average = total / len(token_count_list)
sorted_list = sorted(token_count_list, key=lambda x: x[0])
print(f'''Highest: {sorted_list[-1][0]}
{sorted_list[-1][2]}
{sorted_list[-1][1]}
      
Average: {round(average)}
Total: {total}

Lowest: {sorted_list[0][0]}
{sorted_list[0][2]}
{sorted_list[0][1]}''')
