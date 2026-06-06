from app.logger import get_logger
from typing import Optional
from app.utils.parse import parse_listings_response
from app.utils.listings_to_dict import listings_to_dict
from app.extractor.stg_extractor import get_latest_raw_listings, get_raw_listings_by_id
from app.loader.load_stg import insert_coin_snapshot
from app.loader.load_raw import update_metadata
from app.utils.cleaners import clean_coin_records


logger = get_logger(__name__)

def run_stg_pipeline(raw_id: Optional[int] = None) -> dict:

    if raw_id:
        logger.info(f"Запускаем get_raw_listings_by_id с id {raw_id}")
        raw_record = get_raw_listings_by_id(raw_id)
    else:
        logger.info("Запускаем get_latest_raw_listings")
        raw_record = get_latest_raw_listings()

    if not raw_record:
        error_msg = "Нет данных для трансформации"
        logger.error(error_msg)
        return {"status": "failed", "error": error_msg}

    raw_id = raw_record["id"]
    
    logger.info("Переходим к парсингу строки")
    parsed = parse_listings_response(raw_record["raw_data"])

    logger.info("Преобразуем в словарь")
    records = listings_to_dict(parsed)

    logger.info("Очищаем данные")
    clean_records = clean_coin_records(records=records, method='python')

    logger.info("Вставляем данные в БД")
    inserted_count = insert_coin_snapshot(clean_records, raw_id)

    update_metadata(
        table_name="stg.coin_snapshot",
        status='success',
        rows_loaded=inserted_count,
        last_loaded_id=raw_id
    )

    logger.info(f"Stg pipeline успешно завершен: {inserted_count} записей")
    return {"status": "success", "rows_loaded": inserted_count}


    



