import os, random

with open('data_pipeline/build/preprocessing.txt', 'r') as file:
    product_ids = file.read().split(',')

scraped_ids = os.listdir('data_pipeline/scraper/results')

for id in scraped_ids:
    if id in product_ids:
        product_ids.remove(id)

random.shuffle(product_ids)

save_lists = [
    [],
    [],
    [],
    []
]

for iteration in range(len(product_ids)):
    index = iteration % 4
    save_lists[index].append(product_ids[iteration])


print_index = 1

for list in save_lists:
    with open(f'data_pipeline/build/preprocessing{print_index}.txt', 'w') as file:
        file.write(','.join(list))
    print_index += 1