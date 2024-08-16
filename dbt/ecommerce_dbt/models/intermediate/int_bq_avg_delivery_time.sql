-- answering that inermediate model, the average delivery time for orders, this is the answer here.
SELECT
    order_id,
    AVG(TIMESTAMP_DIFF(order_delivered_customer_date, order_purchase_timestamp, MINUTE)) AS average_delivery_time_minutes,
    AVG(DATE_DIFF(order_delivered_customer_date, order_purchase_timestamp, DAY)) AS average_delivery_time_days
FROM
    {{ ref('stg_bq_orders')}}
WHERE
    order_status = 'delivered'
    AND order_delivered_customer_date IS NOT NULL
    AND order_purchase_timestamp IS NOT NULL
GROUP BY
    order_id
ORDER BY
    average_delivery_time_minutes ASC
