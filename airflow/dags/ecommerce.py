# from airflow.decorators import dag, task
# from airflow.operators.postgres_operator import PostgresOperator
# from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
# from datetime import datetime, timedelta
# import pendulum

# ## BigQuery config variables
# BQ_CONN_ID = "google_cloud_default"  # Defined in airflow connection
# BQ_BUCKET = 'order_ecomms'

# ## Postgres config variables
# PG_CONN_ID = "postgres_default"  # Defined in airflow connection
# PG_SCHEMA = "IDX-Schema"
# PG_TABLE1 = "olist.order_items"
# PG_TABLE2 = "olist.order_payments"
# PG_TABLE3 = "olist.orders"
# PG_TABLE4 = "olist.order_reviews"
# PG_TABLE5 = "olist.customers"
# PG_TABLE6 = "olist.products"
# PG_TABLE7 = "olist.sellers"
# PG_TABLE8 = "olist.product_category"
# PG_TABLE9 = "olist.product_category_name_translation"

# tables = ["customers", "orders", "order_reviews", "sellers", "product_category"]

# # (Other tables can be added as needed)

# @dag(
#     schedule=None,
#     start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),  # Use pendulum for timezone-aware datetime
#     catchup=False,
#     tags=["example"],
# )
# def example_dag():

#     @task
#     def transfer_postgres_stock_to_gcs():
#         # Task to transfer stock data from PostgreSQL to GCS
#         return PostgresToGCSOperator(
#             task_id='postgres_stock_to_gcs',
#             sql=f'SELECT * FROM "{PG_SCHEMA}"."{PG_TABLE1}";',
#             bucket=BQ_BUCKET,
#             filename=f"{}"
#             export_format='CSV',
#             postgres_conn_id=PG_CONN_ID,
#             field_delimiter=',',
#             gzip=False,
#             gcp_conn_id=BQ_CONN_ID,
#         )

#     @task
#     def transfer_postgres_company_to_gcs():
#         # Task to transfer company data from PostgreSQL to GCS
#         return PostgresToGCSOperator(
#             task_id='postgres_company_to_gcs',
#             sql=f'SELECT * FROM "{PG_SCHEMA}"."{PG_TABLE2}";',
#             bucket=BQ_BUCKET,
#             filename=JSON_FILENAME2,
#             export_format='CSV',
#             postgres_conn_id=PG_CONN_ID,
#             field_delimiter=',',
#             gzip=False,
#             gcp_conn_id=BQ_CONN_ID,
#         )

#     # Define the order of tasks
#     stock_task = transfer_postgres_stock_to_gcs()
#     company_task = transfer_postgres_company_to_gcs()

#     stock_task >> company_task

# dag = example_dag()

