from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

from src.extract import extract_data
from src.transform_trusted import transform_trusted
from src.transform_curated import transform_curated
from src.load_minio import upload_to_minio
from src.spark_task import run_spark_job

with DAG(
    dag_id="pipeline_local",
    start_date=datetime(2024,1,1),
    schedule=None,
    catchup=False,
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_data
    )

    trusted = PythonOperator(
        task_id="transform_trusted",
        python_callable=transform_trusted
    )

    curated = PythonOperator(
        task_id="transform_curated",
        python_callable=transform_curated
    )

    upload = PythonOperator(
        task_id="upload_to_minio",
        python_callable=upload_to_minio
    )

    spark = PythonOperator(
        task_id="spark_processing",
        python_callable=run_spark_job
    )

    extract >> trusted >> curated >> upload >> spark
