import json
from datetime import datetime
from typing import Dict, Any, Optional
from app.logger import get_logger
from app.db import get_connection, release_connection

logger = get_logger(__name__)

def log_anomaly(
        anomaly_type: str,
        severity: str,
        record: dict,
        message: str,
        field_name: Optional[str] = None,
        expected_value: Optional[str] = None,
        raw_id: int = None,
        stg_id: int = None
) -> int:
    conn = get_connection

    coin_id = record.get("coin_id")
    symbol = record.get("symbol")
    actual_value = record.get(field_name)

    try:
        with conn.cursor() as cursor:

            sql = """
                    INSERT INTO public.anomaly_log(anomaly_type, severity, coin_id, symbol, field_name, expected_value, actual_value, raw_id, stg_id, message)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """
            
            cursor.execute(sql,
                           anomaly_type, severity, coin_id, symbol, field_name, expected_value, actual_value, raw_id, stg_id, message)
            conn.commit()
            inserted_id = cursor.fetchone()[0]

            logger.info(f"Данные сохранены в public.anomaly_log с ID {inserted_id}")
    except Exception as e:    
        conn.rollback()
        logger.error(f"Возникла ошибка при сохранении: {e}")
        raise
    finally:
        release_connection(conn)