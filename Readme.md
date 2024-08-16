# ALT SCHOOL CAPSTONE PROJECT

An end-to-end implementation of ETL process using [https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce](Olist) from Kaggle using, PostgreSQL, Docker, Docker Compose, Dbt and Airflow.

## REQUIREMENTS

```markdown
- Ensure you have [https://www.docker.com/](Docker) installed on your computer, have a [https://cloud.google.com/](GCP) account
- Create your PROJECT_ID, DATASET and in IAM/service_account, create key service account, with the BigQuery and Cloud Storage privileges.
- Have a [https://www.github.com](GitHub) account
- Edit PROJECT_ID, DATASET, and service account for your own use in the `docker-compose.yaml` and `Dockerfile`
```

## HOW TO RUN

```markdown
* Fork and Clone this project [https://github.com/darknuma/altschool_capstone.git](here)
* Run Docker in shell, this would trigger the `DockerFile` and `docker-compose.yaml` 
  (CSV Files are extracted to PostgreSQL, from the `init.sql` file) 
    ```sh
        cd project_directory
        docker-compose up --build 
    ```
* In Airflow Connections set up `google_cloud_default` and `postgres_default`, test if the connections are good. (ENVIRONMENT VARIABLE FOR GOOGLE CREDENTIALS      SHOULD BE EDITED IN `docker-compose.yaml`, specifically volumes)
* Login to Airflow and Run the DAGS, to trigger `Postgres_to_BigQuery` DAG ID (Extraction to PostgreSQL and Load to BigQuery)
* To check for your dbt connections, For a new dbt project.
    ```sh
        docker exec -it [CONTAINER_NAME] [COMMAND]
        cd [DBT_PROJECT_PATH]
        dbt init [OPTIONAL]
        dbt-debug 
    ```
* Trigger `dbt_pipeline` DAG ID, to run transformation, and test.
* Check the analyses in BigQuery Console.
```

## PROJECT STRUCTURE

```markdown
+ infra_scripts: This folder contains init.sql which extracts data from CSV files into ecommerce database
    * `init.sql` (table and copy)
+ dbt: This folder contains `ecommerce_dbt` which contains the models to transform and perform analysis
    * `ecommerce_dbt`: contains `models`
        - `models`: (staging, intermediate and mart)
        - `tests`: (test for `delivery_time.sql`, `order_count_matches.sql`, `test_all_categories_translation.sql`--this failed because of null values)
        - `dbt_project.yml`: (configuration for dbt)
        - `requirements.txt`: (libraries dependencies)
+ airflow
    * `dags`
        - package: contains the `schema.json` file for the schema in BigQuery
        - `ecommerce.py`: DAG script to extract to PostgreSQL and load to BigQuery
        - `transformation.py`: A DAG script using BashOperator to run `dbt run && dbt test`
        
+ docker-compose.yaml: Comprises of the infrastructure setup for PostgreSQL, Airflow and directories for DBT_PROFILE_DIR
+ Dockerfile: Dockerfile for Airflow setup and user setup, with setting DBT environments.
```

FOR FEEDBACK, send a DM to my X account [https://www.x.com/numatelly](Numatelly)