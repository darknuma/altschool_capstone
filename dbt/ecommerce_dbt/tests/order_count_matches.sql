WITH order_count_from_orders AS (
    SELECT COUNT(DISTINCT order_id) as total_orders
    FROM {{ ref('stg_bq_orders') }}
),
order_count_from_state AS (
    SELECT SUM(order_count) as total_orders
    FROM {{ ref('fct_bq_orders_by_state') }}
)
SELECT 
    o.total_orders as orders_count,
    s.total_orders as state_sum_count
FROM order_count_from_orders o
CROSS JOIN order_count_from_state s
WHERE o.total_orders != s.total_orders