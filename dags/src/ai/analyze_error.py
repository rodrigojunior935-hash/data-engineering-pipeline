import logging

def analyze_pipeline_error(log_text: str):

    prompt = f"""
    Analise o erro abaixo do pipeline de dados e explique:

    1. Causa provável
    2. Impacto no pipeline
    3. Possível solução

    Erro:
    {log_text}
    """

    logging.info("Simulando análise de erro via IA")

    return f"""
    ANALISE AUTOMATICA:

    Erro identificado: {log_text}

    Possível causa:
    - Problema estrutural no DW
    - Dados inconsistentes
    - Falha de volume ou duplicidade

    Ação recomendada:
    - Verificar tabela e dados na staging
    - Validar execução do dbt
    - Conferir integridade do schema
    """