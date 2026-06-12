CREATE SCHEMA IF NOT EXISTS stg;

CREATE TABLE IF NOT EXISTS stg.coin_snapshot (
    id SERIAL PRIMARY KEY,
    coin_id INTEGER NOT NULL,
    name VARCHAR(100),
    symbol VARCHAR(20),
    slug VARCHAR(100),
    cmc_rank INTEGER,
    num_market_pairs INTEGER,
    circulating_supply DECIMAL(30, 8),
    total_supply DECIMAL(30, 8),
    max_supply DECIMAL(30, 8),
    last_updated TIMESTAMP,
    date_added TIMESTAMP,
    price_usd DECIMAL(20, 8),
    volume_24h DECIMAL(20, 2),
    volume_change_24h DECIMAL(10, 2),
    percent_change_1h DECIMAL(10, 2),
    percent_change_24h DECIMAL(10, 2),
    percent_change_7d DECIMAL(10, 2),
    percent_change_30d DECIMAL(10, 2),
    market_cap DECIMAL(20, 2),
    market_cap_dominance DECIMAL(10, 2),
    fully_diluted_market_cap DECIMAL(20, 2),
    tags TEXT[],
    platform JSONB,  -- может быть null или объект
    extracted_at TIMESTAMP DEFAULT NOW(),
    raw_id INTEGER REFERENCES raw.crypto_listings(id)
);

CREATE INDEX idx_stg_coin_snapshot_coin_id ON stg.coin_snapshot(coin_id);
CREATE INDEX idx_stg_coin_snapshot_extracted_at ON stg.coin_snapshot(extracted_at);