from datetime import datetime
from airflow import DAG

from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import BranchPythonOperator
from airflow.models.param import Param

def choice_task(x):
    if x == "A":
        return ["bashA"]
    else:
        return ["bashB"]

with DAG(
    dag_id='triggers1',
    schedule=None,
    catchup=False,
    tags=['Helion'],
    params={
        "branch_choice": Param("A", enum=["A", "B"])
	}
	):

    start = DummyOperator(
        task_id="start"
    )

    switch = BranchPythonOperator(
        task_id="switch",
        python_callable=choice_task,
        op_args=['{{ params.branch_choice }}']
    )

    bashA = BashOperator(
        task_id="bashA",
        bash_command="echo 'A'"
    )

    bashB = BashOperator(
        task_id="bashB",
        bash_command="echo 'B'"
    )

    bashC = BashOperator(
        task_id="bashC",
        # bash_command="echo 'C'",
        bash_command="ls /airflow-fake", # fikcyjny folder
    )

    end = DummyOperator(
        task_id="end",
        # trigger_rule="one_success" # co najminiej jeden udany task
        trigger_rule="none_failed" # Zadanie uruchomi się, gdy żadne z poprzednich zadań nie zakończy się niepowodzeniem (mogą być sukcesy lub zadania zakończone innymi statusami).
    )

    start >> switch >> [bashA, bashB] >> end
    start >> bashC >> end