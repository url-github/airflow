from airflow import DAG
from datetime import datetime
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.python import PythonSensor

def is_enough_len(minimum: int):
    with open("/Users/p/Documents/VSC/helion_include/helion_airflow.txt", "r") as file:
        data = file.read()

    if len(data) > minimum:
        return True
    else:
        return False


with DAG(
    dag_id='python-sensor',
    schedule_interval=None,
    start_date=datetime(2023, 9, 14),
    tags=['Helion'],
    catchup=False
):

    start = DummyOperator(
        task_id='start'
    )

    python_check = PythonSensor(
		task_id='python_check',
        python_callable=is_enough_len,
        op_args=[10],
        mode='poke',
        timeout=15,
        poke_interval=5
	)

    echo_bash = BashOperator(
		task_id='echo_bash',
        bash_command="echo 'KONIEC'"
    )

    start >> python_check >> echo_bash