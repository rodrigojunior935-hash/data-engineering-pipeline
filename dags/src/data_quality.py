import pandas as pd
import csv
import os
import logging
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text


# ==============================
# Configuração de caminhos
# ==============================

BASE_DIR = "/opt/airflow"

LOG_PATH = os.path.join(BASE_DIR, "data_quality", "logs", "quality_log.csv")
VOLUME_PATH = os.path.join(BASE_DIR, "data_quality", "logs", "volume_log.csv")


# ==============================
# Funções auxiliares
# ==============================

def table_exists(engine, schema, table):
    query = text("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = :schema
            AND table_name = :table
        );
    """)

    with engine.connect() as conn:
        result = conn.execute(query, {"schema": schema, "table": table})
        return result.scalar()


def log_validation(validation_name, status, detail):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

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
    os.makedirs(os.path.dirname(VOLUME_PATH), exist_ok=True)

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
# Função principal
# ==============================

def run_quality_checks():

    logging.info("Iniciando validações de qualidade...")

    engine = create_engine(
        "postgresql://postgres:postgres@project10-postgres_dw-1:5432/postgres"
    )

    try:

        # Verifica se tabela existe
        if not table_exists(engine, "dw", "fact_sales"):
            error_msg = "Tabela dw.fact_sales não existe no DW."
            log_validation("estrutura", "FALHA", error_msg)
            raise ValueError(error_msg)

        df = pd.read_sql("SELECT * FROM dw.fact_sales", engine)

        # Executa validações
        validate_row_count(df)
        validate_no_nulls(df, ["category"])
        validate_no_duplicates(df, "category")

        # Registra volume histórico
        log_volume(df)

        logging.info("Validações executadas com sucesso.")

    except Exception as e:

        logging.error("Erro detectado na validação de dados.")

        # 🔥 AQUI ENTRA A IA
        analysis = analyze_pipeline_error(str(e))

        logging.error("===== ANALISE IA =====")
        logging.error(analysis)

        # mantém comportamento original (falha a DAG)
        raise