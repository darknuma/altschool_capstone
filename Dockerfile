
FROM apache/airflow:2.7.1-python3.10

ENV HOME=/opt/airflow

WORKDIR /opt/airflow

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip intstall dbt-core dbt-bigquery && \
    pip install --no-cache-dir -r requirements.txt

USER root

RUN useradd -ms /bin/bash -u 60000 emmanuel

# Create directory for dbt
RUN mkdir -p /opt/dbt && chown emmanuel:emmanuel /opt/dbt

# Switch back to the airflow user
USER emmanuel

# Set up dbt configuration
ENV DBT_PROFILES_DIR=/opt/dbt
COPY profiles.yml /opt/dbt/profiles.yml