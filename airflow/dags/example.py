from airflow.decorators import dag, task
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
import pendulum 

## BigQuery config variables
BQ_CONN_ID = "google_cloud_default" # Defined in airflow connection
BQ_PROJECT = "ringed-land-398802"
BQ_DATASET = "IDX_Stock"
BQ_TABLE1 = "dim_stocks"
BQ_TABLE2 = "dim_companies"
BQ_TABLE3 = "dim_companies"
BQ_TABLE4 = "dim_companies"
BQ_TABLE5 = "dim_companies"
BQ_TABLE6 = "dim_companies"
BQ_TABLE7 = "dim_companies"
BQ_TABLE8 = "dim_companies"
BQ_TABLE9 = "dim_companies"

BQ_BUCKET = 'idx-data'

## Postgres config variables
PG_CONN_ID = "postgres_default" # Defined in airflow connection
PG_SCHEMA = "IDX-Schema"
PG_TABLE1 = "ksql-stock-stream"
PG_TABLE2 = "ksql-company-stream"
PG_TABLE2 = "ksql-company-stream"
PG_TABLE3 = "ksql-company-stream"
PG_TABLE4 = "ksql-company-stream"
PG_TABLE5 = "ksql-company-stream"
PG_TABLE6 = "ksql-company-stream"
PG_TABLE7 = "ksql-company-stream"
PG_TABLE8 = "ksql-company-stream"
PG_TABLE9 = "ksql-company-stream"


@dag(
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=["example"],
)



## Task to transfer data from PostgreSQL to GCS
postgres_stock_to_gcs = PostgresToGCSOperator(
    task_id = 'postgres_stock_to_gcs',
    sql = f'SELECT * FROM "{PG_SCHEMA}"."{PG_TABLE1}";',
    bucket = BQ_BUCKET,
    filename = JSON_FILENAME1,
    export_format = 'CSV',  # You can change the export format as needed
    postgres_conn_id = PG_CONN_ID,  # Set your PostgreSQL connection ID
    field_delimiter=',',  # Optional, specify field delimiter for CSV
    gzip = False,  # Set to True if you want to compress the output file
    task_concurrency = 1,  # Optional, adjust concurrency as needed
    gcp_conn_id = BQ_CONN_ID,  # Set your GCS connection ID
    dag = dag,
)

## Task to transfer data from PostgreSQL to GCS Bucket
postgres_company_to_gcs = PostgresToGCSOperator(
    task_id = 'postgres_company_to_gcs',
    sql = f'SELECT * FROM "{PG_SCHEMA}"."{PG_TABLE2}";',
    bucket = BQ_BUCKET,
    filename = JSON_FILENAME2,
    export_format = 'CSV',  # You can change the export format as needed
    postgres_conn_id = PG_CONN_ID,  # Set your PostgreSQL connection ID
    field_delimiter=',',  # Optional, specify field delimiter for CSV
    gzip = False,  # Set to True if you want to compress the output file
    task_concurrency = 1,  # Optional, adjust concurrency as needed
    gcp_conn_id = BQ_CONN_ID,  # Set your GCS connection ID
    dag = dag,
)

postgres_stock_to_gcs >> postgres_company_to_gcs