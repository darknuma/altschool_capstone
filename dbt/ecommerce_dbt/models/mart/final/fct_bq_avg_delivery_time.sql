SELECT
    AVG(delivery_time_days) as avg_delivery_time_days
FROM {{ ref('int_bq_avg_delivery_time') }}