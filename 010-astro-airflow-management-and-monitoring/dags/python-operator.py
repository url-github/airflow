from airflow.decorators import task, dag
from datetime import datetime
from time import sleep

@task
def sleep_n_sec(sec: int) -> None:
    sleep(sec)

@task
def print_hello_txt(txt: str) -> None:
    print(f'Hello, {txt}')

default_args = {
    'owner': 'Piotr',
    'start_date': datetime(2024, 1, 1),
    'retries': 1
}

@dag(
    dag_id='python_operator',
    default_args=default_args,
    schedule=None,
    tags=['Helion'],
    catchup=False
)

def python_operator_dag():

    sleep_task = sleep_n_sec(10)
    print_task = print_hello_txt('test test test')

    sleep_task >> print_task

dag = python_operator_dag()