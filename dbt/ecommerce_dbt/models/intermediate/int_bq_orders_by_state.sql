-- models/intermediate/int_orders_by_state.sql
SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) as order_count
FROM {{ ref('stg_bq_orders') }} o
JOIN {{ ref('stg_bq_customers') }} c ON o.customer_id = c.customer_id
GROUP BY c.customer_state