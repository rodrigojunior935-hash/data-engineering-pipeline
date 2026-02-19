Pipeline de Dados Local — Projeto 09

Pipeline de dados completo rodando localmente com Docker, cobrindo ingestão, transformação, armazenamento e modelagem.

## Tecnologias

- **Apache Airflow** — orquestração do pipeline
- **Apache Spark** — processamento distribuído
- **dbt** — modelagem e transformação de dados
- **MinIO** — armazenamento de objetos (S3-compatible)
- **PostgreSQL** — banco de dados (Airflow + Data Warehouse)
- **Docker Compose** — infraestrutura local

## Arquitetura
```
Extração → Transformação (Trusted) → Transformação (Curated) → MinIO → Spark → dbt
```

## Como rodar
```bash
# Subir o ambiente
docker compose -p project09 up -d

# Acessar o Airflow
http://localhost:8080
# usuário: airflow | senha: airflow

# Acessar o MinIO
http://localhost:9001
# usuário: admin | senha: admin123
```

## Estrutura
```
├── dags/          # DAGs do Airflow
│   └── src/       # Módulos do pipeline
├── dbt/           # Projeto dbt
├── spark/         # Jobs Spark
├── datalake/      # Dados locais
└── docker-compose.yaml
```

## Pipeline

1. **extract** — coleta os dados brutos
2. **transform_trusted** — limpeza e padronização
3. **transform_curated** — regras de negócio
4. **upload_to_minio** — armazena no data lake
5. **spark_processing** — processamento com Spark
6. **dbt_run** — modelagem no data warehouse
7. **dbt_test** — validação dos modelos

## Próximos passos

- **Projeto 10** — Observabilidade e qualidade de dados
- **Projeto 11** — IA aplicada ao pipeline
