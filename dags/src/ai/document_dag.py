def document_dag(dag_code: str):

    prompt = f"""
    Documente a DAG abaixo explicando:

    - Objetivo
    - Fluxo
    - Dependências
    - Pontos críticos

    Código:
    {dag_code}
    """

    return """
    Esta DAG executa um pipeline completo:
    Extract → Transform → Upload → Spark → dbt → Data Quality.
    """