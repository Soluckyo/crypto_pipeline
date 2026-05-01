create table if not exists public.pipeline_metadata(
	id serial primary key,
	table_name varchar(100) not null unique,
	last_loaded_at timestamp,
	last_loaded_id timestamp,
	status varchar(20) default 'pending',
	rows_loaded integer dfault now(),
	errors_message text,
	updated_at timestamp default now()
	);

create index idx_metadata_table_name on pipeline_metadata(table_name);

COMMENT ON TABLE public.pipeline_metadata IS 'Метаданные о загрузках таблиц';

