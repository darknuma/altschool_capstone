SELECT
    order_id,
    delivery_time_days
FROM {{ ref('int_bq_avg_delivery_time') }}
WHERE delivery_time_days < 0