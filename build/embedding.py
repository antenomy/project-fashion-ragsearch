from sentence_transformers import SentenceTransformer
import torch.nn.functional as torchF
from torch import argmax
# from numpy import argmax

# Load the model
model = SentenceTransformer('BAAI/bge-large-en-v1.5')

# Example clothing product text
product_text = "slim fit cotton chinos navy blue casual pants"

# Get embedding
example_embedding = model.encode([product_text], convert_to_tensor=True, normalize_embeddings=True)

# print(f"Embedding shape: {embedding.shape}")
# print(f"First 10 dimensions: {embedding[0][:10]}")
# print(f"Embedding type: {type(embedding)}")

# For multiple products
products = [
    "slim fit cotton chinos navy blue casual pants",
    "skinny jeans dark wash denim",
    "denim jacket dark wash",
    "wool sweater cable knit pullover",
    "red volvo fast car",
    "blue volvo casual car",
    "molotov cocktail"
    "H&M clothes",
    "meatballs",
    "pizza",
    "fortnite",
    "hamburger",
    "norway",
    "italy"
]

product_embedding_tensor = model.encode(products, convert_to_tensor=True, normalize_embeddings=True)
similarity_tensor = torchF.cosine_similarity(product_embedding_tensor, example_embedding)
best_index = argmax(similarity_tensor)

for index in range(len(products)):
    print(f"{products[index]} - {similarity_tensor[index]}\n")

print(f"""The closest match to \"{product_text}\" is:

{products[best_index]}""")