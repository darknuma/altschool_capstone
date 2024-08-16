SELECT
    product_category_name_english,
    total_sales
FROM {{ ref('fct_bq_sales_by_category') }}
WHERE total_sales <= 0