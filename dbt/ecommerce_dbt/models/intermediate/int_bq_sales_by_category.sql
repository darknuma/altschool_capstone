-- models/intermediate/int_sales_by_category.sql
SELECT
    p.product_category_name_english,
    SUM(oi.price) as total_sales
FROM {{ ref('stg_bq_order_items') }} oi
JOIN {{ ref('stg_bq_products') }} p ON oi.product_id = p.product_id
GROUP BY p.product_category_name_english
