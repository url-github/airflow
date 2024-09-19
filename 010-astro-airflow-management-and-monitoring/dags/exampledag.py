from airflow import Dataset
from airflow.decorators import dag, task
from pendulum import datetime
import requests

@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    # doc_md=__doc__,
    default_args={"owner": "Astro", "retries": 3},
    tags=["Astronomer"],
)
def example_astronauts():


    @task(outlets=[Dataset("current_astronauts")])

    def get_astronauts(**context) -> list[dict]:

        try:
            r = requests.get("http://api.open-notify.org/astros.json")
            r.raise_for_status()
            number_of_people_in_space = r.json()["number"]
            list_of_people_in_space = r.json()["people"]
        except:
            print("API currently not available, using hardcoded data instead.")
        #     number_of_people_in_space = 12
        #     list_of_people_in_space = [
        #         {"craft": "ISS", "name": "Oleg Kononenko"},
        #         {"craft": "ISS", "name": "Nikolai Chub"},
        #         {"craft": "ISS", "name": "Tracy Caldwell Dyson"},
        #         {"craft": "ISS", "name": "Matthew Dominick"},
        #         {"craft": "ISS", "name": "Michael Barratt"},
        #         {"craft": "ISS", "name": "Jeanette Epps"},
        #         {"craft": "ISS", "name": "Alexander Grebenkin"},
        #         {"craft": "ISS", "name": "Butch Wilmore"},
        #         {"craft": "ISS", "name": "Sunita Williams"},
        #         {"craft": "Tiangong", "name": "Li Guangsu"},
        #         {"craft": "Tiangong", "name": "Li Cong"},
        #         {"craft": "Tiangong", "name": "Ye Guangfu"},
        #     ]

        context["ti"].xcom_push(
            key="number_of_people_in_space", value=number_of_people_in_space
        )

        return list_of_people_in_space

    @task
    def print_astronaut_craft(greeting: str, person_in_space: dict) -> None:
        craft = person_in_space["craft"]
        name = person_in_space["name"]

        print(f"{name} is currently in space flying on the {craft}! {greeting}")

    """Metoda partial w Airflow pozwala na “zakolejkowanie” (ustalenie) części argumentów funkcji i oczekiwanie na dostarczenie brakujących argumentów później, np. poprzez metodę expand."""
    print_astronaut_craft.partial(greeting="Hello! :)").expand(
        person_in_space=get_astronauts()
    )

example_astronauts()
