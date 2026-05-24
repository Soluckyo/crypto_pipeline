from app.extractor.cmc_extractor import fetch_listings
from logger import get_logger

def test_connection():
    """Тест 1: Проверяем, что можем подключиться к API"""
    print("=" * 50)
    print("ТЕСТ 1: Проверка подключения к API")
    print("=" * 50)
    
    try:
        # Пробуем получить всего 5 монет для быстрого теста
        data = fetch_listings(limit=5)
        
        # Проверяем структуру ответа
        assert "status" in data, "Нет поля 'status' в ответе"
        assert "data" in data, "Нет поля 'data' в ответе"
        
        status = data["status"]
        assert status.get("error_code") == 0, f"API вернул ошибку: {status.get('error_message')}"
        
        crypto_list = data["data"]
        assert len(crypto_list) > 0, "Список криптовалют пуст"
        
        print(f"✅ Успешно подключились к API")
        print(f"   Получено монет: {len(crypto_list)}")
        print(f"   Timestamp ответа: {status.get('timestamp')}")
        
        return True, crypto_list
        
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False, None

def test_data_structure(crypto_list):
    """Тест 2: Проверяем структуру данных"""
    print("\n" + "=" * 50)
    print("ТЕСТ 2: Проверка структуры данных")
    print("=" * 50)
    
    if not crypto_list:
        print("❌ Нет данных для проверки")
        return False
    
    try:
        # Берем первую монету для проверки
        first_coin = crypto_list[0]
        
        # Проверяем обязательные поля
        required_fields = ["id", "name", "symbol", "quote"]
        for field in required_fields:
            assert field in first_coin, f"Отсутствует поле '{field}' в данных монеты"
        
        # Проверяем структуру quote
        quote = first_coin.get("quote", {})
        assert "USD" in quote, "Нет котировки в USD"
        
        usd_quote = quote["USD"]
        price_fields = ["price", "volume_24h", "market_cap"]
        for field in price_fields:
            assert field in usd_quote, f"Отсутствует поле '{field}' в котировке USD"
        
        print(f"✅ Структура данных корректна")
        print(f"   Пример: {first_coin['name']} ({first_coin['symbol']})")
        print(f"   Цена: ${usd_quote['price']:.2f}")
        print(f"   Рыночная капитализация: ${usd_quote['market_cap']:,.0f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка в структуре данных: {e}")
        return False

def test_different_limits():
    """Тест 3: Проверяем работу с разными лимитами"""
    print("\n" + "=" * 50)
    print("ТЕСТ 3: Проверка параметра limit")
    print("=" * 50)
    
    limits = [1, 5, 10]
    
    for limit in limits:
        try:
            data = fetch_listings(limit=limit)
            received_count = len(data.get("data", []))
            
            assert received_count == limit, f"Ожидалось {limit} монет, получено {received_count}"
            print(f"✅ limit={limit}: получено {received_count} монет")
            
        except Exception as e:
            print(f"❌ limit={limit}: ошибка - {e}")
            return False
    
    return True

def print_sample_data(crypto_list):
    """Тест 4: Показываем пример данных (красиво)"""
    print("\n" + "=" * 50)
    print("ТЕСТ 4: Пример полученных данных")
    print("=" * 50)
    
    print(f"\n{'ID':<5} {'Symbol':<8} {'Name':<20} {'Price (USD)':<15} {'Market Cap (USD)':<20}")
    print("-" * 75)
    
    for coin in crypto_list[:5]:  # Показываем первые 5
        coin_id = coin.get("id", "N/A")
        symbol = coin.get("symbol", "N/A")
        name = coin.get("name", "N/A")[:18]  # Обрезаем длинные имена
        
        quote = coin.get("quote", {}).get("USD", {})
        price = quote.get("price", 0)
        market_cap = quote.get("market_cap", 0)
        
        print(f"{coin_id:<5} {symbol:<8} {name:<20} ${price:<14.2f} ${market_cap:<19,.0f}")

def main():
    print("\n🚀 Начинаем тестирование API клиента CoinMarketCap\n")
    
    # Тест 1: Подключение
    success, crypto_list = test_connection()
    if not success:
        print("\n❌ Тестирование прервано: не удалось подключиться к API")
        print("\nПроверьте:")
        print("  1. Файл .env существует и содержит API_KEY")
        print("  2. API_KEY валидный (не истек и не заблокирован)")
        print("  3. Есть интернет соединение")
        sys.exit(1)
    
    # Тест 2: Структура
    if not test_data_structure(crypto_list):
        print("\n❌ Тестирование прервано: неверная структура данных")
        print("Возможно API изменило формат ответа")
        sys.exit(1)
    
    # Тест 3: Разные лимиты
    if not test_different_limits():
        print("\n❌ Тестирование прервано: проблема с параметром limit")
        sys.exit(1)
    
    # Тест 4: Пример данных
    print_sample_data(crypto_list)
    
    print("\n" + "=" * 50)
    print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
    print("=" * 50)
    print("\nAPI клиент готов к использованию в DAG.")
    print("Можно переходить к созданию таблиц и load_raw.")

if __name__ == "__main__":
    main()