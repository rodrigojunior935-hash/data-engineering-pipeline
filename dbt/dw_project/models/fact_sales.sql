{{ config(materialized='incremental') }}

select
    category,
    avg(price) as avg_price,
    count(*) as total_sales
from {{ source('staging', 'sales') }}
group by category
