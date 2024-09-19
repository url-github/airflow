from airflow.decorators import dag, task
from datetime import datetime
from time import sleep
from airflow.providers.http.operators.http import SimpleHttpOperator

@task
def sleep_n_sec(sec: int) -> None:
    sleep(sec)

@task
def print_hello_txt(txt: str) -> None:
    print(f'Hello, {txt}')

@dag(
    dag_id='http_operator',
    start_date=datetime(2024, 9, 14),
    # end_date=datetime(2024, 9, 15),
    # schedule="* * * * *", # co minutę
    schedule=None,
    tags=['Helion'],
    catchup=False
)
def http_operator_dag():

    sleep_task = sleep_n_sec(10)

    get_user = SimpleHttpOperator(
        task_id='get_user',
        http_conn_id='http_user_api',
        endpoint='/api',
        method='GET'
    )

    sleep_task >> get_user

dag = http_operator_dag()