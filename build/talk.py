import httpx, asyncio, json
import requests
import psutil, time
from crawl4ai import *

input_query = "Find me a blue jacket for me and a red dress for my friend. This is for a casual party tomorrow."

def check_system_resources():
    """Check if we have enough RAM"""
    memory = psutil.virtual_memory()
    available_gb = memory.available / (1024**3)
    print(f"Available RAM: {available_gb:.1f} GB")
    return available_gb > 1  # Need at least 2GB free

async def multi_query():
    if not check_system_resources():
        print("⚠️  Low memory! Close other apps first.")
        return

    prompt_end = f"""
    keep answer short!
"""
    prompt = f"""ask me any question you want
{prompt_end}"""
    for i in range(500):
        async with httpx.AsyncClient(timeout=30) as client:
            try:
                response = requests.post('http://localhost:11434/api/generate',
                    # json={
                    #     "model": "llama3.2:1b",  # Use 1B model
                    #     "prompt": prompt,
                    #     "stream": False,
                    #     "options": {
                    #         "temperature": 0,
                    #         "num_predict": 300,  # Short response
                    #         "num_ctx": 2048     # Smaller context window
                    #     }
                    json={
                        "model": "llama3.2:1b",
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 1,
                            "num_ctx": 2048,
                            "num_predict": 300
            }
                    }, timeout=30)
                
                response.raise_for_status()
                response_data = json.loads(response.text)

                print(prompt, "\n")

                # Now extract only the 'response' field
                prompt = response_data["response"] + prompt_end
                    
            except Exception as e:
                print(f"Request failed: {e}")

        time.sleep(4.5)
    # print(json_list)


if __name__ == "__main__":
    asyncio.run(multi_query())
