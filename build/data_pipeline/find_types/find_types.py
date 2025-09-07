import os, json

JSON_PATH = 'data_pipeline/data/alpha/refine'

types = dict()

total = len(os.listdir(JSON_PATH))
success = 0

for filename in os.listdir(JSON_PATH):
    try:
        with open(f'{JSON_PATH}/{filename}', 'r') as file:
            product = json.load(file)
        
        product_type = product['product_type'].strip().lower()

        if product_type in types:
            types[product_type] += 1
            
        else:
            types[product_type] = 1
    except Exception as e:
        print(e)
        input()
        continue

    success += 1

for key in types:
    print(f'{key}  :  {types[key]}')

print(f'{success} / {total}')