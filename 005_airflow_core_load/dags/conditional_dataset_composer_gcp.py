from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.pubsub import PubSubPublishMessageOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.datasets import Dataset
from datetime import datetime

# Definicja datasetów - plik w GCS jako wyzwalacz i przetworzony dataset dla BigQuery
gcs_file = Dataset("gs://data_stream_gcs/datasets/output.csv")
bq_table = Dataset("bq://third-essence-345723.temp.output")

# Konfiguracja zmiennych środowiskowych
GCS_BUCKET = "data_stream_gcs"
GCS_FILE_PATH = "datasets/output.csv"
BQ_DATASET = "temp"
BQ_TABLE = "output"
PROJECT_ID = "third-essence-345723"
TOPIC_ID = "projects/third-essence-345723/topics/data_stream"

# Funkcja tworząca plik bezpośrednio w GCS
def create_file_in_gcs():
    gcs_hook = GCSHook()
    file_content = "name,age\nJohn Doe,30\nJane Doe,25"
    gcs_hook.upload(bucket_name=GCS_BUCKET, object_name=GCS_FILE_PATH, data=file_content)

# DAG do generowania danych i zapisu w GCS
with DAG(
    "generate_data_to_gcs",
    start_date=datetime(2023, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["gcp"]
) as dag1:

    # Task do tworzenia pliku w GCS
    create_file_task = PythonOperator(
        task_id="create_file_in_gcs",
        python_callable=create_file_in_gcs
    )

# DAG do załadowania danych z GCS do BigQuery po aktualizacji Dataset
with DAG(
    "load_gcs_to_bigquery",
    start_date=datetime(2023, 1, 1),
    schedule=[gcs_file],  # uruchomienie przy aktualizacji pliku w GCS
    catchup=False,
    tags=["gcp"]
) as dag2:

    load_to_bq = GCSToBigQueryOperator(
        task_id="load_to_bigquery",
        bucket=GCS_BUCKET,
        source_objects=[GCS_FILE_PATH],
        destination_project_dataset_table=f"{PROJECT_ID}:{BQ_DATASET}.{BQ_TABLE}",
        source_format="CSV",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        outlets=[bq_table],  # definiuje BigQuery jako dataset wyjściowy
    )

# DAG do wysyłania powiadomienia po zakończeniu przetwarzania w BigQuery
with DAG(
    "notify_completion",
    start_date=datetime(2023, 1, 1),
    schedule=[bq_table],  # uruchomienie przy aktualizacji tabeli w BigQuery
    catchup=False,
    tags=["gcp"]
) as dag3:

    notify_task = PubSubPublishMessageOperator(
        task_id="send_pubsub_message",
        project_id=PROJECT_ID,
        topic=TOPIC_ID,
        messages=[{"data": "Przetwarzanie danych zakończone"}]
    )