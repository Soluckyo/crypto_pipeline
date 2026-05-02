create schema if not exists raw;

create table if not exists raw.crypto_listings(
	id serial primary key,
	raw_data JSONB not null,
	validation_status varchar(20) default 'pending',
	validation_error text ,
	loaded_at timestamp default now(),
	api_timestamp timestamp
	);

create index idx_raw_listings_status on raw.crypto_listings(validation_status);

COMMENT ON TABLE raw.crypto_listings IS 'Сырые данные от API /listings/latest';
COMMENT ON COLUMN raw.crypto_listings.raw_data IS 'Полный JSON ответ от CoinMarketCap';
COMMENT ON COLUMN raw.crypto_listings.validation_status IS 'Статус валидации: pending/valid/failed';