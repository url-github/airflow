import json

from airflow import DAG
from airflow.models.baseoperator import chain
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.google.cloud.sensors.bigquery import BigQueryTableExistenceSensor
from airflow.providers.google.cloud.operators.bigquery import (
    BigQueryCreateEmptyDatasetOperator,
    BigQueryCreateEmptyTableOperator,
    BigQueryInsertJobOperator,
    BigQueryCheckOperator,
    BigQueryValueCheckOperator,
    BigQueryDeleteDatasetOperator,
)
from airflow.utils.dates import datetime
from airflow.utils.task_group import TaskGroup


DATASET = "astronomer"
TABLE = "forestfires"

with DAG(
    "008-simple-extract-load-bq",
    start_date=datetime(2024, 1, 1),
    description="Example DAG showcasing loading and data quality checking with BigQuery.",
    doc_md=__doc__,
    schedule_interval=None,
    template_searchpath="/opt/airflow/dags/include/sql/",
    catchup=False,
    tags=['astronomer']
) as dag:

    # BigQuery dataset creation
    create_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id="create_dataset",
        dataset_id=DATASET,
        gcp_conn_id='bigquery'
    )

    # BigQuery table creation
    create_table = BigQueryCreateEmptyTableOperator(
        task_id="create_table",
        dataset_id=DATASET,
        table_id=TABLE,
        gcp_conn_id='bigquery',
        schema_fields=[
            {"name": "id", "type": "INTEGER", "mode": "REQUIRED"},
            {"name": "y", "type": "INTEGER", "mode": "NULLABLE"},
            {"name": "month", "type": "STRING", "mode": "NULLABLE"},
            {"name": "day", "type": "STRING", "mode": "NULLABLE"},
            {"name": "ffmc", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "dmc", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "dc", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "isi", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "temp", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "rh", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "wind", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "rain", "type": "FLOAT", "mode": "NULLABLE"},
            {"name": "area", "type": "FLOAT", "mode": "NULLABLE"},
        ],
    )

    # BigQuery table check
    check_table_exists = BigQueryTableExistenceSensor(
        task_id="check_for_table",
        gcp_conn_id='bigquery',
        project_id="{{ var.value.gcp_project_id }}",
        dataset_id=DATASET,
        table_id=TABLE,
    )

    # Insert data
    load_data = BigQueryInsertJobOperator(
        task_id="insert_query",
        gcp_conn_id='bigquery',
        configuration={
            "query": {
                "query": "{% include 'load_bigquery_forestfire_data.sql' %}",
                "useLegacySql": False,
            }
        },
    )

    # Row-level data quality check
    with open("/opt/airflow/dags/include/validation/forestfire_validation.json") as ffv:
        with TaskGroup(group_id="row_quality_checks") as quality_check_group:
            ffv_json = json.load(ffv)
            for id, values in ffv_json.items():
                values["id"] = id

                BigQueryCheckOperator(
                    task_id=f"check_row_data_{id}",
                    gcp_conn_id='bigquery',
                    sql="row_quality_bigquery_forestfire_check.sql",
                    use_legacy_sql=False,
                    params=values,
                )

    # Table-level data quality check
    check_bq_row_count = BigQueryValueCheckOperator(
        task_id="check_row_count",
        gcp_conn_id='bigquery',
        sql=f"SELECT COUNT(*) FROM {DATASET}.{TABLE}",
        pass_value=9,
        use_legacy_sql=False,
    )

    # Delete test dataset and table
    delete_dataset = BigQueryDeleteDatasetOperator(
        task_id="delete_dataset",
        gcp_conn_id='bigquery',
        dataset_id=DATASET,
        delete_contents=True
    )

    begin = DummyOperator(task_id="begin")
    end = DummyOperator(task_id="end")

    chain(
        begin,
        create_dataset,
        create_table,
        check_table_exists,
        load_data,
        [quality_check_group, check_bq_row_count],
        delete_dataset,
        end,
    )
