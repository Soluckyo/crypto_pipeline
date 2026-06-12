from typing import List, Dict, Any
from psycopg2.extras import execute_values
from app.logger import get_logger
from app.db import get_connection, release_connection
from datetime import datetime


logger = get_logger(__name__)

def insert_coin_snapshot(records: List[Dict[str, Any]], raw_id: int) -> int:

    for record in records:
        record['extracted_at'] = datetime.now()
        record['raw_id'] = raw_id

    columns = [
        'coin_id', 'name', 'symbol', 'slug', 'cmc_rank', 'num_market_pairs',
        'circulating_supply', 'total_supply', 'max_supply', 'last_updated', 
        'date_added', 'price_usd', 'volume_24h', 'volume_change_24h', 
        'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 
        'percent_change_30d', 'market_cap', 'market_cap_dominance', 
        'fully_diluted_market_cap', 'tags', 'platform', 'extracted_at', 'raw_id'
    ]

    values = [
        [record[col] for col in columns]
        for record in records
    ]

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            sql = """
                    INSERT INTO stg.coin_snapshot({})
                    VALUES %s
                """.format(', '.join(columns))
            
            execute_values(cur, sql, values)
            conn.commit()

            logger.info(f"Вставлено {len(values)} записей в stg.coin_snapshot")
            return len(values)
    except Exception as e:
        conn.rollback()
        logger.error(f"Возникла ошибка при вставке: {e}")
        raise
    finally:
        release_connection(conn)
