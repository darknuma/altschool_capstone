{{ config(
    materialized='view',
    schema='ecommerce'
) }}

SELECT
    product_category_name_english,
    total_sales,
    RANK() OVER (ORDER BY total_sales DESC) as sales_rank
FROM 
    {{ ref('int_bq_sales_by_category') }}
WHERE 
    product_category_name_english IS NOT NULL
ORDER BY 
    total_sales DESC


