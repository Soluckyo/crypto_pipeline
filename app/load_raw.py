import json
from datetime import datetime
from typing import Dict, Any, Optional
from logger import get_logger
from db import get_connection, release_connection

logger = get_logger(__name__)


def save_listings_to_raw(
    response_data: Dict[str, Any],
    validation_status: str = 'pending',
    validation_error: Optional[str] = None
) -> int:
    

    status = response_data.get("status")
    if status:
        timestamp_str = status.get("timestamp")
        if timestamp_str:
            api_timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        else:
            api_timestamp = None
    else:
        api_timestamp = None


    json_data = json.dumps(response_data)
    
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql =   """
                        INSERT INTO raw.crypto_listings(raw_data, validation_status, validation_error, api_timestamp)
                        VALUES(%s, %s, %s, %s)
                        RETURNING id;
                    """
            cursor.execute(sql, 
                           (json_data, validation_status, validation_error, api_timestamp))
            conn.commit()
            inserted_id = cursor.fetchone()[0]

            logger.info(f"Данные сохранены в raw.crypto_listings с ID {inserted_id}")
            return inserted_id
    except Exception as e:
        conn.rollback()
        logger.error(f"Возникла ошибка при сохранении: {e}")
        raise
    finally:
        release_connection(conn)


def update_metadata(
        table_name: str,
        status: str,
        rows_loaded: int = 0,
        last_loaded_id: Optional[int] = None,
        error_message: Optional[str] = None 
) -> None:
    if status == 'success':
        last_loaded_at = datetime.now()
        logger.info(f"Успешная загрузка {table_name}: {rows_loaded} строк")
    else:
        last_loaded_at= None
        logger.error(f"Ошибка загрузки {table_name}: {error_message}")

    conn = get_connection()
    try:
        with conn.cursor() as cursor:

            sql =   """
                        INSERT INTO public.pipeline_metadata(table_name, last_loaded_at, last_loaded_id, status, rows_loaded, error_message, updated_at)
                        VALUES(%s, %s, %s, %s, %s, %s, now())
                        ON CONFLICT(table_name) DO UPDATE
                        SET last_loaded_at = COALESCE(EXCLUDED.last_loaded_at, pipeline_metadata.last_loaded_at),
                            last_loaded_id = EXCLUDED.last_loaded_id,
                            status = EXCLUDED.status,
                            rows_loaded = EXCLUDED.rows_loaded,
                            error_message = EXCLUDED.error_message,
                            updated_at = EXCLUDED.updated_at
                    """
            cursor.execute(sql, 
                           (table_name, last_loaded_at, last_loaded_id, status, rows_loaded, error_message))
            conn.commit()
            logger.info(f"Данные записаны в public.pipeline_metadata")
    except Exception as e:
        conn.rollback()
        logger.error(f"Возникла ошибка при обновлении pipeline_metadata: {e}")
        raise
    finally:
        release_connection(conn)