from airflow import DAG
from airflow.decorators import task, dag
from datetime import datetime

default_args = {
    'owner': 'Piotr',
    'start_date': datetime(2024, 1, 1),
    'retries': 1
}

@dag(
    default_args=default_args,
    schedule='@daily',
    tags=['Helion'],
    catchup=False,
    dag_id='example-2'
)
def example_dag():
    @task
    def start_task():
        return 'Example task completed'
    start_task()

dag = example_dag()