-- Use the `ref` function to select from other models

select *
from "crypto_pipeline"."mart"."my_first_dbt_model"
where id = 1