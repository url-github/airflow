# to dyrektywa, która włącza nową funkcjonalność dla typów adnotacji. Umożliwia to opóźnione rozwiązywanie typów, co oznacza, że można używać typów adnotacji jako ciągów znaków, co poprawia czytelność kodu i unika problemów z cyklicznymi zależnościami.
from __future__ import annotations
import datetime
import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule

with DAG(
    dag_id="example_bash_operator",
    schedule=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["a"],
    params={"example_key": "example_value"},
) as dag:


    run_this_last = EmptyOperator(
        task_id="run_this_last",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    run_after_loop = BashOperator(
        task_id="run_after_loop",
        bash_command="echo https://airflow.apache.org/",
    )

    run_after_loop >> run_this_last

	# {{ task_instance_key_str }} to specjalna zmienna, która jest używana w kontekście szablonów Jinja.
    for i in range(3):
        runme = BashOperator(
            task_id=f"runme_{i}",
            bash_command='echo "{{ task_instance_key_str }}" && sleep 1', # {dag_id}__{task_id}__{ds_nodash} / example_bash_operator__runme_0__20240926
        )
        runme >> run_after_loop


    also_run_this = BashOperator(
        task_id="also_run_this",
        bash_command='echo "ti_key={{ task_instance_key_str }}"',
    )

    also_run_this >> run_this_last

this_will_skip = BashOperator(
	task_id="this_will_skip",
	bash_command='echo "hello world"; exit 1;', # Airflow potraktuje ten task jako nieudany (failed), ponieważ kod wyjścia nie jest równy 0.
	trigger_rule=TriggerRule.ALL_DONE,
	dag=dag,
)

this_will_skip >> run_this_last

if __name__ == "__main__":
    dag.test() # test() pozwala uruchomić DAG w trybie testowym, bez potrzeby uruchamiania całego serwera Airflow.