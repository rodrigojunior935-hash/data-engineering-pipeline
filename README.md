Evolução do pipeline de dados com uma camada de inteligência artificial para análise automática de erros, geração de SQL e documentação assistida por LLM.


✨ Highlights

🧠 LLM-ready architecture — módulo de IA desacoplado, pronto para integrar qualquer LLM provider (OpenAI, Anthropic, Ollama, etc.)
🔍 Automated error analysis — falhas no pipeline disparam análise automática via prompt engineering, com diagnóstico de causa raiz, impacto e sugestão de correção
⚙️ AI-assisted SQL generation — geração de modelos dbt incrementais a partir de descrição em linguagem natural
📄 DAG auto-documentation — documentação automática do pipeline gerada via LLM a partir do próprio código-fonte
🔗 Native Airflow integration — IA integrada como task dentro da DAG, sem alterar a arquitetura principal


🏗️ Arquitetura
pipeline_dag.py (Apache Airflow)
│
├── extract          → Ingestão de dados brutos
├── transform        → Camadas trusted e curated
├── load_minio       → Upload para object storage (MinIO)
├── spark_task       → Processamento distribuído (Apache Spark)
├── dbt_run          → Transformações analíticas (dbt Core)
├── data_quality     → Validações de qualidade com análise de erro via LLM
└── ai_debug         → Task de diagnóstico assistido por IA
         │
         └── src/ai/
              ├── analyze_error.py      → Prompt engineering para root cause analysis
              ├── generate_dbt_model.py → Text-to-SQL via LLM
              └── document_dag.py       → Auto-documentação de pipelines
Stack principal:
CamadaTecnologiaOrquestraçãoApache AirflowProcessamentoApache SparkTransformaçãodbt CoreObject StorageMinIO (S3-compatible)Camada de IALLM-agnostic (plugável)Prompt LayerPython + prompt engineering

📁 Estrutura do Projeto
project_11_IA_aplicada/
├── docker-compose.yaml
├── dags/
│   ├── pipeline_dag.py
│   └── src/
│       ├── extract.py
│       ├── transform_trusted.py
│       ├── transform_curated.py
│       ├── load_minio.py
│       ├── spark_task.py
│       ├── data_quality.py
│       └── ai/
│           ├── analyze_error.py
│           ├── generate_dbt_model.py
│           └── document_dag.py
├── dbt/
├── spark/
├── datalake/
└── data_quality/

🚀 Como rodar localmente
Pré-requisitos

Docker + Docker Compose
Python 3.9+
Git

1. Clone o repositório
bashgit clone https://github.com/<seu-usuario>/project_11_IA_aplicada.git
cd project_11_IA_aplicada
2. Suba os containers
bashdocker-compose up -d
3. Acesse o Airflow
URL:      http://localhost:8080
Usuário:  airflow
Senha:    airflow
4. Ative e rode a DAG
No Airflow UI, ative a DAG pipeline_dag e dispare manualmente ou aguarde o schedule.
5. (Opcional) Testar o módulo de IA isolado
bash# A partir da raiz do projeto
python -c "
from dags.src.ai.analyze_error import analyze_pipeline_error
result = analyze_pipeline_error('Tabela dw.fact_sales nao existe no DW')
print(result)
"
bash# Testar geração de SQL
python -c "
from dags.src.ai.generate_dbt_model import generate_dbt_model
sql = generate_dbt_model('Criar agregação de vendas por categoria')
print(sql)
"
6. (Opcional) Integrar um LLM real
No analyze_error.py, substitua o bloco de resposta simulada pela chamada ao provider de sua escolha:
python# Exemplo com OpenAI
import openai

client = openai.OpenAI(api_key="sua-chave")
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
return response.choices[0].message.content

🧠 Sobre a camada de IA
O módulo src/ai/ foi projetado como uma abstraction layer sobre qualquer LLM provider. Os prompts são construídos com técnicas de prompt engineering estruturado, permitindo:

Trocar o provider (OpenAI → Ollama → Anthropic) sem alterar o pipeline
Evoluir os prompts de forma isolada sem risco de regressão
Testar as funções de IA de forma independente da DAG


👤 Autor
Desenvolvido como parte de um portfólio de Engenharia de Dados moderno, demonstrando integração de LLMs em pipelines de produção com Apache Airflow, Spark e dbt.
