from typing import List, Dict, Any
from app.logger import get_logger
from app.db import get_connection, release_connection
from datetime import datetime

logger = get_logger(__name__)

def get_id_last_loaded_stg():
    conn = get_connection()

    try:
        with conn.cursor() as cursor:
            sql = """
                    SELECT last_loaded_id 
                      FROM public.pipeline_metadata
                     WHERE table_name = 'stg.coin_snapshot'
                       AND status = 'success';
                  """
            
            cursor.execute(sql)
            result = cursor.fetchone()
            last_loaded_id = result[0] if result else 0
            
            logger.info(f"Данные о последней загрузке извлечены. ID: {last_loaded_id}")
            return last_loaded_id
    except Exception as e:
        logger.error(f"Возникла ошибка при извлечении ID последней загрузки: {e}")
        raise
    finally:
        release_connection(conn)


def get_new_stg_records(limit: int = 1000) -> List[Dict[str, Any]]:
    conn = get_connection()

    last_loaded_id = get_id_last_loaded_stg()

    try:
        with conn.cursor() as cursor:
            sql = """
                    SELECT *
                      FROM stg.coin_snapshot
                     WHERE raw_id > %s
                     ORDER BY raw_id, id
                     LIMIT %s
                  """
            
            cursor.execute(sql, (last_loaded_id, limit))
            rows = cursor.fetchall()

            if not rows:
                logger.info(f"Нет новых записей (raw_id > {last_loaded_id})")
                return []
            
            columns = [desc[0] for desc in cursor.description]
            records = [dict(zip(columns, row)) for row in rows]

            logger.info(
                f"Получено {len(records)} записей из stg"
                f"(raw_id от {records[0]['raw_id']} до {records[-1]['raw_id']})"
            )
            return records

    except Exception as e:
        logger.error(f"Возникла ошибка при обращении к БД: {e}")
        raise
    finally:
        release_connection(conn)