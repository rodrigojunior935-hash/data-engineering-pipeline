from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from run_pipeline import run_pipeline

with DAG(
    dag_id="pipeline_local",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    run_pipeline_task = PythonOperator(
        task_id="run_pipeline",
        python_callable=run_pipeline,
        retries=2,
    )
