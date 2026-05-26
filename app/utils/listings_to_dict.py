from schemas.cmc_listings import Status, QuoteUsd, CryptoCurrency, ListingsResponse
from collections import namedtuple
from datetime import datetime
from typing import Dict, Any, List

def listings_to_dict(response: ListingsResponse) -> List[Dict[str, Any]]:
    result = []

    for crypto in response.data:
        quote_usd = crypto.quote.get("USD", {})

        record = {
            "coin_id": crypto.id,
            "name": crypto.name,
            "symbol": crypto.symbol,
            "slug": crypto.slug,
            "cmc_rank": crypto.cmc_rank,
            "num_market_pairs": crypto.num_market_pairs,
            "circulating_supply": crypto.circulating_supply,
            "total_supply": crypto.total_supply,
            "max_supply": crypto.max_supply,
            "last_updated": crypto.last_updated,
            "date_added": crypto.date_added,
            "price_usd": quote_usd.price,
            "volume_24h": quote_usd.volume_24h,
            "volume_change_24h": quote_usd.volume_change_24h,
            "percent_change_1h": quote_usd.percent_change_1h,
            "percent_change_24h": quote_usd.percent_change_24h,
            "percent_change_7d": quote_usd.percent_change_7d,
            "percent_change_30d": quote_usd.percent_change_30d,
            "market_cap": quote_usd.market_cap,
            "market_cap_dominance": quote_usd.market_cap_dominance,
            "fully_diluted_market_cap": quote_usd.fully_diluted_market_cap,
            "tags": crypto.tags,
            "platform": crypto.platform 
        }
        result.append(record)
    return result


