{{
    config(
        materialized='table',
        alias='daily_price_trends'
    )
}}


SELECT 
    c.symbol,
    d.full_date,
    f.price_usd,
    f.volume_24h,
    LAG(f.price_usd, 1) OVER (PARTITION BY c.id ORDER BY d.full_date) as prev_day_price,
    ROUND(
        (f.price_usd - LAG(f.price_usd, 1) OVER (PARTITION BY c.id ORDER BY d.full_date)) 
        / NULLIF(LAG(f.price_usd, 1) OVER (PARTITION BY c.id ORDER BY d.full_date), 0) * 100, 
        2
    ) as pct_change
FROM {{ source('dwh', 'fact_market_snapshot') }} f
JOIN {{ source('dwh', 'dim_cryptocurrency') }} c 
    ON f.id_cryptocurrency = c.id
JOIN {{ source('dwh', 'dim_date') }} d 
    ON f.id_date = d.id_date
WHERE d.full_date >= CURRENT_DATE - INTERVAL '7 days'
  AND c.is_current = TRUE
ORDER BY c.symbol, d.full_date