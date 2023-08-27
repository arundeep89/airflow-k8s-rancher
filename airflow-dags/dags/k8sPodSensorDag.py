import json
from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.models.baseoperator import chain
from airflow.sensors.bash import BashSensor

from k8s_pod_sensor import KubernetesPodSensor


DYNAMODB_READINESS_OP_IMAGE = "readiness-check:latest"
AWS_ACCESS_KEY_ID = "AKIA5X7HQXP2Q7B5K462"
AWS_SECRET_ACCESS_KEY = "OvUvg5btHis1SAs3cretKFHIUQ24wA"     # Change this
READINESS_SENSOR_POKE_INTERVAL = 25
READINESS_SENSOR_TIMEOUT = 60


def make_safe_name(name: str) -> str:
    """ Name in KubernetesPodOperator cannot be longer than 63 characters, this will truncate name to safe size.

    :param name: Name to make a safe length
    :return: safe Name with a length under 63 chars
    """
    return name[:62]


def create_external_table_readiness_task(table: str, dag: DAG) -> KubernetesPodSensor:
    return KubernetesPodSensor(
        image=DYNAMODB_READINESS_OP_IMAGE,
        image_pull_policy="IfNotPresent",
        arguments=["--table-name", table,
                   "--date", "{{ ds }}"],
        env_vars={'AWS_ACCESS_KEY_ID': AWS_ACCESS_KEY_ID,
                  'AWS_SECRET_ACCESS_KEY': AWS_SECRET_ACCESS_KEY},
        poke_interval=READINESS_SENSOR_POKE_INTERVAL,
        mode="reschedule",
        timeout=READINESS_SENSOR_TIMEOUT,
        name=make_safe_name(table.lower()),
        task_id=table.lower(),
        dag=dag
    )


@task
def final_task():
    return json.dumps({'return': 'i am done'})


with DAG(
    dag_id="k8s_sensors_dag_demo",
    schedule=None,
    start_date=datetime(2021, 1, 1),
    catchup=False,
) as dag:
    sleep_10sec_sensor = BashSensor(
        task_id='wait_for_10sec',
        poke_interval=2,
        timeout=30,
        soft_fail=False,
        retries=0,
        bash_command="sleep 10",
        dag=dag)

    the_final_task = final_task()

    chain(create_external_table_readiness_task('ios_ingestion', dag),
          sleep_10sec_sensor,
          the_final_task)
