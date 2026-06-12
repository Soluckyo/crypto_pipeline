create table if not exists public.pipeline_metadata(
	id serial primary key,
	table_name varchar(100) not null unique,
	last_loaded_at timestamp,
	last_loaded_id integer,
	status varchar(20) default 'pending',
	rows_loaded integer default 0,
	error_message text,
	updated_at timestamp default now()
	);

create index idx_metadata_table_name on pipeline_metadata(table_name);

COMMENT ON TABLE public.pipeline_metadata IS 'Метаданные о загрузках таблиц';

CREATE TABLE public.anomaly_log (
    id SERIAL PRIMARY KEY,
    anomaly_type VARCHAR(50) NOT NULL,  -- negative_price, missing_field, price_spike, volume_spike
    severity VARCHAR(20) NOT NULL,      -- error, warning, info
    coin_id INTEGER,
    symbol VARCHAR(20),
    field_name VARCHAR(50),
    expected_value DECIMAL(20, 8),
    actual_value DECIMAL(20, 8), 
    raw_id INTEGER,
    stg_id INTEGER,
    raw_record JSONB,
    message TEXT NOT NULL,
    detected_at TIMESTAMP DEFAULT NOW(),
    resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP,
    resolution_note TEXT
);

CREATE INDEX idx_anomaly_detected ON public.anomaly_log(detected_at);
CREATE INDEX idx_anomaly_coin ON public.anomaly_log(coin_id);
CREATE INDEX idx_anomaly_type ON public.anomaly_log(anomaly_type);
CREATE INDEX idx_anomaly_unresolved ON public.anomaly_log(resolved) WHERE resolved = false;

COMMENT ON TABLE public.anomaly_log IS 'Лог аномалий и критических ошибок при обработке данных';
COMMENT ON COLUMN public.anomaly_log.anomaly_type IS 'Тип: negative_price, missing_field, price_spike, volume_spike';
COMMENT ON COLUMN public.anomaly_log.severity IS 'Серьезность: error (исправлено), warning (требует внимания)';
COMMENT ON COLUMN public.anomaly_log.resolved IS 'Проблема решена (для warning)';