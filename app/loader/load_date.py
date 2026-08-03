from datetime import datetime, timedelta
from typing import List, Dict

def generate_dim_date(start_date: str = '2026-01-01', end_date: str = '2036-12-31') -> List[Dict]:
    
    start = timedelta.strptime(start_date, '%Y-%m-%d')
    end = timedelta.strptime(end_date, '%Y-%m-%d')

    dates = []
    current = start

    while current <= end:
        date_sk = int(current.strftime('%Y%m%d'))

        dates.append({
            'date_sk': date_sk,
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
            'is_weekend': current.isoweekday() in (6, 7)
        })

        current += timedelta(days=1)
    return dates


def insert_dim_date(dates: List[Dict]) -> int:
    return None
