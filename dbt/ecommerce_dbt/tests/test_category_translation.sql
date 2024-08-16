SELECT 
    product_id,
    product_category_name,
    product_category_name_english
FROM {{ ref('stg_bq_products') }}
WHERE product_category_name = product_category_name_english
  AND product_category_name != 'None'

