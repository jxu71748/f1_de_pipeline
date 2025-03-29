from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
import os

# DAG default arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
}

# Define paths inside container
RAW_DATA_PATH = "/opt/airflow/raw_data"
TRANSFORMED_DATA_PATH = "/opt/airflow/data/transformed"
SCRIPT_PATH = "/opt/airflow/scripts/spark_transform.py"

with DAG(
    dag_id='f1_transform_dag',
    default_args=default_args,
    schedule_interval=None,  # manual trigger
    catchup=False,
    description='Transform raw CSVs to cleaned Parquet using PySpark',
) as dag:

    spark_transform = BashOperator(
        task_id='run_spark_transform',
        bash_command=f"""
        /opt/spark/bin/spark-submit \
            --master local[*] \
            {SCRIPT_PATH}
        """
    )

    spark_transform
