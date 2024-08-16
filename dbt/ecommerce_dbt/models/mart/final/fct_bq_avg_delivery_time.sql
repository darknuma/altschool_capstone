-- I AM ASSUMING THE QUESTION IS SAYING ASKING, FINAL AVERAGE DELIVERY TIME (following what the requirement is saying.)
SELECT
    AVG(average_delivery_time_days) as final_avg_delivery_time_days,
    AVG(average_delivery_time_minutes) as final_avg_delivery_time_minutes
FROM {{ ref('int_bq_avg_delivery_time') }}