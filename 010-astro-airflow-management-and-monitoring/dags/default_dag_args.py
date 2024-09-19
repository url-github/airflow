from datetime import datetime, timedelta
from airflow.decorators import dag, task

@task
def start_task():
	pass

@task
def t1_task():
	pass

@task
def t2_task():
	pass

default_args = {
    'owner': 'Piotr',
    'start_date': datetime(2024, 9, 14),
    'end_date': datetime(2025, 9, 14),
    'retries': 3,  # liczba prób
    'retry_delay': timedelta(minutes=30)  # czas pomiędzy próbami
}

@dag(
    dag_id='default_dag_args',
    default_args=default_args,
    schedule_interval=None,
    tags=['Helion'],
    catchup=False
)
def my_dag():

    start = start_task()
    t1 = t1_task()
    t2 = t2_task()

    start >> t1 >> t2

dag = my_dag()