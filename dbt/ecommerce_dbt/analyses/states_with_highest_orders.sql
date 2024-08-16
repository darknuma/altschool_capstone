-- states with the highest number of order
SELECT
    *
FROM {{ ref('fct_bq_orders_by_state') }}
