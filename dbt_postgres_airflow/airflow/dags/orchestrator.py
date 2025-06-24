from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount
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
    dag_id = "weather-api-dbt-orchestrator",
    default_args= default_args,
    schedule = timedelta(minutes=1)
)

with dag:
    task1 = PythonOperator(
        task_id = "ingest-data-task",
        python_callable= main
        
    )
    
    task2 = DockerOperator(
    task_id ='transform-data-task',
    image = 'ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
    command='run',
    working_dir='/usr/app',
    mounts=[
        Mount(source="/home/saffire/dlytica/internship/l-dbt/dbt_postgres_airflow/dbt/dbt_project", target="/usr/app", type="bind"),
        Mount(source="/home/saffire/dlytica/internship/l-dbt/dbt_postgres_airflow/dbt", target="/root/.dbt", type="bind")
        ],
    network_mode='postgres_my-network',
    mount_tmp_dir=False,
    docker_url="unix://var/run/docker.sock",
    auto_remove="success"
    
    )
    
    task1 >> task2