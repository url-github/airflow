from datetime import datetime
from airflow.decorators import dag, task

default_args = {
    'owner': 'Piotr',
    'start_date': datetime(2024, 9, 1),
}

@dag(
    dag_id='order_task',
    default_args=default_args,
    schedule=None,
    catchup=False,
    tags=['Helion']
)
def order_task_dag():

    @task
    def start():
        print("Start Task")

    @task
    def echoA():
        print('Hello World! (A)')

    @task
    def echoB():
        print('Hello World! (B)')

    @task
    def echoC():
        print('Hello World! (C)')

    @task
    def echoD():
        print('Hello World! (D)')

    start_task = start()

    echoA_task = echoA()
    echoB_task = echoB()
    echoC_task = echoC()
    echoD_task = echoD()

    start_task >> [echoA_task, echoC_task]
    echoA_task >> echoB_task
    [echoB_task, echoC_task] >> echoD_task

dag = order_task_dag()