# Use the official Apache Airflow image as the base image
FROM apache/airflow:2.7.1

# Set the home directory
ENV HOME=/opt/airflow

# Set the working directory
WORKDIR /opt/airflow

# Run the useradd command as root
USER root

# Create a new user with the specified UID and set up the home directory
RUN useradd -ms /bin/bash -u 60000 emmanuel

# Switch back to the airflow user
USER emmanuel

# Additional setup commands can follow here, if needed
ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt