
  
    

  create  table "crypto_pipeline"."mart"."market_overview__dbt_tmp"
  
  
    as
  
  (
    

WITH daily_agg AS (
    SELECT 
        id_date,
        COUNT(DISTINCT id_cryptocurrency) as active_coins,
        SUM(market_cap) as total_market_cap,
        SUM(volume_24h) as total_volume,
        AVG(price_usd) as avg_price
    FROM "crypto_pipeline"."dwh"."fact_market_snapshot"
    GROUP BY id_date
)
SELECT 
    d.full_date,
    a.active_coins,
    a.total_market_cap,
    a.total_volume,
    a.avg_price
FROM daily_agg a
JOIN "crypto_pipeline"."dwh"."dim_date" d 
    ON a.id_date = d.id_date
ORDER BY d.full_date DESC
LIMIT 30
  );
  