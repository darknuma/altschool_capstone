-- answering sales by category
SELECT
    *
FROM 
    {{ ref('fct_bq_sales_by_category') }}
