from typing import Dict, Any, Optional
from app.logger import get_logger
from app.db import get_connection, release_connection

logger = get_logger(__name__)

def get_latest_raw_listings(validation_status: str = 'valid') -> Optional[Dict[str, Any]]:
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            sql =   """ SELECT id, raw_data, validation_status, loaded_at, api_timestamp
                          FROM raw.crypto_listings
                         WHERE validation_status = %s
                         ORDER BY id DESC
                         LIMIT 1
                    """
            cur.execute(sql, (validation_status,))
            raw = cur.fetchone()

            if not raw :
                logger.warning(f"Нет записей со статусом {validation_status} в raw.crypto_listings")

                return None
            
            return {
                "id": raw[0],
                "raw_data": raw[1],
                "validation_status": raw[2],
                "loaded_at": raw[3],
                "api_timestamp": raw[4]
            }
    except Exception as e:
        logger.error(f"Ошибка при получении записей: {e}")
        raise
    finally:
        release_connection(conn)

def get_raw_listings_by_id(id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            sql =   """ SELECT id, raw_data, validation_status, loaded_at, api_timestamp
                          FROM raw.crypto_listings
                         WHERE id = %s
                         ORDER BY id DESC
                         LIMIT 1
                    """
            cur.execute(sql, (id,))
            raw = cur.fetchone()

            if not raw:
                logger.warning(f"Записи с id {id} в raw.crypto_listings не нашлось")

                return None
            
            return {
                "id": raw[0],
                "raw_data": raw[1],
                "validation_status": raw[2],
                "loaded_at": raw[3],
                "api_timestamp": raw[4]
            }
    except Exception as e:
        logger.error(f"Ошибка при получении записи: {e}")
        raise
    finally:
        release_connection(conn)

    


