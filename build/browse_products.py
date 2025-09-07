import os, json

search_str = 'Checked'
search_dir = 'data_pipeline/data/2_refine'#'data_pipeline/data/3_embedd'

files = os.listdir(search_dir)

for filename in files:
    with open(f'{search_dir}/{filename}', 'r') as file:
        product = file.read()
    
    if search_str in product:
        file_path = os.path.join(search_dir, filename)
        if os.path.isfile(file_path):
            print(f"\n--- Contents of {file_path} ---")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    print(f.read())
                input()
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
