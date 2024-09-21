from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator
from datetime import datetime

def _task_a():
    print('Task A')
    return 1

@dag(
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
)
def taskflow_decorators_mix():

    task_a = PythonOperator(
        task_id='task_a',
        python_callable=_task_a
	)

    @task
    def task_b():
        print('Task B')
        print()

    # task_b(task_a.output) # new method
    task_a >> task_b() # old method

taskflow_decorators_mix()