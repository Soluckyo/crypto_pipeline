from app.logger import get_logger


logger = get_logger(__name__)

def validate_listings_response(response_data: dict) -> tuple[bool, str|None]:
    # Проверяем:
    # - наличие status и error_code == 0
    # - наличие data
    # - data не пустой список

    is_valid = False
    status = response_data.get("status", {})
    data = response_data.get("data", [])
    error_msg = None
    if status:
        error_code = status.get("error_code")
        if error_code == 0:
            if len(data) != 0:
                is_valid = True
            else:
                error_msg = "поле 'data' пустое, либо отсутствует"
                logger.warning(f"Ошибка валидации: {error_msg}")
        else:
            error_msg = status.get("error_message", "неизвестная ошибка")
            logger.warning(f"Ошибка валидации: {error_code}, {error_msg}")
    else:
        error_msg = "поле 'status' пустое, либо отсутствует"
        logger.warning(f"Ошибка валидации: {error_msg}")

    if is_valid:
        logger.info(f"Валидация прошла успешно, получено: {len(data)} записей")
        return (True, None)
    return (False, f"Ошибка валидации: {error_msg}")