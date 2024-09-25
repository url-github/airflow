

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from datetime import datetime

default_args = {
    'start_date': datetime(2024, 1, 1)
}

def _cleaning():
    print('Clearning from target DAG')

with DAG('target_dag',
    schedule_interval=None,
    default_args=default_args,
	tags=['a'],
    catchup=False) as dag:

    storing = BashOperator(
        task_id='storing',
        bash_command='sleep 200'
    )

    cleaning = PythonOperator(
        task_id='cleaning',
        python_callable=_cleaning
    )

    storing >> cleaning