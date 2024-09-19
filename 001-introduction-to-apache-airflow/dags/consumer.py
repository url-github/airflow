from airflow import DAG
from airflow.decorators import task
from include.datasets import MY_FILE, MY_FILE_2

from datetime import datetime

with DAG(
	dag_id='consumer',
	schedule=[MY_FILE, MY_FILE_2],
	start_date=datetime(2024, 1, 1),
	catchup=False,
	tags=['udemy']
):

	@task
	def read_dataset():
		with open(MY_FILE.uri, 'r') as f:
			print(f.read())

	read_dataset()


