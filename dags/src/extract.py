import requests
import pandas as pd

def extract_data():
    url = "https://dummyjson.com/products"
    response = requests.get(url)
    data = response.json()["products"]

    df = pd.DataFrame(data)
    df.to_parquet("/opt/airflow/datalake/raw/products.parquet")

    print("Extract concluído")

