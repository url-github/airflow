'''
Praktyczne zastosowanie

	1.	Automatyczne przetwarzanie danych z dynamicznymi nazwami plików – aliasy pozwalają na reagowanie DAG-ów konsumentów na zmiany bez potrzeby określania dokładnej nazwy pliku lub ścieżki.
	2.	Elastyczne przetwarzanie danych – użycie DatasetAlias umożliwia dynamiczne dopasowanie zestawów danych do DAG-ów bez modyfikacji kodu konsumentów.
	3.	Modułowość – takie podejście pozwala na wyzwalanie wielu DAG-ów konsumentów przez jeden producenta, co jest przydatne przy architekturach opartych na zbiorach danych w dużych projektach data engineeringowych.

'''

from __future__ import annotations

import pendulum

from airflow import DAG
from airflow.datasets import Dataset, DatasetAlias
from airflow.operators.python import PythonOperator

with DAG(
    dag_id="dataset_s3_bucket_producer_with_no_taskflow",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    # tags=["producer", "dataset"],
    tags=["e"],
):

    def produce_dataset_events():
        pass

    PythonOperator(
        task_id="produce_dataset_events",
        outlets=[Dataset("s3://bucket/my-task-with-no-taskflow")],
        python_callable=produce_dataset_events,
    )


with DAG(
    dag_id="dataset_alias_example_alias_producer_with_no_taskflow",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    # tags=["producer", "dataset-alias"],
    tags=["e"]
):

    def produce_dataset_events_through_dataset_alias_with_no_taskflow(*, outlet_events=None):
        bucket_name = "bucket"
        object_path = "my-task"
        outlet_events["example-alias-no-taskflow"].add(Dataset(f"s3://{bucket_name}/{object_path}"))

    PythonOperator(
        task_id="produce_dataset_events_through_dataset_alias_with_no_taskflow",
        outlets=[DatasetAlias("example-alias-no-taskflow")],
        python_callable=produce_dataset_events_through_dataset_alias_with_no_taskflow,
    )

with DAG(
    dag_id="dataset_s3_bucket_consumer_with_no_taskflow",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=[Dataset("s3://bucket/my-task-with-no-taskflow")],
    catchup=False,
    # tags=["consumer", "dataset"],
    tags=["e"]
):

    def consume_dataset_event():
        pass

    PythonOperator(task_id="consume_dataset_event", python_callable=consume_dataset_event)

with DAG(
    dag_id="dataset_alias_example_alias_consumer_with_no_taskflow",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=[DatasetAlias("example-alias-no-taskflow")],
    catchup=False,
    # tags=["consumer", "dataset-alias"],
    tags=["e"]
):

    def consume_dataset_event_from_dataset_alias(*, inlet_events=None):
        for event in inlet_events[DatasetAlias("example-alias-no-taskflow")]:
            print(event)

    PythonOperator(
        task_id="consume_dataset_event_from_dataset_alias",
        python_callable=consume_dataset_event_from_dataset_alias,
        inlets=[DatasetAlias("example-alias-no-taskflow")],
    )