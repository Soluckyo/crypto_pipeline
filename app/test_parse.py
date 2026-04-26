from utils.parse import parse_listings_response

test_json = {
    "status": {"timestamp": "2024-01-15T00:00:00Z", "error_code": 0, "error_message": None, "elapsed": 10, "credit_count": 1},
    "data": [{
        "id": 1, "name": "Bitcoin", "symbol": "BTC", "slug": "bitcoin",
        "cmc_rank": 1, "num_market_pairs": 10000, "circulating_supply": 19500000,
        "total_supply": 21000000, "max_supply": 21000000,
        "last_updated": "2024-01-15T00:00:00Z", "date_added": "2013-04-28T00:00:00Z",
        "tags": ["mineable"], "platform": None,
        "quote": {"USD": {"price": 43000, "volume_24h": 1e10, "volume_change_24h": 2.5,
                         "percent_change_1h": 0.5, "percent_change_24h": -1.2,
                         "percent_change_7d": 5.3, "percent_change_30d": 15.8,
                         "market_cap": 8.5e11, "market_cap_dominance": 48.5,
                         "fully_diluted_market_cap": 9e11, "last_updated": "2024-01-15T00:00:00Z"}}
    }]
}

result = parse_listings_response(test_json)
print(result.data[0].quote["USD"].price)  # Должно вывести 43000.0
print(result.data[0].name)  # Должно вывести "Bitcoin"
print(result.status.error_code)  # Должно вывести 0