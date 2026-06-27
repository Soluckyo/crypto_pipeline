CREATE SCHEMA IF NOT EXISTS dwh;

CREATE TABLE IF NOT EXISTS dwh.dim_cryptocurrency(
	id SERIAL PRIMARY KEY,
	coin_id INTEGER NOT NULL,
	name VARCHAR(100) NOT NULL,
	symbol VARCHAR(20) NOT NULL,
	slug VARCHAR(100),
	tags TEXT[],
	cmc_rank INTEGER,
	max_supply DECIMAL(30, 8),
	date_added DATE,
	valid_from TIMESTAMP NOT NULL DEFAULT NOW(),
	valid_to TIMESTAMP,
	is_current BOOLEAN DEFAULT TRUE,
	updated_at TIMESTAMP DEFAULT NOW(),
	loaded_at TIMESTAMP DEFAULT NOW(),
	raw_id INTEGER
	);
	
CREATE INDEX idx_dim_coin_id ON dwh.dim_cryptocurrency(coin_id);
CREATE INDEX idx_dim_is_current ON dwh.dim_cryptocurrency(coin_id) WHERE is_current = TRUE;
CREATE INDEX idx_dim_valid ON dwh.dim_cryptocurrency(valid_from, valid_to);

COMMENT ON TABLE dwh.dim_cryptocurrency IS 'SCD Type 2 таблица с историей изменений криптовалют';
COMMENT ON COLUMN dwh.dim_cryptocurrency.valid_from IS 'Начало периода действия версии';
COMMENT ON COLUMN dwh.dim_cryptocurrency.valid_to IS 'Конец периода действия версии. NULL = текущая';



CREATE TABLE IF NOT EXISTS dwh.dim_date(
	id INTEGER PRIMARY KEY,
	full_date DATE NOT NULL,
	day_of_week INTEGER NOT NULL,
	day_name VARCHAR(10),
	day_of_month INTEGER NOT NULL,
	day_of_year INTEGER NOT NULL,
	week_of_year INTEGER NOT NULL,
	month_number INTEGER NOT NULL,
	month_name VARCHAR(10),
	quarter SMALLINT NOT NULL,
	year SMALLINT NOT NULL,
	is_weekend BOOLEAN DEFAULT FALSE,
	is_holiday BOOLEAN DEFAULT FALSE
	);

CREATE INDEX idx_dim_date_year ON dwh.dim_date(year);
CREATE INDEX idx_dim_date_month ON dwh.dim_date(month_number);



CREATE TABLE IF NOT EXISTS dwh.fact_market_snapshot(
	id SERIAL PRIMARY KEY,
	id_cryptocurrency INTEGER NOT NULL,
	id_date INTEGER NOT NULL,
	price_usd DECIMAL(20, 8) NOT NULL,
	volume_24h DECIMAL(20, 2),
	volume_change_24h DECIMAL(10, 2),
	percent_change_1h DECIMAL(10, 2),
	percent_change_24h DECIMAL(10, 2),
	percent_change_7d DECIMAL(10, 2),
	percent_change_30d DECIMAL(10, 2),
	num_market_pairs INTEGER,
	circulating_supply DECIMAL(30, 8),
	total_supply DECIMAL(30, 8),
	market_cap DECIMAL(20, 2),
	market_cap_dominance DECIMAL(10, 2),
	fully_diluted_market_cap DECIMAL(20, 2),
	extracted_at TIMESTAMP,
	last_updated TIMESTAMP,
	loaded_at TIMESTAMP DEFAULT NOW(),
	raw_id INTEGER,
    
	CONSTRAINT fk_fact_dim FOREIGN KEY (id_cryptocurrency) 
	REFERENCES dwh.dim_cryptocurrency(id),
	
	CONSTRAINT fk_fact_date FOREIGN KEY (id_date)
	REFERENCES dwh.dim_date(id)
	);
		
CREATE INDEX idx_fact_dim_id ON dwh.fact_market_snapshot(id_cryptocurrency);
CREATE INDEX idx_extracted ON dwh.fact_market_snapshot(extracted_at);
CREATE INDEX idx_last_updated ON dwh.fact_market_snapshot(last_updated);

COMMENT ON TABLE dwh.fact_market_snapshot IS 'Cнимки рыночных показателей криптовалюты';
	
 