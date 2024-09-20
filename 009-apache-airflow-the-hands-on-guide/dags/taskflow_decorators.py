from airflow.decorators import dag, task
from datetime import datetime

@dag(
    dag_id='taskflow_decorators',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
)
def taskflow_decorators():

    @task
    def task_a():
        print('Task A')
        return 1

    @task
    def task_b(a_value):
        print('Task B')
        print(a_value)

    a_value = task_a()
    task_b(a_value)

taskflow_decorators()