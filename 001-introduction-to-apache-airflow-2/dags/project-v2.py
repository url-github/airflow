from datetime import datetime
from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.models.param import Param
from airflow.operators.python import BranchPythonOperator

import json

def switch_option(o):
    if o == "file":
        return ["check_file"]
    elif o == "sql":
        return ["create_table"]
    else:
        return ["check_file", "create_table"]

def prepare_sql(ti):
    data = ti.xcom_pull(
        key="result_user",
        task_ids=["format_user"]
    )[0].split(" ")

    ti.xcom_push(
        key="sql_command",
        value=f"INSERT INTO api_users VALUES ('{data[0]}', '{data[1]}', '{data[2]}');"
    )

def save_to_file(ti):
    data = ti.xcom_pull(
        key="result_user",
        task_ids=["format_user"]
    )

    with open("/home/piotr/Documents/airflow/files/users.txt", "a") as file:
        file.write(f'{data[0]}\n')

def format_user_data(ti):
    user = ti.xcom_pull(
        key="return_value",
        task_ids=["get_user_api"]
    )[0]

    user = json.loads(user)
    result = f'{user["results"][0]["name"]["first"]} {user["results"][0]["name"]["last"]} {user["results"][0]["login"]["username"]}'
    ti.xcom_push(key="result_user", value=result)


with DAG(
    dag_id="get_users",
    tags=["videopoint", "project"],
    start_date=datetime(2023, 8, 28, 20),
    end_date=datetime(2023, 8, 30, 20),
    schedule_interval="*/30 * * * *",
    params={"source": Param("both", enum=["file", "sql", "both"], description="Gdzie zapisać dane")}
    ):

    wait_for_api = HttpSensor(
        task_id="wait_for_api",
        http_conn_id="http_user_api",
        endpoint="/api",
        method="GET",
        response_check=lambda response: response.status_code == 200,
        mode="poke",
        timeout=60,
        poke_interval=15
    )

    get_user_api = SimpleHttpOperator(
        task_id="get_user_api",
        http_conn_id="http_user_api",
        endpoint="/api",
        method="GET"
    )

    format_user = PythonOperator(
        task_id="format_user",
        python_callable=format_user_data
    )

    check_file = FileSensor(
        task_id="check_file",
        filepath="/home/piotr/Documents/airflow/files/users.txt"
    )

    python_save_to_file = PythonOperator(
        task_id="python_save_to_file",
        python_callable=save_to_file
    )

    create_table = PostgresOperator(
        task_id="create_table",
        postgres_conn_id="pg_default",
        sql="CREATE TABLE IF NOT EXISTS api_users (fname VARCHAR, lname VARCHAR, login VARCHAR);"
    )

    prepare_sql_script = PythonOperator(
        task_id="prepare_sql_script",
        python_callable=prepare_sql
    )

    insert_data = PostgresOperator(
        task_id="insert_data",
        postgres_conn_id="pg_default",
        sql="{{ ti.xcom_pull(key='sql_command', task_ids='prepare_sql_script') }}"
    )

    switch_source = BranchPythonOperator(
        task_id="switch_source",
        python_callable=switch_option,
        op_args=['{{ params.source }}']
    )


    wait_for_api >> get_user_api >> format_user >> switch_source
    switch_source >> [check_file, create_table]
    check_file >> python_save_to_file
    create_table >> prepare_sql_script >> insert_data