from app.logger import get_logger
from app.extractor.cmc_extractor import fetch_listings
from app.loader.load_raw import save_listings_to_raw, update_metadata
from app.validator.cmc_validator import validate_listings_response

logger = get_logger(__name__)

def run_dwh_pipeline(limit: int = 100) -> dict:
    