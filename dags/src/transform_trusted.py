import pandas as pd

def transform_trusted():
    df = pd.read_parquet("/opt/airflow/datalake/raw/products.parquet")

    df = df[["id", "title", "price", "category"]]

    df.to_parquet("/opt/airflow/datalake/trusted/products.parquet")

    print("Transform trusted concluído")
