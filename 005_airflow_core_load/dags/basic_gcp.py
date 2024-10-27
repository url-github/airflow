# Importujemy wymagane moduły
import json
import pendulum
from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.pubsub import PubSubPublishMessageOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryExecuteQueryOperator
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.google.cloud.operators.bigquery import BigQueryCheckOperator

# Konfiguracja podstawowych parametrów, takich jak nazwy zasobów GCP
GCP_PROJECT_ID = "twoj_projekt_id"
GCS_BUCKET_NAME = "twoj_bucket"
GCS_FILE_PATH = "sciezka/do/pliku.csv"
BIGQUERY_DATASET = "twoj_bigquery_dataset"
BIGQUERY_TABLE = "twoja_bigquery_tabela"
PUBSUB_TOPIC = "twoj_topic"

# Definiujemy DAG z podstawową konfiguracją
with DAG(
    "gcs_to_bigquery_with_pubsub",
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
) as dag:

    # 1. Sensor do sprawdzenia, czy plik istnieje w Google Cloud Storage
    check_gcs_file = GCSObjectExistenceSensor(
        task_id="check_gcs_file",
        bucket=GCS_BUCKET_NAME,
        object=GCS_FILE_PATH,
    )

    # 2. Przeniesienie danych z GCS do BigQuery
    load_data_to_bq = GCSToBigQueryOperator(
        task_id="load_data_to_bq",
        bucket=GCS_BUCKET_NAME,
        source_objects=[GCS_FILE_PATH],
        destination_project_dataset_table=f"{GCP_PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_TABLE}",
        source_format="CSV",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
    )

    # 3. Sprawdzenie, czy dane zostały poprawnie załadowane do BigQuery
    check_bq_data = BigQueryCheckOperator(
        task_id="check_bq_data",
        sql=f"SELECT COUNT(1) > 0 FROM `{GCP_PROJECT_ID}.{BIGQUERY_DATASET}.{BIGQUERY_TABLE}`",
        use_legacy_sql=False,
    )

    # 4. Opublikowanie wiadomości do Pub/Sub
    publish_to_pubsub = PubSubPublishMessageOperator(
        task_id="publish_to_pubsub",
        project_id=GCP_PROJECT_ID,
        topic=PUBSUB_TOPIC,
        messages=[
            {
                "data": json.dumps({"status": "completed", "table": BIGQUERY_TABLE}),
                "attributes": {"source": "airflow", "dataset": BIGQUERY_DATASET},
            }
        ],
    )

    # Definiowanie kolejności zadań
    check_gcs_file >> load_data_to_bq >> check_bq_data >> publish_to_pubsub