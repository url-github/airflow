from datetime import datetime
from airflow import DAG

from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator


with DAG(
    dag_id='triggers2',
    schedule=None,
    catchup=False,
    tags=['Helion']
	):

    start = DummyOperator(
        task_id="start"
    )

    bashA = BashOperator(
        task_id="bashA",
        # bash_command="echo 'A'"
        bash_command="ls /airflow-fake", # fikcyjny folder
    )

    bashB = BashOperator(
        task_id="bashB",
        # bash_command="echo 'B'"
        bash_command="ls /airflow-fake", # fikcyjny folder
    )

    bashC = BashOperator(
        task_id="bashC",
        # bash_command="ls ~", # poprawne wykonanie bash
        bash_command="ls /airflow-fake", # fikcyjny folder
    )

    end = DummyOperator(
        task_id="end",
        # trigger_rule="one_failed" # Zadanie uruchomi się, gdy co najmniej jedno z poprzednich zadań zakończy się niepowodzeniem.
        trigger_rule="all_failed" # Wszystkie poprzednie zadania muszą zakończyć się niepowodzeniem, aby to zadanie mogło się uruchomić.

    )

    start >> [bashA, bashB, bashC] >> end