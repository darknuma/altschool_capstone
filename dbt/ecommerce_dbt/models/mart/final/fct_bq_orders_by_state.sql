{{ config(
    materialized='table',
    schema='ecommerce'
) }}

SELECT
    customer_state,
    order_count,
    RANK() OVER (ORDER BY order_count DESC) as order_rank
FROM {{ ref('int_bq_orders_by_state') }}