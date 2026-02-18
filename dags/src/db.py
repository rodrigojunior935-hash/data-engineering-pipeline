from sqlalchemy import create_engine

def get_engine():
    engine = create_engine(
        "postgresql+psycopg2://airflow:airflow@postgres/airflow"
    )
    return engine

