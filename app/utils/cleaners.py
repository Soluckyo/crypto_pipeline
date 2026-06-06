from typing import Dict, Any, List
from app.logger import get_logger

logger = get_logger(__name__)

def clean_coin_records_python(records: List):
    cleaned = []

    for record in records:
        if not record.get("name"):
            logger.warning(f"Пустое имя криптовалюты у {record['symbol']}")
            record["name"] = "UNKNOWN"
        
        if record.get('price_usd') is None or record.get("price_usd") < 0:
            logger.warning(f"Неверная цена для {record['symbol']}: {record.get('price_usd')}")
            record["price_usd"] = 0.0
        
        if record.get('volume_24h') is None or record.get("volume_24h") < 0:
            logger.warning(f"Неверный торговый объем для {record['symbol']}: {record.get('volume_24h')}")
            record["volume_24h"] = 0.0

        if record.get('market_cap') is None or record.get("market_cap") < 0:
            logger.warning(f"Неверная рыночная капитализация для {record['symbol']}: {record.get('market_cap')}")
            record["market_cap"] = 0.0

        if not record.get("symbol"):
            logger.warning(f"Пустой символ для {record['name']}: {record.get('symbol')}")            
            record["symbol"] = "UNKNOWN"
            
        cleaned.append(record)

    return cleaned

def clean_coin_records_sql():
    #доделаю позже
    raise Exception("Функция еще не реализована")

def clean_coin_records(records: List, method: str = 'python') -> List:
    if method == 'python':
        return clean_coin_records_python(records)
    elif method == 'sql':
        return clean_coin_records_sql()
    else:
        raise Exception(f"Неизвестный тип метода очистки: {method}")

