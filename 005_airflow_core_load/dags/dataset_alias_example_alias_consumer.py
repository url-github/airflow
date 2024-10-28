"""
Przykład scenariusza zastosowania

	1.	Producent: Tworzy plik z danymi i zapisuje go w s3://bucket/file1.csv. Ten plik jest przypisany do aliasu dane_sprzedażowe.
	2.	Konsument: Kolejny DAG jest skonfigurowany, aby wykonywać przetwarzanie zawsze, gdy pojawią się nowe dane związane z aliasem dane_sprzedażowe.

Jeśli zmienisz plik źródłowy na s3://bucket/nowy_file.csv, wystarczy, że przypiszesz nową ścieżkę do aliasu dane_sprzedażowe. Wszystkie zależne DAG-i, które korzystają z tego aliasu, będą teraz uruchamiane na nowym pliku, a nie na file1.csv.
"""

from __future__ import annotations

import pendulum

from airflow import DAG
from airflow.datasets import Dataset, DatasetAlias
from airflow.decorators import task

with DAG(
    dag_id="dataset_s3_bucket_producer",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    # tags=["producer", "dataset"],
    tags=["d"]
):

    @task(outlets=[Dataset("s3://bucket/my-task")])
    def produce_dataset_events():
        pass

    produce_dataset_events()

with DAG(
    dag_id="dataset_alias_example_alias_producer",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    # tags=["producer", "dataset-alias"],
	tags=["d"]
):

    @task(outlets=[DatasetAlias("example-alias")])
    def produce_dataset_events_through_dataset_alias(*, outlet_events=None):
        bucket_name = "bucket"
        object_path = "my-task"
        outlet_events["example-alias"].add(Dataset(f"s3://{bucket_name}/{object_path}"))

    produce_dataset_events_through_dataset_alias()

with DAG(
    dag_id="dataset_s3_bucket_consumer",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=[Dataset("s3://bucket/my-task")],
    catchup=False,
    # tags=["consumer", "dataset"],
    tags=["d"]
):

    @task
    def consume_dataset_event():
        pass

    consume_dataset_event()

with DAG(
    dag_id="dataset_alias_example_alias_consumer",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    schedule=[DatasetAlias("example-alias")],
    catchup=False,
    # tags=["consumer", "dataset-alias"],
    tags=["d"]
):

    @task(inlets=[DatasetAlias("example-alias")])
    def consume_dataset_event_from_dataset_alias(*, inlet_events=None):
        for event in inlet_events[DatasetAlias("example-alias")]:
            print(event)

    consume_dataset_event_from_dataset_alias()
