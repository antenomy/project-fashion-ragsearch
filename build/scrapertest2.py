import asyncio
import json
import requests
import psutil
import re
from crawl4ai import *

START_PHRASE = "View products"
STOP_PHRASE = "Delivery and Payment"

def check_system_resources():
    """Check if we have enough RAM"""
    memory = psutil.virtual_memory()
    available_gb = memory.available / (1024**3)
    print(f"Available RAM: {available_gb:.1f} GB")
    return available_gb > 1.5  # Need at least 2GB free

async def extract_product_info(crawler, url: str, schema: dict) -> dict:
    
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url
            )
        print(result.markdown)
        if START_PHRASE in result.markdown and STOP_PHRASE in result.markdown:
            formatted_result = result.markdown.split(START_PHRASE)[1]
            product_info = formatted_result.split(STOP_PHRASE)[0]
        else:
            # Fallback: use first 2000 characters
            product_info = result.markdown[:2000]
        
        # print(product_info)

        # Use much shorter prompt for small model
        short_prompt = f"""Extract product information from this H&M page and return ONLY a JSON object with these exact fields:

{json.dumps(schema, indent=2)}

Product page content:
{product_info}

Return only the JSON object with the exact field names shown above. Do not add any additional fields."""
        try:
            response = requests.post('http://localhost:11434/api/generate',
                json={
                    "model": "llama3.2:1b",  # Use 1B model
                    "prompt": short_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0,
                        "num_predict": 300,  # Short response
                        "num_ctx": 2048     # Smaller context window
                    }
                }, timeout=30)
            
            if response.status_code == 200:
                result_text = response.json()['response']
                # print("LLM Response:")
                # print(result_text)

                try:
                    parsed_json = json.loads(result_text)
                    # Check if it only contains expected keys
                    expected_keys = set(schema.keys())
                    actual_keys = set(parsed_json.keys())
                    
                    if actual_keys == expected_keys:
                        print("✅ Schema matches perfectly!")
                        return result_text
                    else:
                        extra_keys = actual_keys - expected_keys
                        missing_keys = expected_keys - actual_keys
                        if extra_keys:
                            print(f"⚠️  Extra keys found: {extra_keys}")
                        if missing_keys:
                            print(f"⚠️  Missing keys: {missing_keys}")
                            
                except json.JSONDecodeError:
                    print("⚠️  Response is not valid JSON")

            else:
                print(f"Error: {response.status_code}")
                
        except Exception as e:
            print(f"Request failed: {e}")

async def crawl_category_page(base_category_url: str, schema: dict, max_products: int = 2) -> list:
    
    print(f"🔍 Discovering products from category: {base_category_url}")
    
    async with AsyncWebCrawler() as crawler:
        # First, get the category page
        category_result = await crawler.arun(url=base_category_url)
        
        # Extract product URLs (you'll need to adjust this regex based on H&M's structure
        product_urls = re.findall(r'https://www2\.hm\.com/[^/]+/productpage\.\d+\.html', category_result.markdown)
        
        # Remove duplicates and limit
        unique_urls = list(set(product_urls))[:max_products]
        
        # print(f"📦 Found {len(unique_urls)} unique products to crawl"
        
        return_list = []
        
        if unique_urls:
            tasks = [extract_product_info(crawler, url, schema) for url in unique_urls]
            json_list = await asyncio.gather(*tasks)

            return [json.loads(item) for item in json_list]
        else:
            print("❌ No product URLs found. You may need to adjust the URL pattern.")


async def main():
    if not check_system_resources():
        print("⚠️  Low memory! Close other apps first.")
        return
    
    url = 'https://www2.hm.com/en_gb/men/shop-by-product/jackets-and-coats/denim-jackets.html'

    schema={
            "name": "Product name",
            "price": "Product price", 
            "description": "Product description",
            "material": "Material composition",
            "fit": "Fit type",
            "color": "Color description"
        }
    
    json_list = await crawl_category_page(url, schema)

    with open('result.json', 'w') as f:
        json.dump(json_list, f, indent=2, ensure_ascii=False)


    # print(json_list)


if __name__ == "__main__":
    asyncio.run(main())