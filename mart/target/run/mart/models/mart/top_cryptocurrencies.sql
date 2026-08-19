
  
    

  create  table "crypto_pipeline"."mart"."top_cryptocurrencies__dbt_tmp"
  
  
    as
  
  (
    

WITH last_snap AS (SELECT f.id, 
						  f.id_cryptocurrency, 
                          dc.symbol,
                          dc.name,
						  f.id_date, 
						  f.market_cap, 
					      f.price_usd, 
						  f.volume_24h,
						  row_number() over(PARTITION BY f.id_cryptocurrency ORDER BY f.last_updated DESC) AS rank
					 FROM "crypto_pipeline"."dwh"."fact_market_snapshot" f
                     JOIN "crypto_pipeline"."dwh"."dim_cryptocurrency" dc 
                       ON dc.id = f.id_cryptocurrency 
					WHERE id_date = (SELECT max(id_date) FROM "crypto_pipeline"."dwh"."fact_market_snapshot")
                      AND dc.is_current = TRUE)
SELECT  lp.id_cryptocurrency,
        lp.symbol,
        lp.name,
        lp.price_usd,
        lp.market_cap,
        lp.volume_24h,
        lp.rank
  FROM last_snap lp
 WHERE lp.rank = 1
 ORDER BY lp.market_cap DESC 
 LIMIT 10
  );
  