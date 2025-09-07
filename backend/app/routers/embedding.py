from fastapi import APIRouter, HTTPException
import requests
from backend.config.constants import AZURE_KEY, AZURE_EMBEDDING_URL
from backend.app.datatypes.EmbeddingString import EmbeddingString

router = APIRouter()

@router.post("/embedd_string")
async def embedd_string(payload: EmbeddingString):
    headers = {
        "Content-Type" : "application/json",
        "api-key": AZURE_KEY
    }

    data = {
        "input": payload.input
    }

    try:
        response = requests.post(AZURE_EMBEDDING_URL, headers=headers, json=data)
        response.raise_for_status()
        embedding = response.json()['data'][0]['embedding']
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    return embedding