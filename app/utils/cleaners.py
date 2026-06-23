from typing import Dict, Any, List
from app.logger import get_logger
from app.loader.anomaly_loader import log_anomaly

logger = get_logger(__name__)

def clean_coin_records_python(records: List, raw_id: int = None):
    cleaned = []

    for record in records:

        if not record.get("symbol"):
            log_anomaly(
                anomaly_type='missing_field',
                severity='warning',
                record=record,
                message=f"Пустой символ для {record['name']}: {record.get('symbol')}",
                field_name='symbol',
                raw_id=raw_id
            )
            record["symbol"] = "UNKNOWN"

        if not record.get("name"):
            log_anomaly(
                anomaly_type='missing_field',
                severity='warning',
                record=record,
                message=f"Пустое имя криптовалюты у {record['symbol']}",
                field_name='name',
                raw_id=raw_id
            )
            record["name"] = "UNKNOWN"
        
        if record.get('price_usd') is None:
            log_anomaly(
                anomaly_type='missing_field',
                severity='error',
                record=record,
                message=f"Отсутствует цена для {record['symbol', 'UNKNOWN']}",
                field_name='price_usd',
                raw_id=raw_id
            )
            record["price_usd"] = 0.0

        elif record.get("price_usd") < 0:
            log_anomaly(
                anomaly_type='negative_price',
                severity='error',
                record=record,
                message=f"Отрицательная цена для {record['symbol', 'UNKNOWN']}",
                expected_value=0.0,
                field_name='price_usd',
                raw_id=raw_id
            )
            record["price_usd"] = 0.0
        
        volume = record.get('volume_24h')
        if volume is None:
            log_anomaly(
                anomaly_type='missing_field',
                severity='warning',
                record=record,
                message=f"Отсутствует объем для {record['symbol', 'UNKNOWN']}",
                field_name='volume_24h',
                raw_id=raw_id
            )
            record["volume_24h"] = 0.0

        elif volume < 0:
            log_anomaly(
                anomaly_type='negative_volume',
                severity='error',
                record=record,
                message=f"Отрицательный объем {volume} для {record['symbol', 'UNKNOWN']}",
                expected_value=0.0,
                field_name='volume_24h',
                raw_id=raw_id
            )
            record["volume_24h"] = 0.0

        market_cap = record.get("market_cap")
        if market_cap is None:
            log_anomaly(
                anomaly_type='missing_field',
                severity='error',
                record=record,
                message=f"Отсутствует капитализация для {record['symbol', 'UNKNOWN']}",
                field_name='market_cap',
                raw_id=raw_id
            )
            record["market_cap"] = 0.0

        elif market_cap < 0:
            log_anomaly(
                anomaly_type='negative_value',
                severity='error',
                record=record,
                message=f"Отрицательная капитализация {market_cap} для {record['symbol', 'UNKNOWN']}",
                expected_value=0.0,
                field_name='market_cap',
                raw_id=raw_id
            )
            logger.warning(f"Неверная рыночная капитализация для {record['symbol']}: {record.get('market_cap')}")
            record["market_cap"] = 0.0
            
        cleaned.append(record)

    return cleaned

def clean_coin_records_sql():
    #доделаю позже
    raise Exception("Функция еще не реализована")

def clean_coin_records(records: List, method: str = 'python', raw_id: int = None) -> List:
    if method == 'python':
        return clean_coin_records_python(records, raw_id)
    elif method == 'sql':
        return clean_coin_records_sql()
    else:
        raise Exception(f"Неизвестный тип метода очистки: {method}")

