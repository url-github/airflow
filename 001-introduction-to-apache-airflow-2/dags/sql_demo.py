from airflow.decorators import dag
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

@dag(
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['udemy']
)
def sql_demo():

    start = DummyOperator(
        task_id="start"
    )

    check_db_version = PostgresOperator(
        task_id='check_db_version',
        postgres_conn_id='postgres',
        sql="SELECT version();"
	)

    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres',
        sql="sql/create_table.sql"
    )

    start >> check_db_version
    start >> create_table

sql_demo()