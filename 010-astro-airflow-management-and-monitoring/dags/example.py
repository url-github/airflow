from airflow import DAG
from datetime import datetime
from airflow.operators.dummy import DummyOperator

default_args = {
    'owner': 'Piotr',
    'start_date': datetime(2024, 1, 1),
    'retries': 1
}

with DAG(
    dag_id='example',
    default_args=default_args,
    schedule='@daily',
    tags=['Helion'],
    catchup=False
) as dag:

    start = DummyOperator(
        task_id='example'
    )

    start