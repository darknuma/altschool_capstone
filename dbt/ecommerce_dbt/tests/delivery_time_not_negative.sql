SELECT
    order_id,
    average_delivery_time_days,
    average_delivery_time_minutes
FROM 
    {{ ref('int_bq_avg_delivery_time') }}
WHERE 
    average_delivery_time_days < 0 
    AND average_delivery_time_minutes < 0