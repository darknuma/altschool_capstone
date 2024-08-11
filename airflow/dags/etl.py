from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator, BigQueryExecuteQueryOperator
from airflow.utils.dates import days_ago
from google.cloud import bigquery
from google.cloud.bigquery import SchemaField
import json
import logging

default_args = {
    'owner': 'emmanuel',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

BUCKET_NAME = "order_ecomms"
PROJECT_ID = "altschool-capstones"
DATASET_ID = "ecommerce"
SCHEMA_FILE = "./package/schema.json"

with DAG(
    'postgres_to_bigquery',
    default_args=default_args,
    description='Extract data from Postgres, upload to GCS, and load to BigQuery',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
) as dag:
    
    extract_and_upload_tasks = []
    
    for table in ['customers', 'geolocation_data', 'orders', 'products',
                   'sellers', 'order_items',
                     'order_payments', 'order_reviews', 'product_category_translation']:
        extract_task = PostgresToGCSOperator(
            task_id=f'extract_{table}',
            postgres_conn_id='postgres_default',
            sql=f'SELECT * FROM {table}',
            bucket=BUCKET_NAME,
            filename=f'{table}.csv',
            export_format='csv',
            gzip=False,
        )
        extract_and_upload_tasks.append(extract_task)
    
    def load_to_bigquery():
        client = bigquery.Client()
        
        tables = ['customers', 'geolocation_data', 'orders', 'products',
                   'sellers', 'order_items',
                     'order_payments', 'order_reviews', 'product_category_translation']
        
        for table in tables:
            table_id = f'{PROJECT_ID}.{DATASET_ID}.{table}'

            try:
                with open(SCHEMA_FILE, 'r') as f:
                    schema_json = f.read()
                schema = [SchemaField.from_api_repr(field) for field in json.loads(schema_json)]
            except Exception as e:
                logging.error(f"Error reading schema file: {e}")
                return

            job_config = bigquery.LoadJobConfig(
                schema=schema,
                skip_leading_rows=1,
                source_format=bigquery.SourceFormat.CSV,
            )
            
        
            uri = f'gs://{BUCKET_NAME}/{table}.csv'
            try:
                load_job = client.load_table_from_uri(
                    uri, table_id, job_config=job_config, connection_id='google_cloud_default'
                )
                logging.info(f"Starting job {load_job.job_id}")
                load_job.result()  
                logging.info(f"Job finished. Loaded {load_job.output_rows} rows into {table_id}.")
            except Exception as e:
                logging.error(f"Error loading data into BigQuery: {e}")


    load_to_bigquery_task = PythonOperator(
        task_id='load_to_bigquery',
        python_callable=load_to_bigquery,
    )
    
    extract_and_upload_tasks >> load_to_bigquery_task
