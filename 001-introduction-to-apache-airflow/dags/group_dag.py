from airflow import DAG
from airflow.operators.bash import BashOperator

from groups.groups_downloads import downloads_tasks
from groups.groups_transforms import transforms_tasks

from datetime import datetime

with DAG(dag_id='group_dag',
         start_date=datetime(2024, 1, 1),
         schedule_interval='@daily',
         catchup=False,
         tags=['udemy']
    ) as dag:

    args = {'start_date': dag.start_date,
            'schedule_interval': dag.schedule_interval,
            'catchup': dag.catchup,
            'tags': dag.tags}

    downloads = downloads_tasks()

    check_files = BashOperator(
        task_id='check_files',
        bash_command='sleep 10'
    )

    transforms = transforms_tasks()

    downloads >> check_files >> transforms