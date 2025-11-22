Verificador de Processos Judiciais com IA
Trata-se de uma aplicação de IA Generativa que automatiza a análise de elegibilidade de processos judiciais, verificando conformidade com políticas de negócio através de LLMs e RAG (Retrieval-Augmented Generation).

Visão Geral do Projeto
O sistema recebe dados estruturados de um processo judicial, consulta uma base de conhecimento de políticas internas e utiliza o Google Gemini para decidir se o processo deve ser Aprovado, Rejeitado ou classificado como Incompleto.

Principais Funcionalidades

Validação de Contrato: Garantia de integridade dos dados de entrada via Pydantic.


RAG Híbrido: Utilização de banco vetorial (ChromaDB) com embeddings locais (HuggingFace) para recuperação eficiente de regras de negócio sem latência de API.


Decisão Estruturada: O LLM retorna estritamente um JSON contendo decisão, justificativa e citações das políticas aplicadas.



Observabilidade Total: Integração com LangSmith para rastreamento de traces, custos e versionamento de prompts em tempo real.


Interface Visual: UI interativa em Streamlit para testes manuais rápidos.

Arquitetura da Solução
A aplicação foi desenhada seguindo o padrão de microsserviços containerizados:

Snippet de código

graph LR
    A[User / Client] --> B(Streamlit UI :8501)
    A --> C(FastAPI Backend :8000)
    B --> C
    C --> D{LangChain Engine}
    D --> E[(ChromaDB Vector Store)]
    D --> F[Google Gemini API]
    D -.-> G[LangSmith Observability]

Tecnologias Utilizadas
Orquestração de LLM: LangChain

LLM: Google Gemini 2.5 Flash (Eficiência de custo e janela de contexto)

Embeddings: all-MiniLM-L6-v2 (HuggingFace - Execução local na CPU para evitar Rate Limits)

Vector DB: ChromaDB (Persistente)

Backend: FastAPI + Uvicorn

Frontend: Streamlit

Infra: Docker & Docker Compose

Como Executar o Projeto
Pré-requisitos:

Docker.

Uma chave de API do Google AI Studio (Gemini).

Uma chave de API do LangSmith para observabilidade.

1. Clonar o Repositório
Bash

git clone https://github.com/albertvinicius10/verificador_processos_judiciais.git
cd verificador_processos_judiciais
2. Configurar Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto. Você pode usar o modelo abaixo:

Exemplo de .env:

# Obrigatório: Motor de Inteligência Artificial
GOOGLE_API_KEY=sua_chave_google_api_aqui

LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY=sua_chave_langsmith_aqui
LANGCHAIN_PROJECT="juscash-case"

3. Executar com Docker Compose

Este comando irá construir as imagens, baixar os modelos de embedding e iniciar os serviços.

docker-compose up --build
Nota: Na primeira execução, pode levar alguns instantes para baixar o modelo de embedding do HuggingFace.



Executando os Testes
O projeto inclui uma suíte de testes automatizados (pytest) para validar a saúde da API, a conexão com o LLM e o cumprimento do contrato de dados.

Para rodar os testes dentro do container em execução:

docker-compose exec api pytest

Guia de Uso
Interface Visual (UI)
Acesse http://localhost:8501 no seu navegador.

Cole o JSON do processo na área de texto.

Clique em "Analisar Processo".

Visualize a decisão colorida (Approved/Rejected/Incomplete), a justificativa e as políticas citadas.

API Rest
A documentação interativa (Swagger/OpenAPI) está disponível em http://localhost:8000/docs.


Decisões Técnicas (Rationale)
Estratégia de RAG Híbrida (Local Embeddings + Cloud LLM):

Decisão: Utilizar LangChain + HuggingFaceEmbeddings (modelo all-MiniLM-L6-v2) rodando localmente na CPU para a vetorização, deixando apenas a geração de texto (chat) para a API do Google.

Motivo: A API de Embeddings do Google possui rate-limits restritivos no tier gratuito (erros 429). A execução local garante estabilidade, zero latência de rede na indexação e elimina custos de API para a etapa de retrieval.

Uso de Pydantic:

A definição rigorosa dos esquemas de entrada (ProcessoInput) e saída (AnaliseJuridicaOutput) garante que o LLM nunca alucine a estrutura do JSON, facilitando a integração com o front-end e sistemas externos.

LangSmith para Observabilidade:

Para cumprir o requisito de monitoramento de fluxos, o LangSmith foi integrado nativamente. Isso permite auditar cada execução, verificar o tempo de latência do LLM e inspecionar exatamente quais documentos o RAG recuperou para cada decisão.
Estrutura do Projeto
Plaintext

juscash-case/
├── app/
│   ├── __init__.py
│   ├── main.py          # Entrypoint da API FastAPI
│   ├── ui.py            # Interface Streamlit
│   ├── engine.py        # Lógica de Orquestração (LangChain)
│   ├── rag.py           # Gestão do ChromaDB e Embeddings
│   ├── schemas.py       # Modelos de Dados (Pydantic)
│   └── policies.txt     # Base de conhecimento (Políticas)
├── chroma_data/         # Persistência do Banco Vetorial (GitIgnore)
├── .env                 # Variáveis de Ambiente (GitIgnore)
├── docker-compose.yml   # Orquestração de Containers
├── Dockerfile           # Definição da Imagem
├── requirements.txt     # Dependências Python
└── README.md            # Documentação

Projeto entregue por Albert Vinicius.