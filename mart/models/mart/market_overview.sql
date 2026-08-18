{{
    config(
        materialized='table',
        schema='mart',
        alias='market_overview'
    )
}}

WITH daily_agg AS (
    SELECT 
        date_sk,
        COUNT(DISTINCT id_cryptocurrency) as active_coins,
        SUM(market_cap) as total_market_cap,
        SUM(volume_24h) as total_volume,
        AVG(price_usd) as avg_price
    FROM {{ source('dwh', 'fact_market_snapshot') }}
    GROUP BY date_sk
)
SELECT 
    d.full_date,
    a.active_coins,
    a.total_market_cap,
    a.total_volume,
    a.avg_price
FROM daily_agg a
JOIN {{ source('dwh', 'dim_date') }} d 
    ON a.date_sk = d.date_sk
ORDER BY d.full_date DESC
LIMIT 30