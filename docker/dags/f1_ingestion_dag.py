from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "airflow",
    "start_date": datetime(2023, 1, 1),
    "retries": 1,
}

with DAG(
    dag_id="f1_ingestion_dag",
    default_args=default_args,
    schedule_interval=None,  # manually trigger for now
    catchup=False,
    description="Download Formula 1 data and upload to GCS",
) as dag:

    download_data = BashOperator(
        task_id="download_kaggle_data",
        bash_command="python3 scripts/download_f1_data.py"
    )

    upload_to_gcs = BashOperator(
        task_id="upload_to_gcs",
        bash_command="python3 scripts/upload_to_gcs.py"
    )

    download_data >> upload_to_gcs

# trigger reload
