from __future__ import annotations
import pendulum
from airflow.datasets import Dataset
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

# [START dataset_def]
# Definiujemy zestaw danych, który będzie używany przez zadania w DAG
my_dataset = Dataset("s3://my_bucket/output.txt", extra={"info": "data produced"})
# [END dataset_def]

with DAG(
    dag_id="simple_data_producer",
    catchup=False,
    start_date=pendulum.datetime(2023, 10, 1, tz="UTC"),  # Ustalamy datę początkową DAG
    schedule="@daily",  # DAG uruchamia się codziennie
    tags=["c"]
) as dag_producer:

    # [START task_outlet]
    # Zadanie, które generuje zestaw danych
    BashOperator(
        outlets=[my_dataset],  # Określamy zestaw danych, który będzie tworzony przez to zadanie
        task_id="generate_data",  # Identyfikator zadania
        bash_command="echo 'Producing data' > /tmp/output.txt"  # Komenda do generacji danych
    )
    # [END task_outlet]

# DAG konsumenta, który reaguje na zestaw danych
with DAG(
    dag_id="simple_data_consumer",
    catchup=False,
    start_date=pendulum.datetime(2023, 10, 1, tz="UTC"),
    schedule=[my_dataset],  # Ustalamy, że zadanie uruchamia się po aktualizacji zestawu danych
    tags=["c"]
) as dag_consumer:

    # [START task_consume]
    # Zadanie, które konsumuje zestaw danych
    BashOperator(
        task_id="consume_data",  # Identyfikator zadania
        bash_command="cat /tmp/output.txt"  # Komenda do przetwarzania danych
    )
    # [END task_consume]