import requests
from typing import Dict, Any, List
from app.logger import get_logger
import os
import time
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
base_api = os.getenv("BASE_API")
listings_latest = base_api+os.getenv("LISTINGS_L")
MAX_RETRIES = 3
RETRY_DELAY = 60
DEFAULT_LIMIT = 100

headers = {
    "X-CMC_PRO_API_KEY": api_key
    }


logger = get_logger(__name__)

def fetch_listings(limit: int = DEFAULT_LIMIT):
    params = {
        "limit": limit,
        "convert": "USD"
    }
    last_err = None
    for attempt in range(1, MAX_RETRIES + 1): 
        try:   
            response = requests.get(url = listings_latest, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            status_error_code = data.get("status", {}).get("error_code")
            if status_error_code != 0:
                error_msg = data.get("status", {}).get("error_message", "Unknown error")
                logger.error("CMC API вернул ошибку: code=%s, msg=%s", status_error_code, error_msg)
                raise Exception(f"CMC API error: {error_msg}")

            logger.info(f"Успешно получены {len(data.get('data', []))} криптовалют")
            return data
        except requests.exceptions.RequestException as e:
            last_err = e
            logger.warning("Возникла ошибка, попытка подключения %s из %s: %s", attempt, MAX_RETRIES, e)
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)

    logger.error("Все попытки подключения к API провалились")
    raise Exception("Не удалось получить данные после %s попыток", MAX_RETRIES) from last_err
