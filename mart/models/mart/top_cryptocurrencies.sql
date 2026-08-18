{{
    config(
        materialized = 'table',
        schema = 'mart',
        alias = 'top_cryptocurrencies'
    )
}}

WITH last_snap AS (SELECT f.id, 
						  f.id_cryptocurrency, 
						  f.id_date, 
						  f.market_cap, 
					      f.price_usd, 
						  f.volume_24h,
						  row_number() over(ORDER BY f.market_cap DESC) AS rank
					 FROM {{SOURCE('dwh', 'fact_market_snapshot')}} f
					WHERE id_date = (SELECT max(id_date) FROM {{SOURCE('dwh', 'fact_market_snapshot')}}))
SELECT  lp.id_cryptocurrency,
        dc.symbol,
        dc.name,
        lp.price_usd,
        lp.market_cap,
        lp.volume_24h,
        lp.rank
  FROM last_snap lp
  JOIN {{SOURCE('dwh', 'dim_cryptocurrency')}} dc ON dc.id = lp.id_cryptocurrency 
 WHERE dc.is_current = TRUE
 ORDER BY lp.rank ASC 
 LIMIT 10