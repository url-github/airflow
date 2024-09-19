from airflow.decorators import task, dag
from datetime import datetime
from time import sleep

@task
def sleep_n_sec(sec: int) -> None:
    sleep(sec)

@task
def print_hello_txt(txt: str) -> None:
    print(f'Hello, {txt}')

@dag(
    dag_id='python_operator_scheduler',
    start_date=datetime(2024, 1, 1, 11, 0),
    end_date=datetime(2024, 12, 1, 23, 0),
    # schedule="0 * * * *", # co godzinę
    schedule="* * * * *", # co minutę
    tags=['Helion'],
    catchup=False
)
def python_operator_scheduler():
    start_task = sleep_n_sec(10)
    print_task = print_hello_txt('test test test')

    start_task >> print_task

dag = python_operator_scheduler()