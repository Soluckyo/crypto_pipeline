from datetime import datetime, timedelta
from typing import List, Dict
from app.logger import get_logger
from app.db import get_connection, release_connection
from psycopg2.extras import execute_values
from holidays_ru import is_holiday


logger = get_logger(__name__)

def generate_dim_date(start_date: str = '2026-01-01', end_date: str = '2036-12-31') -> List[Dict]:
    
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')

    dates = []
    current = start

    while current <= end:
        id_date = int(current.strftime('%Y%m%d'))

        dates.append({
            'id_date': id_date,
            'full_date': current.date(),
            'day_of_week': current.isoweekday(),
            'day_name':current.strftime('%A'),
            'day_of_month': current.day,
            'day_of_year': current.timetuple().tm_yday,
            'week_of_year': current.isocalendar()[1],
            'month_number': current.month,
            'month_name': current.strftime('%B'),
            'quarter': (current.month-1)//3+1,
            'year': current.year,
            'is_weekend': current.isoweekday() in (6, 7),
            'is_holiday': is_holiday(current.date())
        })

        current += timedelta(days=1)
    return dates


def insert_dim_date(dates: List[Dict]) -> int:

    if not dates:
        logger.warning("Нет данных для вставки в dwh.dim_date")
        return 0

    columns = [
        'id_date','full_date','day_of_week','day_name',
        'day_of_month','day_of_year','week_of_year','month_number',
        'month_name','quarter','year','is_weekend','is_holiday'
    ]

    values = [
        [date[col] for col in columns]
        for date in dates
    ]

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            sql = """
                     INSERT INTO dwh.dim_date({})
                     VALUES %s
                     ON CONFLICT (id_date) DO NOTHING;
                  """.format(', '.join(columns))
            
            execute_values(cur, sql, values)
            conn.commit()
            logger.info(f'Вставлено {len(values)} записей в таблицу dwh.dim_date')
            return len(values)
    except Exception as e:
        conn.rollback()
        logger.error(f"Возникла ошибка при вставке в таблицу dwh.dim_date: {e}")
        raise
    finally:
        release_connection(conn)