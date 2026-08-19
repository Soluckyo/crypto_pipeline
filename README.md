# Crypto Pipeline

ETL/ELT пайплайн для загрузки и трансформации данных о криптовалютах из CoinMarketCap API. Проект реализует полную архитектуру хранилища данных с оркестрацией, трансформацией и BI-визуализацией.

<H3>Технологии</H3>
Docker - контейнеризация<br>
Apache Airflow - оркестрация<br>
PostgreSQL - хранение данных<br>
dbt - трансформации (слой витрин)<br>
Metabase - BI-визуализация<br>
Python - кастомная ETL-логика<br>

<H3>Архитектура</H3>
API CoinMarketCap > RAW слой (сырые JSON) > STG слой (очищенные данные) > DWH слой (звезда: измерения + факты) > MART слой (агрегированные витрины через dbt) > Metabase (дашборды)

<H3>Настройка</H3>
Клонировать репозиторий.

Создать файл .env с необходимыми переменными:
DB_USER=...
DB_PASSWORD=...
API_KEY=ваш_ключ_coinmarketcap

Собрать и запустить контейнеры:
docker-compose up -d

<H3>Доступ к сервисам:</H3>
Airflow UI: http://localhost:8080
Metabase: http://localhost:3000

<H3>Выполнение пайплайна</H3>
DAG crypto_pipeline в Airflow состоит из четырёх задач:

load_raw – получение данных из API и сохранение сырых JSON в raw-слой.

load_stg – парсинг и очистка данных в staging-таблицы.

load_dwh – обновление измерений (SCD Type 2) и фактов.

load_mart – запуск dbt-моделей для материализации витрин.

<H3>Модели dbt</H3>
Слой витрин включает следующие таблицы:

top_cryptocurrencies – топ-10 монет по рыночной капитализации<br>
daily_price_trends – дневная динамика цен за последние 7 дней<br>
market_overview – агрегированные метрики рынка

Запуск dbt вручную:
docker exec -it airflow_crypto dbt run --project-dir /opt/airflow/mart --profiles-dir /opt/airflow/mart

Дашборды в Metabase
После подключения Metabase к базе crypto_pipeline можно создавать дашборды из таблиц схемы mart. Данные обновляются автоматически при каждом запуске пайплайна.
