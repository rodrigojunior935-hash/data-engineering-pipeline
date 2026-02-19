
select distinct
    category as category_name
from {{ source('staging', 'sales') }}

