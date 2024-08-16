-- WHAT IS THE AVERAGE DELIVERY TIME FOR ORDERS
select 
    * 
from
     {{ ref('fct_bq_avg_delivery_time')}}

