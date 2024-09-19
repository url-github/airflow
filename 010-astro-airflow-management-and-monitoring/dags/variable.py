from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.models import Variable

default_args = {
    'owner': 'Piotr',
    'start_date': datetime(2024, 9, 14),
    'end_date': datetime(2025, 9, 14),
    'retries': 3,
    'retry_delay': timedelta(minutes=30)
}

@dag(
    dag_id='variable',
    default_args=default_args,
    schedule=None,
    tags=['Helion'],
    catchup=False
)
def my_variable_dag():
    @task
    def print_value_task():
        print(Variable.get("foo"))

    @task
    def print_json_task():
        print(Variable.get("jsondata", deserialize_json=True))

    @task
    def print_array_task():
        print(Variable.get("arraydata"))

    start = print_value_task()
    json_task = print_json_task()
    array_task = print_array_task()

    start >> json_task >> array_task

dag = my_variable_dag()