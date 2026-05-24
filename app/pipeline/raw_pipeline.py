from app.logger import get_logger
from app.extractor.cmc_extractor import fetch_listings
from app.loader.load_raw import save_listings_to_raw, update_metadata
from app.validator.cmc_validator import validate_listings_response

logger = get_logger(__name__)

def run_raw_pipeline(limit: int = 100) -> dict:
    table_name = "raw.crypto_listings"

    try:
        data = fetch_listings(limit=limit)

        is_valid, err_msg = validate_listings_response(data)

        inserted_id = save_listings_to_raw(response_data=data, 
                                           validation_status='valid' if is_valid else 'failed',
                                           validation_error=err_msg)
        
        rows_loaded = len(data.get("data", [])) if isinstance(data, dict) else 0

        if is_valid:
            update_metadata(table_name=table_name,
                            status="success",
                            rows_loaded=rows_loaded,
                            last_loaded_id=inserted_id)
            logger.info(f"Row pipeline успешно отработал: {rows_loaded} строк загружено")
            return {"status": "success",
                    "rows_loaded": rows_loaded,
                    "inserted_id": inserted_id}
        else:
            update_metadata(table_name=table_name,
                            status="failed",
                            error_message=err_msg,
                            rows_loaded=rows_loaded)
            logger.error(f"Row pipeline завершен с ошибкой валидации: {err_msg}")
            return{"status": "failed",
                   "rows_loaded": rows_loaded,
                   "inserted_id": inserted_id,
                   "error_message": err_msg}
    except Exception as e:
        error_msg = str(e)
        update_metadata(table_name=table_name,
                        status="failed",
                        error_message=str(e),
                        rows_loaded=0)
        return {"status": "failed",
                "error": error_msg}
        raise