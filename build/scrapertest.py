import asyncio
import json
import requests
from crawl4ai import *

# Define your schema
PRODUCT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "price": {"type": "string"},
        "description": {"type": "string"},
        "images": {"type": "array", "items": {"type": "string"}},
        "sizes": {"type": "array", "items": {"type": "string"}},
        "colors": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["name", "price"]
}

def format_with_ollama(content, schema):
    print("atempting formating with ollama")
    
    prompt = f"""
Extract product information from this HTML content and format it according to this JSON schema:

Schema: {json.dumps(schema, indent=2)}

HTML Content: {content[:5000]}  # Truncate if too long

Return only valid JSON that matches the schema.
"""
    
    response = requests.post('http://localhost:11434/api/generate',
        json={
            "model": "llama3.1",  # or whatever model you have
            "prompt": prompt,
            "stream": False
        })
    
    return response.json()['response']

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://www2.hm.com/sv_se/productpage.1283781001.html",
        )
        
        # Format with local LLM

        formatted_result = result #format_with_ollama(result.markdown, PRODUCT_SCHEMA)
        print(result.markdown)
        # try:
        #     product_data = json.loads(formatted_result)
        #     print(json.dumps(product_data, indent=2))
        # except json.JSONDecodeError:
        #     print("Failed to parse JSON, raw response:")
        #     print(formatted_result)

if __name__ == "__main__":
    asyncio.run(main())