from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.models.param import Param

default_args = {
    'owner': 'Piotr',
    'start_date': datetime(2024, 9, 1),
    'end_date': datetime(2024, 10, 1),
    'retries': 3,
    'retry_delay': timedelta(minutes=30)
}

@dag(
    dag_id='params',
    default_args=default_args,
    schedule=None,
    tags=['Helion'],
    params={
        "show_data": Param(True, type="boolean", description="Czy wyświetlić dane"),
        "my_number": Param(10, type="integer", minimum=0, maximum=10, description="Podaj liczbę"),
        "enum_param": Param("One", enum=["One", "Two", "Three"], description="Wybierz wartość")
    },
    catchup=False
)
def params_dag():

    @task
    def start():
        print("Start DAG")

    @task
    def test_params(isActive, var1, var2):
        if isActive == 'True':
            print(var1, var2)

    start_task = start()

    test_params_task = test_params(
        '{{ params.show_data }}',
        '{{ params.my_number }}',
        '{{ params.enum_param }}'
    )


    start_task >> test_params_task


dag = params_dag()