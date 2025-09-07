file_name = 'round-2.txt' #input()

with open(file_name, 'r') as file:
    product_list = [line.strip() for line in file]

    simplified_product_list = list(set(product_list))

with open(file_name, 'w') as file:
    file.write(',\n'.join(f"{item}" for item in simplified_product_list))