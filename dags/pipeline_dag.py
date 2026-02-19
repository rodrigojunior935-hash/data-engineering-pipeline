from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

from src.extract import extract_data
from src.transform_trusted import transform_trusted
from src.transform_curated import transform_curated
from src.load_minio import upload_to_minio
from src.spark_task import run_spark_job
from src.data_quality import run_quality_checks

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
    
    setup_staging = BashOperator(
    task_id="setup_staging",
    bash_command="""docker exec project10-postgres_dw-1 psql -U postgres -c "TRUNCATE staging.sales; INSERT INTO staging.sales VALUES ('A',100),('A',200),('B',150),('C',300);" """
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="docker exec project10-dbt-1 dbt run --project-dir /usr/app/dw_project --profiles-dir /usr/app/dw_project"
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="docker exec project10-dbt-1 dbt test --project-dir /usr/app/dw_project --profiles-dir /usr/app/dw_project"
    )

    data_quality = PythonOperator(
        task_id="data_quality_check",
        python_callable=run_quality_checks
    )

    extract >> trusted >> curated >> upload >> spark >> setup_staging >> dbt_run >> dbt_test >> data_quality

