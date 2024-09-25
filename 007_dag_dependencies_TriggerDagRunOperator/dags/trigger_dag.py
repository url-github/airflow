

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from datetime import datetime

default_args = {
    'start_date': datetime(2024, 1, 1)
}

def _downloading():
    print('downloading')

with DAG('trigger_dag',
    schedule_interval=None,
    default_args=default_args,
	tags=['a'],
    catchup=False) as dag:

    downloading = PythonOperator(
        task_id='downloading',
        python_callable=_downloading
    )

    trigger_target = TriggerDagRunOperator(
		task_id='trigger_target',
		trigger_dag_id='target_dag', # Identyfikator DAG, który zostanie wywołany. W tym przypadku jest to DAG o nazwie 'target_dag'.
		execution_date='{{ ds }}',
		reset_dag_run=True, # Jeżeli ustawione na True, usunie w target_dag poprzednie uruchomienie DAG-a (jeżeli istnieje) przed uruchomieniem nowego.
		wait_for_completion=True, # Jeżeli ustawione na True, task będzie czekał na zakończenie wywołanego DAG-a przed kontynuowaniem swojego wykonania.
		poke_interval=30 # Co ile sekund ma sprawdzać, czy wywołany DAG zakończył wykonanie, gdy pole `wait_for_completion` jest ustawione na True.
	)