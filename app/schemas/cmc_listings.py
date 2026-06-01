from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any

@dataclass
class Status:
    timestamp: datetime
    error_code: int
    error_message: Optional[str]
    elapsed: int
    credit_count: int

@dataclass
class QuoteUsd:
    price: float
    volume_24h: float
    volume_change_24h: float
    percent_change_1h: float
    percent_change_24h: float
    percent_change_7d: float
    percent_change_30d: float
    market_cap: float
    market_cap_dominance: float
    fully_diluted_market_cap: float
    last_updated: datetime

@dataclass
class CryptoCurrency:
    id: int
    name: str
    symbol: str
    slug: str
    cmc_rank: int
    num_market_pairs: int
    circulating_supply: float
    total_supply: Optional[float]
    max_supply: Optional[float]
    last_updated: datetime
    date_added: datetime
    tags: List[str]
    platform: Optional[Dict[str, Any]]
    quote: Dict[str, QuoteUsd]

@dataclass
class ListingsResponse:
    status: Status
    data: List[CryptoCurrency]