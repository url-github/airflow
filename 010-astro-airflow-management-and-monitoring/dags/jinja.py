from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Piotr',
    'start_date': datetime(2024, 9, 1),
    'end_date': datetime(2024, 10, 1),
    'retries': 1
}

@dag(
    dag_id='jinja',
    default_args=default_args,
    schedule=None,
    tags=['Helion'],
    catchup=False
)
def jinja_dag():

    echo_ds = BashOperator(
        task_id='echo_ds',
        bash_command="echo '{{ ds }}'" # 2024-09-17
    )

    echo_task_instance = BashOperator(
        task_id='echo_task_instance',
        bash_command="echo '{{ task_instance_key_str }}'" # jinja__echo_task_instance__20240917
    )

    @task
    def test_parse_var(x):
        print(x, 'NOT FAKE') # bar NOT FAKE
        print('{{ var.value.foo }}', 'FAKE') # {{ var.value.foo }} FAKE

    parse_var_task = test_parse_var('{{ var.value.foo }}')

    echo_ds >> echo_task_instance >> parse_var_task

dag = jinja_dag()