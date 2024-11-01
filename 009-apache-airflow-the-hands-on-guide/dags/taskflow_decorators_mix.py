from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator
from datetime import datetime

def _task_a():
    print('Task A')
    return 13

@dag(
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=["taskflow_decorators_mix", "Mix (PythonOperator i TaskFlow API)"]
)
def taskflow_decorators_mix():

    task_a = PythonOperator(
        task_id='task_a',
        python_callable=_task_a
    )

    @task
    def task_b(value):
        print('Task B')
        print(f'Value from Task A: {value}')

    result = task_a.output  # Pobieranie wyniku task_a przez XCom
    task_b(result)

taskflow_decorators_mix()