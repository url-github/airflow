from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def _task_a():
	print('Task A')
	return 13

def _task_b(ti=None):
	print('Task B')
	print(ti.xcom_pull(task_ids='task_a'))

with DAG(
	dag_id='taskflow_classic',
	start_date=datetime(2024, 1, 1),
	schedule_interval='@daily',
	catchup=False,
	tags=["taskflow_classic", "PythonOperator (old method)"]
):
	task_a = PythonOperator(
		task_id='task_a',
		python_callable=_task_a
	)

	task_b = PythonOperator(
		task_id='task_b',
		python_callable=_task_b
	)

	task_a >> task_b