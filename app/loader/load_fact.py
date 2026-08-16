from datetime import datetime, timedelta
from typing import List, Dict
from app.logger import get_logger
from app.db import get_connection, release_connection
from psycopg2.extras import execute_values
from typing import Optional


logger = get_logger(__name__)

def prepare_fact_records(stg_records: List[Dict], dim_map: Dict[int, int]) -> List[Dict]:

    fact_records = []
    fact_fields = [
        'price_usd', 'volume_24h', 'volume_change_24h',
        'percent_change_1h', 'percent_change_24h', 'percent_change_7d',
        'percent_change_30d', 'num_market_pairs',
        'circulating_supply', 'total_supply',
        'market_cap', 'market_cap_dominance', 'fully_diluted_market_cap',
        'last_updated'
    ]

    for record in stg_records:
        coin_id = record['coin_id']
        dim_id = dim_map.get(coin_id)

        if not dim_id:
            logger.warning(f"Нет dim_id для coin_id={coin_id}")
            continue

        last_updated = record.get('last_updated')
        if last_updated:
            id_date = int(last_updated.strftime('%Y%m%d'))
        else:
            extracted_at = record.get('extracted_at')
            id_date = int(extracted_at.strftime('%Y%m%d'))

    
        fact_record = {
            'id_cryptocurrency': dim_id,
            'id_date': id_date,
        }
        
        #копирование из stg
        for field in fact_fields:
            fact_record[field] = record.get(field)       

        fact_record['extracted_at'] = record.get('extracted_at')
        fact_record['raw_id'] = record.get('raw_id')
        
        fact_records.append(fact_record)
    
    logger.info(f"Подготовлено {len(fact_records)} записей для fact_market_snapshot")
    return fact_records

        
def insert_fact_market_snapshot(fact_records: List[Dict]) -> int:
    if not fact_records:
        logger.warning("Нет данных для вставки в dwh.fact_market_snapshot")
        return 0

    columns = [
        'id_cryptocurrency', 'id_date', 'price_usd', 'volume_24h', 
        'volume_change_24h', 'percent_change_1h', 'percent_change_24h', 
        'percent_change_7d', 'percent_change_30d', 'num_market_pairs',
        'circulating_supply', 'total_supply',
        'market_cap', 'market_cap_dominance', 'fully_diluted_market_cap',
        'extracted_at', 'last_updated', 'raw_id'
    ]

    values = [
        [record[col] for col in columns]
        for record in fact_records
    ]

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            sql = """
                     INSERT INTO dwh.fact_market_snapshot({})
                     VALUES %s
                  """.format(', '.join(columns))
            
            execute_values(cur, sql, values)
            conn.commit()
            logger.info(f"Вставлено {len(values)} записей в таблицу dwh.fact_market_snapshot")
            return len(values)
            
    except Exception as e:
        conn.rollback()
        logger.error(f"Ошибка при вставке в dwh.fact_market_snapshot: {e}")
        raise
    finally:
        release_connection(conn)
