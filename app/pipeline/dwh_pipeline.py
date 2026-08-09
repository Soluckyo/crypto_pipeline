from app.logger import get_logger
from app.extractor.dwh_extractor import get_new_stg_records
from app.loader.load_dim import update_dim_cryptocurrency
from app.loader.load_fact import prepare_fact_records, insert_fact_market_snapshot
from app.loader.load_raw import update_metadata

logger = get_logger(__name__)

def run_dwh_pipeline() -> dict:

    stg_records = get_new_stg_records(int = 10000)
    if not stg_records:
        logger.info("Нет новых данных для dwh")
        return {"status": "skipped", "message": "Нет новых stg записей"}
    
    dim_stats = update_dim_cryptocurrency(stg_records, stg_records[-1]['raw_id'])

    fact_records = prepare_fact_records(stg_records, dim_stats['dim_map'])
    fact_inserted = insert_fact_market_snapshot(fact_records)

    last_raw_id = stg_records[-1]['raw_id']

    update_metadata(
        table_name='dwh.dim_cryptocurrency',
        status='success',
        rows_loaded=dim_stats['inserted'] + dim_stats['updated'],
        last_loaded_id=last_raw_id
    )

    update_metadata(
        table_name='dwh.fact_market_snapshot',
        status='success',
        rows_loaded=fact_inserted,
        last_loaded_id=last_raw_id
    )

    logger.info(
        f"DWH загрузка завершена: "
        f"dim (inserted={dim_stats['inserted']}, updated={dim_stats['updated']}), "
        f"fact={fact_inserted}"
    )

    return {
        "status": "success",
        "dim": dim_stats,
        "fact_inserted": fact_inserted,
        "last_raw_id": last_raw_id
    }
