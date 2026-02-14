import logging
from datetime import datetime
from pathlib import Path
import pandas as pd
import requests
from src.db import get_connection 
 
def save_to_postgres(data, execution_date):

    conn = get_connection()
    cursor = conn.cursor()

    for row in data:
        cursor.execute("""
            INSERT INTO products (
                product_id,
                title,
                category,
                price,
                rating,
                stock,
                brand,
                last_execution_date
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (product_id)
            DO UPDATE SET
                title = EXCLUDED.title,
                category = EXCLUDED.category,
                price = EXCLUDED.price,
                rating = EXCLUDED.rating,
                stock = EXCLUDED.stock,
                brand = EXCLUDED.brand,
                last_execution_date = EXCLUDED.last_execution_date;
        """, (
            row["product_id"],
            row["title"],
            row["category"],
            row["price"],
            row["rating"],
            row["stock"],
            row["brand"],
            execution_date
        ))

    conn.commit()
    cursor.close()
    conn.close()


def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / f"ingestion_{datetime.now():%Y%m%d_%H%M%S}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


def fetch_api_data():
    url = "https://dummyjson.com/products"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()["products"]


def normalize_data(raw_data):
    normalized = []

    for item in raw_data:
        normalized.append({
            "product_id": item.get("id"),
            "title": item.get("title"),
            "category": item.get("category"),
            "price": item.get("price"),
            "rating": item.get("rating"),
            "stock": item.get("stock"),
            "brand": item.get("brand")
        })

    return normalized


def validate_data(data):
    if not data:
        raise ValueError("Nenhum dado retornado após normalização")

    logging.info(f"Quantidade de registros processados: {len(data)}")

    # Mostrar 5 linhas no log
    sample = data[:5]
    logging.info("Amostra de 5 registros normalizados:")
    
    for row in sample:
        logging.info(row)



def save_to_parquet(data, execution_date):
    df = pd.DataFrame(data)

    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = (
        output_dir /
        f"products_{execution_date:%Y%m%d}.parquet"
    )

    df.to_parquet(output_path, index=False)

    logging.info(f"Arquivo salvo em: {output_path}")

