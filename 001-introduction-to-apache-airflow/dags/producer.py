from airflow import DAG
from airflow.decorators import task
from include.datasets import MY_FILE, MY_FILE_2

from datetime import datetime

with DAG(
	dag_id='producer',
	schedule="@daily",
	start_date=datetime(2024, 1, 1),
	catchup=False,
	tags=['udemy']
):

	@task(outlets=[MY_FILE])
	def update_dataset():
		with open(MY_FILE.uri, 'a+') as f:
			f.write('producer update')

	@task(outlets=[MY_FILE_2])
	def update_dataset_2():
		with open(MY_FILE_2.uri, 'a+') as f:
			f.write('producer update')

	update_dataset() >> update_dataset_2()
