from datetime import datetime
from airflow.decorators import dag
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from pandas import json_normalize
import json

def _process_user(ti):
    user = ti.xcom_pull(task_ids="extract_user")
    user = user['results'][0]
    processed_user = json_normalize({
        'firstname': user['name']['first'],
        'lastname': user['name']['last'],
        'country': user['location']['country'],
        'username': user['login']['username'],
        'password': user['login']['password'],
        'email': user['email']
	})
    processed_user.to_csv('/tmp/processed_user.csv', index=None, header=False)

def _store_user():
    hook = PostgresHook(postgres_conn_id='postgres')
    hook.copy_expert(
        sql="COPY users FROM stdin WITH DELIMITER as ',' ",
        filename='/tmp/processed_user.csv'
	)

@dag(schedule=None,
     start_date=datetime(2024, 9, 20, 20),
     end_date=datetime(2024, 9, 23, 20),
     catchup=False,
     tags=['udemy']
)
def project():

    wait_for_api = HttpSensor(
        task_id='wait_for_api',
        http_conn_id='user_api',
        endpoint='api/',
        method='GET',
        response_check=lambda response: response.status_code == 200,
        mode='poke',
        timeout=60,
        poke_interval=15
    )

    extract_user = SimpleHttpOperator(
        task_id='extract_user',
        http_conn_id='user_api',
        endpoint='api/',
        method='GET',
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    process_user = PythonOperator(
        task_id='process_user',
        python_callable=_process_user
    )

    store_user = PythonOperator(
        task_id='store_user',
        python_callable=_store_user
    )

    wait_for_api >> extract_user >> process_user >> store_user

project()