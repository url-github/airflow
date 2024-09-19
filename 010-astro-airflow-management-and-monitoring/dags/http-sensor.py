from airflow.decorators import dag, task
from datetime import datetime
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor

@task
def start_task():
    return 'Start task completed'

@dag(
    dag_id='http_sensor',
    start_date=datetime(2024, 9, 14),
    # end_date=datetime(2024, 9, 15),
    # schedule="* * * * *", # co minutę
    schedule=None,
    tags=['Helion'],
    catchup=False
)
def http_sensor_dag():

    start = start_task()

    check_api = HttpSensor(
        task_id='check_api',
        http_conn_id='http_user_api',
        endpoint='/api',
        method='GET',
        response_check=lambda response: response.status_code == 200,
        mode='poke',
        timeout=30,
        poke_interval=10
    )

    get_user = SimpleHttpOperator(
        task_id='get_user',
        http_conn_id='http_user_api',
        endpoint='/api',
        method='GET'
    )

    start >> check_api >> get_user

dag = http_sensor_dag()