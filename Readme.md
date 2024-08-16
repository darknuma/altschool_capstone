# AltSchool Capstone Project

This project demonstrates an end-to-end ETL (Extract, Transform, Load) process using the [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) from Kaggle. The implementation utilizes PostgreSQL, Docker, Docker Compose, dbt (Data Build Tool), and Apache Airflow.

## Requirements

- Ensure [Docker](https://www.docker.com/) is installed on your machine.
- Set up a [Google Cloud Platform (GCP)](https://cloud.google.com/) account.
- Create a GCP project with a `PROJECT_ID` and `DATASET`. In the IAM section, create a service account with the appropriate BigQuery and Cloud Storage permissions, and generate a key.
- Have a [GitHub](https://www.github.com) account.
- Modify the `docker-compose.yaml` and `Dockerfile` to include your own `PROJECT_ID`, `DATASET`, and service account details.

## How to Run

1. **Fork and Clone the Project:**
   - Fork and clone this repository from [here](https://github.com/darknuma/altschool_capstone.git).

2. **Build and Start Docker Containers:**
   - Navigate to the project directory and run Docker to trigger the `Dockerfile` and `docker-compose.yaml`. This will set up the environment, including loading CSV data into PostgreSQL as defined in the `init.sql` file.

     ```sh
     cd project_directory
     docker-compose up --build 
     ```

3. **Set Up Airflow Connections:**
   - In the Airflow UI, configure the `google_cloud_default` and `postgres_default` connections. Test the connections to ensure they are set up correctly. Ensure that the Google credentials environment variable is properly set in `docker-compose.yaml` (under volumes).

4. **Run Airflow DAGs:**
   - Log in to Airflow and manually trigger the `Postgres_to_BigQuery` DAG. This DAG handles data extraction from PostgreSQL and loading it into BigQuery.

5. **Verify dbt Setup:**
   - To verify dbt connections or initialize a new dbt project, run the following commands inside the Docker container:

     ```sh
     docker exec -it [CONTAINER_NAME] [COMMAND]
     cd [DBT_PROJECT_PATH]
     dbt init [OPTIONAL]
     dbt debug 
     ```

6. **Run dbt Transformations and Tests:**
   - Trigger the `dbt_pipeline` DAG in Airflow to perform data transformations and run tests using dbt.

7. **Analyze Data in BigQuery:**
   - Review the results and analyses directly in the BigQuery Console.

## Project Structure

- **infra_scripts:** Contains the `init.sql` script, which creates tables and loads data from CSV files into the `ecommerce` database.
  - `init.sql`: SQL script for table creation and data loading.

- **dbt:** Contains the `ecommerce_dbt` project, which includes dbt models for data transformation and analysis.
  - `ecommerce_dbt`:
    - `models`: Organized into staging, intermediate, and mart layers.
    - `tests`: Includes SQL tests such as `delivery_time.sql`, `order_count_matches.sql`, and `test_all_categories_translation.sql` (Note: the last test may fail due to null values).
    - `dbt_project.yml`: Configuration file for dbt.
    - `requirements.txt`: Lists the dependencies required for the dbt project.

- **airflow:**
  - **dags:**
    - `package`: Contains `schema.json`, defining the schema for BigQuery.
    - `ecommerce.py`: DAG script for extracting data to PostgreSQL and loading it into BigQuery.
    - `transformation.py`: DAG script using BashOperator to run `dbt run && dbt test`.

- **docker-compose.yaml:** Defines the infrastructure setup for PostgreSQL, Airflow, and directories for the dbt profile.
- **Dockerfile:** Configures Airflow and sets up the dbt environment.

## Feedback

For any feedback, feel free to reach out via DM on my X account [Numatelly](https://www.x.com/numatelly)
