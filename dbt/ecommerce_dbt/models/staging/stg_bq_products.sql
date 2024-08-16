-- the raw products model
SELECT
    p.product_id,
    p.product_category_name,
    COALESCE(pct.product_category_name_english, p.product_category_name) AS product_category_name_english,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm
FROM {{ source('raw', 'products') }} p
LEFT JOIN {{ ref('stg_bq_product_category_translation') }} pct
    ON p.product_category_name = pct.product_category_name