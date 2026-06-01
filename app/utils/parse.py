from app.schemas.cmc_listings import Status, QuoteUsd, CryptoCurrency, ListingsResponse
from collections import namedtuple
from datetime import datetime
from typing import Dict, Any, List

def parse_listings_response(json_data: list) -> ListingsResponse:
    status = json_data.get("status", {})

    timestamp_str = status.get("timestamp")
    if timestamp_str:
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    else:
        timestamp = datetime.now()

    status_obj = Status(
            timestamp = timestamp,
            error_code = status.get("error_code", 0),
            error_message = status.get("error_message"),
            elapsed = status.get("elapsed", 0),
            credit_count = status.get("credit_count", 0)
    )


    data = json_data.get("data", [])
    crypto_list: List[CryptoCurrency]= []

    for item in data:
        quote_data = item.get("quote", {}).get("USD", {})

        quote_last_updated_str = quote_data.get("last_updated")
        if quote_last_updated_str:
            quote_last_updated = datetime.fromisoformat(quote_last_updated_str.replace('Z', '+00:00'))
        else:
            quote_last_updated = datetime.now()

        quote_obj = QuoteUsd(
                price = quote_data.get("price", 0.0),
                volume_24h = quote_data.get("volume_24h", 0.0),
                volume_change_24h = quote_data.get("volume_change_24h", 0.0),
                percent_change_1h = quote_data.get("percent_change_1h", 0.0),
                percent_change_24h = quote_data.get("percent_change_24h", 0.0),
                percent_change_7d = quote_data.get("percent_change_7d", 0.0),
                percent_change_30d = quote_data.get("percent_change_30d", 0.0),
                market_cap = quote_data.get("market_cap", 0.0),
                market_cap_dominance = quote_data.get("market_cap_dominance", 0.0),
                fully_diluted_market_cap = quote_data.get("fully_diluted_market_cap", 0.0),
                last_updated = quote_last_updated
        )

        last_updated_str = item.get("last_updated")
        if last_updated_str:
            last_updated = datetime.fromisoformat(last_updated_str.replace('Z', '+00:00'))
        else:
            last_updated = datetime.now()

        date_added_str = item.get("date_added")
        if date_added_str:
            date_added = datetime.fromisoformat(date_added_str.replace('Z', '+00:00'))
        else:
            date_added = None

        crypto_obj = CryptoCurrency(
            id = item.get("id", []),
            name = item.get("name", []),
            symbol = item.get("symbol", []),
            slug = item.get("slug", []),
            cmc_rank = item.get("cmc_rank", []),
            num_market_pairs = item.get("num_market_pairs", []),
            circulating_supply = item.get("circulating_supply", []),
            total_supply = item.get("total_supply", []),
            max_supply = item.get("max_supply", []),
            last_updated = last_updated,
            date_added = date_added,
            tags = item.get("tags", {}),
            platform = item.get("platform", []),
            quote = {"USD": quote_obj}
        )
        crypto_list.append(crypto_obj)

    return ListingsResponse(status = status_obj, data = crypto_list)