-- tests/test_all_categories_have_translation.sql

-- This test will return any product categories that don't have a corresponding
-- entry in the translation table.

WITH product_categories AS (
    SELECT DISTINCT product_category_name
    FROM {{ ref('stg_bq_products') }}
    WHERE product_category_name IS NOT NULL
),
translations AS (
    SELECT DISTINCT product_category_name
    FROM {{ ref('stg_bq_product_category_translation') }}
)
SELECT pc.product_category_name
FROM product_categories pc
LEFT JOIN translations t ON pc.product_category_name = t.product_category_name
WHERE t.product_category_name IS NULL