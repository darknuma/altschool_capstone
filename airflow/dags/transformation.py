from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from airflow import DAG
from datetime import datetime, timedelta

default_args = {
    'owner': 'emmanuel',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'dbt_pipeline',
    default_args=default_args,
    description='DBT TO BIGQUERY',
    schedule_interval='@daily',
    start_date=days_ago(1),
    catchup=False,
) as dag:

    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command='cd /path/to/dbt/project && dbt run',
        dag=dag,
    )

    dbt_test = BashOperator(
        task_id='dbt_test',
        bash_command='cd /path/to/dbt/project && dbt test',
        dag=dag,
    )

    dbt_run >> dbt_test

