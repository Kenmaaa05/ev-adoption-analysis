from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os

# Add the scripts folder to the path (optional if your scripts are in the same folder)
sys.path.append(os.path.join(os.path.dirname(__file__)))

from download_data import download_csv
from cleaning import clean_ev_data
from load_to_postgres import load_to_postgres

default_args = {
    'owner': 'kenmaaa',
    'start_date': datetime(2024, 1, 1),
    'retries': 0
}

with DAG(
    dag_id='ev_data_pipeline',
    default_args=default_args,
    description='ETL pipeline for WA EV adoption data',
    schedule=None,  # Use `schedule` in Airflow 3.x instead of `schedule_interval`
    catchup=False,
    tags=['ev', 'etl']
) as dag:

    task_download = PythonOperator(
        task_id='download_ev_csv',
        python_callable=download_csv
    )

    task_clean = PythonOperator(
        task_id='clean_data',
        python_callable=clean_ev_data
    )

    task_load = PythonOperator(
        task_id='load_to_postgres',
        python_callable=load_to_postgres
    )

    task_download >> task_clean >> task_load
