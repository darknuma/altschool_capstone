-- models/stg_product_category_translation.sql
SELECT
    product_category_name,
    product_category_name_english
FROM {{ source('raw', 'product_category_translation') }}

