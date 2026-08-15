from datetime import datetime
from typing import List, Dict
from app.logger import get_logger
from app.db import get_connection, release_connection
from psycopg2.extras import execute_values
from typing import Optional

logger = get_logger(__name__)

def get_current_dim_version(coin_id: int) -> Optional[Dict]:

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            sql = """
                     SELECT id, coin_id, name, symbol, slug, 
                            cmc_rank, max_supply, date_added,
                            valid_from, valid_to, is_current, raw_id
                       FROM dwh.dim_cryptocurrency
                      WHERE coin_id = %s
                        and is_current = true
                  """
            
            cur.execute(sql, (coin_id,))
            current_coin_id = cur.fetchone()

            if not current_coin_id:
                logger.warning(f"Нет актуальной записи значений монеты с id: {coin_id}")
                return None
            
            return {
                "id": current_coin_id[0],
                "coin_id": current_coin_id[1], 
                "name": current_coin_id[2],
                "symbol": current_coin_id[3],
                "slug": current_coin_id[4],
                "cmc_rank": current_coin_id[5],
                "max_supply": current_coin_id[6], 
                "date_added": current_coin_id[7], 
                "valid_from": current_coin_id[8], 
                "valid_to": current_coin_id[9], 
                "is_current": current_coin_id[10], 
                "raw_id": current_coin_id[11]
            }
    except Exception as e:
        logger.error(f"Ошибка при получении актуальной записи монеты с ID: {coin_id}. Ошибка: {e}")
        raise
    finally:
        release_connection(conn)


def insert_new_dim_version(record: Dict, raw_id: int) -> int:
    conn = get_connection()

    columns = [
        'coin_id', 'name', 'symbol', 'slug', 
        'cmc_rank', 'max_supply', 'date_added',
        'valid_from', 'valid_to', 'is_current', 'raw_id'
    ]

    date_added = record.get('date_added')
    if date_added and isinstance(date_added, str):
        try:
            date_added = datetime.strptime(date_added, '%Y-%m-%d').date()
        except ValueError:
            date_added = None

    values = [
        record.get('coin_id'),
        record.get('name'),
        record.get('symbol'),
        record.get('slug'),
        record.get('cmc_rank'),
        record.get('max_supply'),
        date_added,
        datetime.now(),
        None,            
        True,
        raw_id
    ]

    try:
        with conn.cursor() as cur:
            sql = """
                     INSERT INTO dwh.dim_cryptocurrency({})
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                     RETURNING id;
                  """.format(', '.join(columns))
            
            cur.execute(sql, values)
            inserted_id = cur.fetchone()[0]
            conn.commit()
            logger.info("Успешно добавлена новая версия монеты в dwh.dim_cryptocurrency")
            return inserted_id
    except Exception as e:
        conn.rollback()
        logger.error(f"Ошибка при добавлении новой версии монеты в dwh.dim_cryptocurrency: {e}")
        raise
    finally:
        release_connection(conn)


def close_dim_version(id_pk):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            sql = """
                     UPDATE dwh.dim_cryptocurrency
                     SET is_current = false, valid_to = NOW()
                     WHERE id = %s;
                  """
            cur.execute(sql, (id_pk,))
            conn.commit()
            logger.info(f"Версия dim_cryptocurrency (id={id_pk}) закрыта")
    except Exception as e:
        conn.rollback()
        logger.error(f"Ошибка при закрытии версии dim_cryptocurrency (id={id_pk}): {e}")
        raise
    finally:
        release_connection(conn)

def update_dim_cryptocurrency(stg_records: List[Dict], raw_id: int) -> Dict:
    #cdc type 2

    statistics = {"inserted": 0, "updated": 0, "skipped": 0, "dim_map": {}}

    for record in stg_records:
        coin_id = record['coin_id']
        current = get_current_dim_version(coin_id)

        if not current:
            logger.info('Нет актуальной монеты поэтому добавляем текущую')
            new_id = insert_new_dim_version(record, raw_id)
            statistics["inserted"] += 1
            statistics['dim_map'][coin_id] = new_id
            logger.info(f"Новая монета: {record['symbol']} (coin_id={coin_id})")
            continue

        changed = (
            current['name'] != record.get('name') or
            current['symbol'] != record.get('symbol') or
            current['cmc_rank'] != record.get('cmc_rank') or
            current['max_supply'] != record.get('max_supply')
        )

        if not changed:
            statistics['skipped'] += 1
            statistics['dim_map'][coin_id] = current['id']
            continue

        close_dim_version(current['id'])
        new_id = insert_new_dim_version(record, raw_id)
        statistics['updated'] += 1
        statistics['dim_map'][coin_id] = new_id
        logger.info(f"Обновлена монета {record['symbol']}: {current['cmc_rank']} → {record['cmc_rank']}")


        logger.info(
            f"dim_cryptocurrency: inserted={statistics['inserted']}, "
            f"updated={statistics['updated']}, skipped={statistics['skipped']}"
        )

    return statistics