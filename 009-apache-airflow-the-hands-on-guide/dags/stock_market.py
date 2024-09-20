from airflow.decorators import dag
from datetime import datetime

@dag(
	start_date=datetime(2024, 1, 1),
	schedule='@daily',
	catchup=False
)

def stock_market():
	pass

stock_market()