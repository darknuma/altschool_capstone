from google.cloud import storage, bigquery
from googl.cloud.bigquery import SchemaField
import json
import logging

PROJECT_ID = ""
BUCKET_ID = ""
DATASET_ID = ""

storage_client = storage.Client()
bigquery_client =  bigquery.Client()

def load_to_gcs(destination_name):
    """Load from PostgreSQL to Google Cloud Storage"""
    buck = storage.Bucket(BUCKET_ID)
    blob = buck.blob(destination_name)

    if blob.exists():
        logging.info(f"File exists {destination_name}")
        return
    try:
        blob.upload_from_string()
    except Exception as e:
        logging.error(f"Error uploading data")


def create_table(dataset_name: str, table_name: str, schema_file: str):
    """Creates a BigQuery table using schema from a file."""
    table_id = f"{bigquery_client.project}.{dataset_name}.{table_name}"

    try:
        bigquery_client.get_table(table_id)
        logging.info(f"Table '{table_id}' already exists.")
        return
    except Exception:
        pass

    try:
        with open(schema_file, 'r') as f:
            schema_json = f.read()
        schema = [SchemaField.from_api_repr(field) for field in json.loads(schema_json)]
    except Exception as e:
        logging.error(f"Error reading schema file: {e}")
        return

    try:
       table_ref = bigquery_client.dataset(dataset_name).table(table_name)
       table = bigquery.Table(table_ref, schema=schema)
       bigquery_client.create_table(table)
       logging.info(f"Table '{table_id}' created successfully.")
    except Exception as e:
        logging.error(f"Error creating table: {e}")

def load_to_bq(dataset_name:str, table_name: str, source_uri: str, source_format:str, schema_file:str) -> None:
    "Load data to bigquery"
    table_id = f"{bigquery_client.project}.{dataset_name}.{table_name}"
    source_uri = f"gs://{bucket_name}/{destination_blob_name}"
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        source_format=source_format,
        autodetect=False
    )

    try:
        load_job = bigquery_client.load_table_from_uri(source_uri, table_id, job_config=job_config)
        logging.info(f"Starting job {load_job.job_id}")
        load_job.result()  # Waits for the job to complete
        logging.info(f"Job finished. Loaded {load_job.output_rows} rows into {table_id}.")
    except Exception as e:
        logging.error(f"Error loading data into BigQuery: {e}")
