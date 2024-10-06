# 012_airflow_dbt_retail_project


'''
mkdir 012_airflow_dbt_retail_project
cd 012_airflow_dbt_retail_project
echo "# 012_airflow_dbt_retail_project" >> README.md

python3 -m venv venv && source venv/bin/activate

curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.2/docker-compose.yaml'

mkdir -p ./dags ./logs ./plugins ./config

echo -e "AIRFLOW_UID=$(id -u)" > .env
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

docker compose up -d
docker compose down

docker compose down && docker compose up -d
'''
