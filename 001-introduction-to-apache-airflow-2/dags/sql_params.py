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
def sql_params():

    start = DummyOperator(
        task_id="start"
    )

    add_two_vals = PostgresOperator(
        task_id='add_two_vals',
        postgres_conn_id='postgres',
        sql="SELECT %(x)s + %(y)s;",
        parameters={'x': 25, 'y': 25}
	)

    mul_two_vals = PostgresOperator(
        task_id='mul_two_vals',
        postgres_conn_id='postgres',
        sql='sql/multiply.sql',
        params={'a' : 2, 's' : 50}
	)

    start >> [add_two_vals, mul_two_vals]


sql_params()