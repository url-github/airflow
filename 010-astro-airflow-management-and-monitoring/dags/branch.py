from datetime import datetime
from airflow.decorators import dag, task
from airflow.operators.python import BranchPythonOperator
from airflow.models.param import Param

default_args = {
    'owner': 'Piotr',
    'start_date': datetime(2024, 9, 1),
}

def choice_task(x):
    if x == "A":
        return 'echoA'
    else:
        return 'echoB'

@dag(
    dag_id='branch',
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=['Helion'],
    params={
        "branch_choice": Param("A", enum=["A", "B"])
    }
)
def branch():

    @task.branch
    def start(branch_choice):
        return choice_task(branch_choice)

    @task
    def echoA():
        print('A')

    @task
    def echoB():
        print('B')

    @task
    def end():
        print('End')

    start_task = start('{{ params.branch_choice }}')

    echoA_task = echoA()
    echoB_task = echoB()
    end_task = end()

    start_task >> [echoA_task, echoB_task] >> end_task

dag = branch()