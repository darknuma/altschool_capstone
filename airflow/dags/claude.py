import logging
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from google.cloud import storage
from google.cloud import bigquery
import pandas as pd
from datetime import datetime, timedelta

# Set up logging
logger = logging.getLogger(__name__)

def ingest_csv_to_postgres(**kwargs):
    csv_file = kwargs['csv_file']
    table_name = kwargs['table_name']
    
    logger.info(f"Starting ingestion of {csv_file} into PostgreSQL table {table_name}")
    
    df = pd.read_csv(f'/opt/airflow/data/{csv_file}')
    postgres_hook = PostgresHook(postgres_conn_id='postgres_default')
    engine = postgres_hook.get_sqlalchemy_engine()
    
    df.to_sql(table_name, engine, schema='olist', if_exists='append', index=False)
    
    row_count = engine.execute(f"SELECT COUNT(*) FROM olist.{table_name}").scalar()
    logger.info(f"Successfully ingested {row_count} rows into {table_name}")

def check_gcs_files(**kwargs):
    bucket_name = kwargs['bucket_name']
    prefix = kwargs['prefix']
    
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=prefix))
    
    logger.info(f"Found {len(blobs)} files in GCS bucket {bucket_name} with prefix {prefix}")
    for blob in blobs:
        logger.info(f"File: {blob.name}, Size: {blob.size} bytes")

def check_bigquery_table(**kwargs):
    project_id = kwargs['project_id']
    dataset_id = kwargs['dataset_id']
    table_id = kwargs['table_id']
    
    client = bigquery.Client()
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    
    try:
        table = client.get_table(table_ref)
        logger.info(f"Table {table_ref} contains {table.num_rows} rows")
    except Exception as e:
        logger.error(f"Error checking BigQuery table {table_ref}: {str(e)}")

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'olist_data_pipeline',
    default_args=default_args,
    description='Olist data pipeline with logging',
    schedule_interval=timedelta(days=1),
)

tables = ['customers', 'geolocation_data', 'order_items', 'order_payments', 
          'order_reviews', 'orders', 'products', 'product_category_translation']

for table in tables:
    t1 = PythonOperator(
        task_id=f'ingest_{table}_to_postgres',
        python_callable=ingest_csv_to_postgres,
        op_kwargs={'csv_file': f'{table}.csv', 'table_name': table},
        dag=dag,
    )

    t2 = PostgresToGCSOperator(
        task_id=f'postgres_to_gcs_{table}',
        postgres_conn_id='postgres_default',
        gcp_conn_id='google_cloud_default',
        sql=f'SELECT * FROM olist.{table}',
        bucket='your-gcs-bucket',
        filename=f'olist/{table}/{{{{ ds }}}}/{table}.json',
        export_format='json',
        dag=dag,
    )

    t3 = PythonOperator(
        task_id=f'check_gcs_{table}',
        python_callable=check_gcs_files,
        op_kwargs={'bucket_name': 'your-gcs-bucket', 'prefix': f'olist/{table}/{{{{ ds }}}}'},
        dag=dag,
    )

    t4 = GCSToBigQueryOperator(
        task_id=f'gcs_to_bigquery_{table}',
        bucket='your-gcs-bucket',
        source_objects=[f'olist/{table}/{{{{ ds }}}}/{table}.json'],
        destination_project_dataset_table=f'your-project-id.olist.{table}',
        source_format='NEWLINE_DELIMITED_JSON',
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_TRUNCATE',
        gcp_conn_id='google_cloud_default',
        dag=dag,
    )

    t5 = PythonOperator(
        task_id=f'check_bigquery_{table}',
        python_callable=check_bigquery_table,
        op_kwargs={'project_id': 'your-project-id', 'dataset_id': 'olist', 'table_id': table},
        dag=dag,
    )

    t1 >> t2 >> t3 >> t4 >> t5