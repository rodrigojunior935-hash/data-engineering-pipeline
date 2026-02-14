import logging
from datetime import datetime

from src.utils import (
    save_to_postgres,
    setup_logging,
    fetch_api_data,
    normalize_data,
    validate_data,
    save_to_parquet
)

def run_pipeline():

    setup_logging()
    logging.info("Pipeline iniciado")

    raw_data = fetch_api_data()
    normalized_data = normalize_data(raw_data)

    validate_data(normalized_data)
    execution_date = datetime.now()

    save_to_parquet(normalized_data, execution_date)
    save_to_postgres(normalized_data, execution_date)        # estado atual

    logging.info("Pipeline finalizado com sucesso")


if __name__ == "__main__":
    run_pipeline()
