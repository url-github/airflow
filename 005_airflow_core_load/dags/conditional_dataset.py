from __future__ import annotations

import pendulum

from airflow.datasets import Dataset
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.timetables.datasets import DatasetOrTimeSchedule
from airflow.timetables.trigger import CronTriggerTimetable

# [START dataset_def]
dag1_dataset = Dataset("s3://dag1/output_1.txt", extra={"hi": "bye"})
# [END dataset_def]
dag2_dataset = Dataset("s3://dag2/output_1.txt", extra={"hi": "bye"})
dag3_dataset = Dataset("s3://dag3/output_3.txt", extra={"hi": "bye"})

with DAG(
    dag_id="dataset_produces_1",
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule="@daily",
    # tags=["produces", "dataset-scheduled"],
	tags=["b"]
) as dag1:

    # [START task_outlet]
    BashOperator(outlets=[dag1_dataset], task_id="producing_task_1", bash_command="sleep 5")
    # [END task_outlet]

with DAG(
    dag_id="dataset_produces_2",
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=None,
    # tags=["produces", "dataset-scheduled"],
	tags=["b"]
) as dag2:

    BashOperator(outlets=[dag2_dataset], task_id="producing_task_2", bash_command="sleep 5")

# [START dag_dep]
with DAG(
    dag_id="dataset_consumes_1",
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=[dag1_dataset],
    # tags=["consumes", "dataset-scheduled"],
	tags=["b"]
) as dag3:
    # [END dag_dep]

    BashOperator(
        outlets=[Dataset("s3://consuming_1_task/dataset_other.txt")],
        task_id="consuming_1",
        bash_command="sleep 5",
    )

with DAG(
    dag_id="dataset_consumes_1_and_2",
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=[dag1_dataset, dag2_dataset],
    # tags=["consumes", "dataset-scheduled"],
	tags=["b"]
) as dag4:
    BashOperator(
        outlets=[Dataset("s3://consuming_2_task/dataset_other_unknown.txt")],
        task_id="consuming_2",
        bash_command="sleep 5",
    )

with DAG(
    dag_id="dataset_consumes_1_never_scheduled",
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=[
        dag1_dataset,
        Dataset("s3://unrelated/this-dataset-doesnt-get-triggered"),
    ],
    # tags=["consumes", "dataset-scheduled"],
	tags=["b"]
) as dag5:
    BashOperator(
        outlets=[Dataset("s3://consuming_2_task/dataset_other_unknown.txt")],
        task_id="consuming_3",
        bash_command="sleep 5",
    )

with DAG(
    dag_id="dataset_consumes_unknown_never_scheduled",
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=[
        Dataset("s3://unrelated/dataset3.txt"),
        Dataset("s3://unrelated/dataset_other_unknown.txt"),
    ],
    # tags=["dataset-scheduled"],
	tags=["b"]
) as dag6:
    BashOperator(
        task_id="unrelated_task",
        outlets=[Dataset("s3://unrelated_task/dataset_other_unknown.txt")],
        bash_command="sleep 5",
    )

with DAG(
    dag_id="consume_1_and_2_with_dataset_expressions",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=(dag1_dataset & dag2_dataset),
	tags=["b"]
) as dag5:
    BashOperator(
        outlets=[Dataset("s3://consuming_2_task/dataset_other_unknown.txt")],
        task_id="consume_1_and_2_with_dataset_expressions",
        bash_command="sleep 5",
    )
with DAG(
    dag_id="consume_1_or_2_with_dataset_expressions",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=(dag1_dataset | dag2_dataset),
	tags=["b"]
) as dag6:
    BashOperator(
        outlets=[Dataset("s3://consuming_2_task/dataset_other_unknown.txt")],
        task_id="consume_1_or_2_with_dataset_expressions",
        bash_command="sleep 5",
    )
with DAG(
    dag_id="consume_1_or_both_2_and_3_with_dataset_expressions",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=(dag1_dataset | (dag2_dataset & dag3_dataset)),
	tags=["b"]
) as dag7:
    BashOperator(
        outlets=[Dataset("s3://consuming_2_task/dataset_other_unknown.txt")],
        task_id="consume_1_or_both_2_and_3_with_dataset_expressions",
        bash_command="sleep 5",
    )
with DAG(
    dag_id="conditional_dataset_and_time_based_timetable",
    catchup=False,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=DatasetOrTimeSchedule(
        timetable=CronTriggerTimetable("0 1 * * 3", timezone="UTC"), datasets=(dag1_dataset & dag2_dataset)
    ),
    # tags=["dataset-time-based-timetable"],
	tags=["b"]
) as dag8:
    BashOperator(
        outlets=[Dataset("s3://dataset_time_based/dataset_other_unknown.txt")],
        task_id="conditional_dataset_and_time_based_timetable",
        bash_command="sleep 5",
    )
