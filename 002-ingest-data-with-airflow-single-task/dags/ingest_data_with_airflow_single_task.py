from airflow.decorators import dag, task
from datetime import datetime
from airflow.providers.google.cloud.hooks.bigquery import BigQueryHook
from airflow.models.baseoperator import chain

@dag(
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=['a'],
    max_consecutive_failed_dag_runs=5, # Określa maksymalną liczbę kolejnych nieudanych uruchomień DAG-a, po których DAG zostanie automatycznie zatrzymany (suspended).
    doc_md=__doc__,
)
def ingest_data_with_airflow_single_task():

	# .pyairbyte-venv dodane w pliku Dockerfile
    @task.external_python(python='/usr/local/airflow/.pyairbyte-venv/bin/python')
    def extract():
        import airbyte as ab
        from airbyte.caches import BigQueryCache

        source = ab.get_source(
            "source-s3",
            config={
                "bucket": "002-ingest-data-with-airflow-single-task",
                "region_name": "eu-central-1",
                "streams": [
                  {
                      "name": "transaction",
                      "format": {
                          "filetype": "csv"
                      },
                  }
                ],
                # Edycja pliku .env kluczem pobranym z IAM AWS.
                "credentials": {
                    "aws_access_key_id": ab.get_secret("AWS_ACCESS_KEY_ID"),
                    "aws_secret_access_key": ab.get_secret("AWS_SECRET_ACCESS_KEY")
                }
            },
            install_if_missing=False, # uzywam venv dlatego daje False

        )
        source.select_all_streams()
        read_result = source.read(cache=BigQueryCache(
            project_name="third-essence-345723",
            dataset_name="astronomer",
            credentials_path="/usr/local/airflow/include/sa-ga4-data.json",
        ))

        first_record = next((record for record in read_result["transaction"]))
        print(f"First record: {first_record}")

    @task
    def check():
        bigquery = BigQueryHook(gcp_conn_id='bigquery',
                                use_legacy_sql=False,
                                location='US')
        df = bigquery.get_pandas_df("SELECT COUNT(*) FROM astronomer.transaction", dialect="standard")
        print(f"Number of rows in the table: {df.iloc[0, 0]}")

    chain(extract(), check())

ingest_data_with_airflow_single_task()