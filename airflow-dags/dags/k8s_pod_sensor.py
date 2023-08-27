from airflow.exceptions import AirflowException
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from airflow.sensors.base_sensor_operator import BaseSensorOperator


class KubernetesPodSensor(BaseSensorOperator, KubernetesPodOperator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def poke(self, context):
        try:
            KubernetesPodOperator.execute(self, context)
            return True
        except AirflowException:
            self.log.error("KubernetesPodSensor failed: possibly because the sensor condition not met. "
                           "Will retry...")
            return False
