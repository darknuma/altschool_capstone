
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
SCHEMA_FILE = "/opt/airflow/dags/package/schema.json"

with DAG(
    'postgres_to_bigquery',
    default_args=default_args,
    description='Extract data from Postgres, upload to GCS, and load to BigQuery',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
) as dag:
    
    extract_and_upload = []
    
    for table in ['customers', 'geolocation_data', 'orders', 'products',
                   'sellers', 'order_items',
                     'order_payments', 'order_reviews', 'product_category_translation']:
        extract_task = PostgresToGCSOperator(
            task_id=f'extract_{table}',
            postgres_conn_id='postgres_default',
            sql=f'SELECT * FROM olist.{table}',
            bucket=BUCKET_NAME,
            filename=f'{table}.json',
            export_format='json',
            gzip=False,
        )
        extract_and_upload.append(extract_task)
    
    def load_to_bigquery():
        client = bigquery.Client()
        
        tables = ['customers', 'geolocation_data', 'orders', 'products',
                   'sellers', 'order_items',
                     'order_payments', 'order_reviews', 'product_category_translation']
        try:
            with open(SCHEMA_FILE, 'r') as f:
                schema_dict = json.load(f)  # Load the JSON file as a dictionary
        except Exception as e:
            logging.error(f"Error reading schema file: {e}")
            return

        for table in tables:
            table_id = f'{PROJECT_ID}.{DATASET_ID}.{table}'

            try:
                schema = [SchemaField.from_api_repr(field) for field in schema_dict[table]] 
            except KeyError as e:
                logging.error(f"Schema for table {table} not found: {e}")
                continue
            except Exception as e:
                logging.error(f"Error processing schema for table {table}: {e}")
                continue
            
            job_config = bigquery.LoadJobConfig(
                schema=schema,
                # skip_leading_rows=1,
                source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
                write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
                # quote_character = '"'
            )
            
        
            uri = f'gs://{BUCKET_NAME}/{table}.json'
            try:
                load_job = client.load_table_from_uri(
                    uri, table_id, job_config=job_config
                )
                logging.info(f"Starting job {load_job.job_id}")
                load_job.result()  
                logging.info(f"Job finished. Loaded {load_job.output_rows} rows into {table_id}.")
            except Exception as e:
                logging.error(f"Error loading data into BigQuery: {e}")


    load_to_bigquery = PythonOperator(
        task_id='load_to_bigquery',
        python_callable=load_to_bigquery,
    )
    
    extract_and_upload >> load_to_bigquery
