from datetime import datetime, timedelta
import json

from airflow.decorators import dag, task
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'Piotr',
    'start_date': datetime(2024, 9, 14),
    'end_date': datetime(2025, 9, 14),
    'retries': 3,
    'retry_delay': timedelta(minutes=30)
}

@dag(
    dag_id='xcom',
    default_args=default_args,
    schedule=None,
    tags=['Helion'],
    catchup=False
)
def xcom_dag():

    get_first_name = SimpleHttpOperator(
        task_id='get_first_name',
        http_conn_id='http_user_api',
        endpoint='/api',
        method='GET'
    )

    @task
    def process_name(ti):
        user = ti.xcom_pull(
            key='return_value',
            task_ids='get_first_name'
        )
        user = json.loads(user)
        first_name = user['results'][0]['name']['first']
        ti.xcom_push(key="user_name", value=first_name)


    echo_end = BashOperator(
        task_id='echo_end',
        bash_command="echo '-- KONIEC --'",
        do_xcom_push=False
    )

    get_first_name >> process_name() >> echo_end


dag = xcom_dag()