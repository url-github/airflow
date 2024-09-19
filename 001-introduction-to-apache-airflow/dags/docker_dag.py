from airflow.decorators import task, dag
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

@dag(dag_id='docker_dag',
     start_date=datetime(2024, 1, 1),
	 schedule_interval='@daily',
     tags=['udemy'])
def docker_dag():
	@task()
	def t1():
		pass

	t2 = DockerOperator(
		task_id='t2',
		image='python:3.8-slim-buster',
		command='echo "command running in the docker container"',
		docker_url='unix://var/run/docker.sock',
		# docker_url='unix:///Users/p/.docker/run/docker.sock',
		network_mode='bridge',
		# network_mode='host'
	)


	t1() >> t2

dag = docker_dag()