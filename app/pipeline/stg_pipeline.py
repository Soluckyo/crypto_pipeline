from app.logger import get_logger
from typing import Optional
from utils.parse import parse_listings_response
from utils.listings_to_dict import listings_to_dict
from app.extractor.stg_extractor import get_latest_raw_listings, get_raw_listings_by_id
from loader.load_stg import insert_coin_snapshot
from loader.load_raw import update_metadata

logger = get_logger(__name__)

def run_stg_pipeline(raw_id: Optional[int] = None) -> dict:

    if raw_id:
        raw_record = get_raw_listings_by_id(raw_id)
    else:
        raw_record = get_latest_raw_listings()

    if not raw_record:
        error_msg = "Нет данных для трансформации"
        logger.error(error_msg)
        return {"status": "failed", "error": error_msg}

    raw_id = raw_record["id"]
    
    parsed = parse_listings_response(raw_record["raw_data"])

    records = listings_to_dict(parsed)

    inserted_count = insert_coin_snapshot(records, raw_id)

    update_metadata(
        table_name="stg.coin_snapshot",
        status='success',
        rows_loaded=inserted_count,
        last_loaded_id=raw_id
    )

    logger.info(f"Stg pipeline успешно завершен: {inserted_count} записей")
    return {"status": "success", "rows_loaded": inserted_count}


    



