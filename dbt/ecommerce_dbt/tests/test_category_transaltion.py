
def test_category_translation_complete(project):
    dbt_runner = project.test_data()
    
    # Run dbt models
    results = dbt_runner.run(models=['stg_bq_products', 'stg_product_bq_category_translation'])
    
    # Query the results
    products = dbt_runner.execute_sql("""
        SELECT DISTINCT product_category_name
        FROM {{ ref('stg_bq_products') }}
        WHERE product_category_name_english = product_category_name
    """)
    
    # Assert that no products have untranslated categories
    assert len(products) == 0, f"Found {len(products)} untranslated categories: {products}"