from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__))) # added cuz just in case

from download_data import download_csv
from cleaning import clean_ev_data
from load_to_postgres import load_to_postgres

default_args = {
    'owner': 'kenmaaa',
    'start_date': datetime(2025, 6, 23),
    'retries': 0
}

with DAG(
    dag_id='ev_data_pipeline',
    default_args=default_args,
    description='ETL pipeline for WA EV adoption data',
    schedule= '0 0 23 * *',  
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
