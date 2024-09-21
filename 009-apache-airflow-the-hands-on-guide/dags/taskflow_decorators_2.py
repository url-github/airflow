from airflow.decorators import dag, task
from datetime import datetime
import random

@dag(
    dag_id='taskflow_decorators_2',
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    description='A simple DAG using TaskFlow API to generate and check random numbers',
    catchup=False
)
def taskflow_decorators_2():

    @task
    def generate_random_number():
        number = random.randint(1, 100)
        print(f"Generated random number: {number}")
        return number

    @task
    def check_even_odd(number: int):
        result = "even" if number % 2 == 0 else "odd"
        print(f"The number {number} is {result}.")

    check_even_odd(generate_random_number())

taskflow_decorators_2()