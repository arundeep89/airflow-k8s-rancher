FROM apache/airflow:2.6.2-python3.8 as build

# Attach Labels to the image to help identify the image in the future
LABEL maintainer="Maxcotec <maxcotec.com>"
LABEL com.maxcotec.docker=true
LABEL com.maxcotec.docker.module="airflow"
LABEL com.maxcotec.docker.component="airflow"
LABEL com.maxcotec.docker.airflow.version="2.6.2"

USER root
RUN apt-get autoremove -yqq --purge && apt-get clean && \
    apt-get update && apt-get -y upgrade && \
    apt-get -y install gcc default-libmysqlclient-dev

USER airflow

WORKDIR /opt/airflow/

RUN pip install mysqlclient==1.4.1

# Airflow user in Docker image version 2.2.0+ moved to root group to be compatible with Open-Shift (https://airflow.apache.org/docs/docker-stack/entrypoint.html#allowing-arbitrary-user-to-run-the-container),
# below COPY is from official example: https://airflow.apache.org/docs/docker-stack/build.html#example-when-you-want-to-embed-dags
COPY --chown=airflow:root dags /opt/airflow/dags