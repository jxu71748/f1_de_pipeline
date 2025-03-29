from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
import os

# Default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

# DAG definition
with DAG(
    dag_id='f1_upload_silver_dag',
    default_args=default_args,
    schedule_interval=None,  # manual trigger
    catchup=False,
    description='Upload cleaned Parquet files to GCS (silver layer)',
) as dag:

    upload_silver = BashOperator(
        task_id='upload_parquet_to_gcs',
        bash_command="""
        /opt/spark/bin/spark-submit \
            --master local[*] \
        /opt/airflow/scripts/upload_parquet_to_gcs.py
        """
    )

    upload_silver
