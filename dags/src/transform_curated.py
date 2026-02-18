import pandas as pd

def transform_curated():
    df = pd.read_parquet("/opt/airflow/datalake/trusted/products.parquet")

    df["price"] = df["price"].astype(float)

    df.to_parquet("/opt/airflow/datalake/curated/products.parquet")

    print("Transform curated concluído")
