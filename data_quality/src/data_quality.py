import pandas as pd
import csv
import os
import logging
from datetime import datetime, timedelta
from sqlalchemy import create_engine


# Caminhos dos arquivos de log
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(BASE_PATH, "logs", "quality_log.csv")
VOLUME_PATH = os.path.join(BASE_PATH, "logs", "volume_log.csv")


# ==============================
# Funções de Log
# ==============================

def log_validation(validation_name, status, detail):
    file_exists = os.path.isfile(LOG_PATH)

    with open(LOG_PATH, mode="a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["data", "validacao", "status", "detalhe"])

        writer.writerow([
            datetime.now(),
            validation_name,
            status,
            detail
        ])


def log_volume(df):
    file_exists = os.path.isfile(VOLUME_PATH)

    with open(VOLUME_PATH, mode="a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["data", "row_count"])

        writer.writerow([datetime.now(), len(df)])


# ==============================
# Validações
# ==============================

def validate_row_count(df, min_rows=1):
    count = len(df)

    if count < min_rows:
        detail = f"Quantidade abaixo do esperado: {count}"
        log_validation("volume", "FALHA", detail)
        raise ValueError(detail)
    else:
        log_validation("volume", "OK", f"{count} linhas")


def validate_no_nulls(df, columns):
    for col in columns:
        nulls = df[col].isnull().sum()

        if nulls > 0:
            detail = f"{nulls} valores nulos na coluna {col}"
            log_validation("nulos", "FALHA", detail)
            raise ValueError(detail)
        else:
            log_validation("nulos", "OK", f"nenhum nulo em {col}")


def validate_no_duplicates(df, column):
    duplicates = df[column].duplicated().sum()

    if duplicates > 0:
        detail = f"{duplicates} duplicatas encontradas na coluna {column}"
        log_validation("duplicidade", "FALHA", detail)
        raise ValueError(detail)
    else:
        log_validation("duplicidade", "OK", "nenhuma duplicidade encontrada")


def validate_freshness(df, column, max_days=1):
    latest = df[column].max()
    limit = datetime.now() - timedelta(days=max_days)

    if latest < limit:
        detail = f"Dados desatualizados. Última data encontrada: {latest}"
        log_validation("freshness", "FALHA", detail)
        raise ValueError(detail)
    else:
        log_validation("freshness", "OK", f"última data: {latest}")


# ==============================
# Função principal chamada pelo Airflow
# ==============================

def run_quality_checks():

    logging.info("Iniciando validações de qualidade...")

    # Conexão com o DW do Projeto 10
    engine = create_engine(
        "postgresql://postgres:postgres@project10-postgres_dw-1:5432/postgres"
    )

    # Consulta na tabela do DW
    df = pd.read_sql("SELECT * FROM dw.fact_sales", engine)

    # Executa validações
    validate_row_count(df)
    validate_no_nulls(df, ["category"])
    validate_no_duplicates(df, "category")

    # Registra volume histórico
    log_volume(df)

    logging.info("Validações de qualidade executadas com sucesso.")
