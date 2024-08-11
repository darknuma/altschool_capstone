# Use the official Apache Airflow image as the base image
FROM apache/airflow:2.7.1-python3.10

# Set the home directory
ENV HOME=/opt/airflow

# Set the working directory
WORKDIR /opt/airflow

# Additional setup commands can follow here, if needed
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Run the useradd command as root
USER root

# Create a new user with the specified UID and set up the home directory
RUN useradd -ms /bin/bash -u 60000 emmanuel

# Switch back to the airflow user
USER emmanuel


