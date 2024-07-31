from airflow.decorators import DAG, tasks
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator 
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from datetime import datetime 

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta 
import os



SQL_SELECT = ""
CONNECTION_ID = ""
BUCKET_NAME= ""
FILE_NAME =""

default_args = {
    "owner": "airflow",
    "catchup": False,
}

@dag(
    start_date=datetime(2023,1,2),
     schedule=None,
     catchup=False,
     tags=['retail']
     )

@task 
get_data = PostgresToGCSOperator(
        task_id="upload_to_gcs",
        postgres_conn_id=CONNECTION_ID,
        sql=SQL_SELECT,
        bucket=BUCKET_NAME,
        filename=FILE_NAME,
        gzip=False,
    )


load_to_bq = GCSToBigQueryOperator(

)
