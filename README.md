# Verificador de Processos Judiciais com IA

Aplicação de Inteligência Artificial Generativa para análise automática
de elegibilidade de processos judiciais, garantindo conformidade com
políticas internas através de RAG (Retrieval-Augmented Generation) e
LLMs.

## Sumário

-   [Visão Geral](#visão-geral)
-   [Principais Funcionalidades](#principais-funcionalidades)
-   [Arquitetura da Solução](#arquitetura-da-solução)
-   [Diagrama da Arquitetura](#diagrama-da-arquitetura)
-   [Tecnologias Utilizadas](#tecnologias-utilizadas)
-   [Como Executar o Projeto](#como-executar-o-projeto)
    -   [Pré-requisitos](#pré-requisitos)
    -   [Clonar o Repositório](#clonar-o-repositório)
    -   [Configurar Variáveis de
        Ambiente](#configurar-variáveis-de-ambiente)
    -   [Rodar com Docker Compose](#rodar-com-docker-compose)
-   [Executando os Testes](#executando-os-testes)
-   [Guia de Uso](#guia-de-uso)
    -   [Interface Visual (Streamlit)](#interface-visual-streamlit)
    -   [API REST](#api-rest)
-   [Decisões Técnicas (Rationale)](#decisões-técnicas-rationale)
-   [Estrutura do Projeto](#estrutura-do-projeto)
-   [Autor](#autor)

## Visão Geral

O sistema recebe dados estruturados de um processo judicial, consulta
uma base de políticas internas e utiliza um modelo generativo para
decidir se o processo deve ser **Aprovado**, **Rejeitado** ou
classificado como **Incompleto**.

A decisão é sempre retornada em **JSON estruturado**, com justificativa
e citações das políticas aplicadas.

## Principais Funcionalidades

-   **Validação de Contrato**
    As entradas são validadas com Pydantic, garantindo integridade dos
    dados.

-   **RAG Híbrido**
    Uso de ChromaDB + embeddings locais para recuperação das políticas
    relevantes com velocidade e zero custo de API.

-   **Decisão Estruturada**
    O LLM retorna estritamente um JSON padronizado, facilitando
    integrações.

-   **Observabilidade Completa**
    LangSmith integrado para rastreamento de prompts, latência, custos e
    fluxos.

-   **Interface Visual**
    UI em Streamlit para testes manuais rápidos.

## Arquitetura da Solução

A aplicação segue um design baseado em **microsserviços
containerizados**, separando UI, backend, pipeline de RAG e camada de
vetores.

## Diagrama da Arquitetura

``` mermaid
graph LR
    A[User / Client] --> B(Streamlit UI :8501)
    A --> C(FastAPI Backend :8000)
    B --> C
    C --> D{LangChain Engine}
    D --> E[(ChromaDB Vector Store)]
    D --> F[Google Gemini API]
    D -.-> G[LangSmith Observability]
```

## Tecnologias Utilizadas

-   Orquestração de LLM: LangChain
-   LLM: Google Gemini 2.5 Flash
-   Embeddings: all-MiniLM-L6-v2 (HuggingFace)
-   Vector DB: ChromaDB
-   Backend: FastAPI + Uvicorn
-   Frontend: Streamlit
-   Observabilidade: LangSmith
-   Infra: Docker e Docker Compose

## Como Executar o Projeto

### Pré-requisitos

-   Docker
-   Chave de API do Google Gemini
-   Chave de API do LangSmith

### Clonar o Repositório

``` bash
git clone https://github.com/albertvinicius10/verificador_processos_judiciais.git
cd verificador_processos_judiciais
```

### Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

    GOOGLE_API_KEY=sua_chave_google_api_aqui

    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
    LANGCHAIN_API_KEY=sua_chave_langsmith_aqui
    LANGCHAIN_PROJECT=juscash-case

### Rodar com Docker Compose

``` bash
docker-compose up --build
```

## Executando os Testes

``` bash
docker-compose exec api pytest
```

## Guia de Uso

### Interface Visual (Streamlit)

1.  Acesse `http://localhost:8501`
2.  Cole o JSON do processo
3.  Clique em *Analisar Processo*
4.  Visualize decisão, justificativa e políticas citadas

### API REST

    http://localhost:8000/docs

## Decisões Técnicas 

### RAG Híbrido

-   Embeddings gerados localmente via HuggingFace
-   Evita rate limits da API
-   Reduz custo e latência

### Uso de Pydantic

-   Esquemas estritos
-   Zero alucinação de estrutura
-   Integração segura com UI

### Observabilidade com LangSmith

-   Rastreia cada execução
-   Analisa documentos recuperados
-   Mede custo e latência

## Estrutura do Projeto

    verificador_processos_judiciais/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── ui.py
    │   ├── engine.py
    │   ├── rag.py
    │   ├── schemas.py
    │   └── policies.txt
    ├── chroma_data/
    ├── .env
    ├── docker-compose.yml
    ├── Dockerfile
    ├── requirements.txt
    └── README.md

## Autor

Projeto desenvolvido por **Albert Vinicius**.
