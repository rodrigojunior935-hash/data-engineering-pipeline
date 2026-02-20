def generate_dbt_model(description: str):

    prompt = f"""
    Gere um modelo dbt incremental baseado na descrição:

    {description}

    Use source('staging','sales')
    Gere select organizado e profissional.
    """

    return f"""
    -- Modelo gerado automaticamente
    SELECT
        category,
        SUM(price) AS total_price
    FROM {{ source('staging','sales') }}
    GROUP BY category
    """