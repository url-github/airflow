from airflow.decorators import task, dag
from datetime import datetime

default_args = {
    'owner': 'Piotr',
    'start_date': datetime(2024, 1, 1),
    'retries': 1
}

@dag(
    default_args=default_args,
    schedule=None,
    tags=['Helion'],
    catchup=False,
    dag_id='bash-operator'
)
def bash_operator():

    @task # _PythonDecoratedOperator
    def start_task():
        return 'Start task completed'

    @task # _PythonDecoratedOperator
    def echo_bash_task():
        return 'Bash command executed'

    start_task() >> echo_bash_task()

dag = bash_operator()