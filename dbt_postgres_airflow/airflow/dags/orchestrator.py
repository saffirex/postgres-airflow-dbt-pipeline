from airflow import DAG
from datetime import datetime, timedelta

from airflow.providers.standard.operators.python import PythonOperator
import sys
sys.path.append("/opt/airflow/scripts")


from insert_records import main

default_args = {
    "description": "A DAG to orchestrate data",
    "start_date": datetime(2025, 6, 23),
    "catchup": False,
        
}

dag = DAG(
    dag_id = "weather-api-orchestrator",
    default_args= default_args,
    schedule = timedelta(minutes=5)
)

with dag:
    task1 = PythonOperator(
        task_id = "ingest-data-task",
        python_callable= main
        
    )