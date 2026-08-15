from app.logger import get_logger
from app.extractor.dwh_extractor import get_new_stg_records
from app.loader.load_dim import update_dim_cryptocurrency
from app.loader.load_fact import prepare_fact_records, insert_fact_market_snapshot
from app.loader.load_raw import update_metadata
from app.loader.load_date import generate_dim_date, insert_dim_date

logger = get_logger(__name__)

def run_dwh_pipeline() -> dict:
    table_name="dwh.fact_market_snapshot"
    try:
        logger.info("0. Генерация и вставка дат")
        dates = generate_dim_date()
        insert_dim_date(dates)

        logger.info("1. Получение stg записей")
        stg_records = get_new_stg_records(limit = 10000)
        if not stg_records:
            logger.info("Нет новых данных для dwh")
            return {"status": "skipped", "message": "Нет новых stg записей"}
        
        logger.info("2. Обновление dim_cryptocurrency")
        dim_stats = update_dim_cryptocurrency(stg_records, stg_records[-1]['raw_id'])
        logger.info(f"dim_stats: {dim_stats}")

        logger.info("3. Подготовка фактов")
        fact_records = prepare_fact_records(stg_records, dim_stats['dim_map'])

        logger.info("4. Вставка фактов")
        fact_inserted = insert_fact_market_snapshot(fact_records)

        last_raw_id = stg_records[-1]['raw_id']

        logger.info("5. Обновление metadata")
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
    except Exception as e:
        error_msg = str(e)
        update_metadata(table_name=table_name,
                        status="failed",
                        error_message=str(e),
                        rows_loaded=0)
        return {"status": "failed",
                "error": error_msg}
