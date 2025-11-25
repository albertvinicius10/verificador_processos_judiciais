# ⚖️ JusCash AI Verifier

Este projeto é uma ferramenta de verificação de processos judiciais que utiliza Inteligência Artificial Generativa (LLMs) e Retrieval Augmented Generation (RAG) para analisar a elegibilidade de compra de créditos de processos. Ele é composto por uma API FastAPI (backend) e uma interface de usuário Streamlit (frontend), ambos conteinerizados com Docker.

##  Funcionalidades

-   **Análise de Elegibilidade**: Avalia processos judiciais com base em um conjunto de políticas/regras de negócio.
-   **IA Generativa (LLMs)**: Utiliza modelos como Gemini (Google) ou GPT (OpenAI) para interpretar e aplicar as políticas.
-   **Retrieval Augmented Generation (RAG)**: Recupera políticas relevantes de uma base de conhecimento (ChromaDB) para fundamentar as decisões da IA.
-   **Interface Amigável**: Frontend interativo construído com Streamlit para entrada de dados JSON e visualização dos resultados.
-   **Decisões Claras**: Retorna `approved`, `rejected` ou `incomplete` com justificativa e citação das políticas aplicadas.
-   **Ambiente Conteinerizado**: Fácil setup e execução via Docker Compose.
-   **Configurável**: Suporte a diferentes provedores de LLM (Google Gemini, OpenAI GPT) via variáveis de ambiente.

##  Como Rodar Localmente

Para configurar e rodar o projeto em seu ambiente de desenvolvimento local, siga os passos abaixo:

### Pré-requisitos

-   **Docker Desktop** (ou Docker Engine e Docker Compose) instalado e rodando.
-   Uma chave de API para o provedor de LLM de sua escolha (Google Gemini ou OpenAI).

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/verificador_processos_judiciais.git
cd verificador_processos_judiciais
```

### 2. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com suas chaves de API. Escolha entre `GOOGLE_API_KEY` ou `OPENAI_API_KEY` e defina `LLM_PROVIDER` de acordo.

Exemplo para Google Gemini:

```dotenv
LLM_PROVIDER=google
GOOGLE_API_KEY=SUA_CHAVE_API_GOOGLE
# Opcional: LANGCHAIN_API_KEY para tracing no LangSmith
LANGCHAIN_API_KEY=SUA_CHAVE_LANGSMITH
```

Exemplo para OpenAI GPT:

```dotenv
LLM_PROVIDER=openai
OPENAI_API_KEY=SUA_CHAVE_API_OPENAI
# Opcional: LANGCHAIN_API_KEY para tracing no LangSmith
LANGCHAIN_API_KEY=SUA_CHAVE_LANGSMITH
```

Você também pode especificar o modelo LLM, se desejar:

```dotenv
# Para Google
LLM_MODEL=gemini-1.5-flash
# Para OpenAI
# LLM_MODEL=gpt-4o
```

### 3. Inicie os Contêineres

Utilize o arquivo `docker-compose.local.yml` para iniciar os serviços de API e Frontend, sem Nginx ou Certbot, otimizado para desenvolvimento local.

```bash
docker-compose -f docker-compose.local.yml up --build
```

-   O `--build` garante que as imagens Docker sejam construídas (ou reconstruídas) com as últimas alterações.
-   Este comando pode levar alguns minutos na primeira execução, pois baixará as imagens base e instalará as dependências.

### 4. Acesse a Aplicação

Após os contêineres estarem rodando, você pode acessar:

-   **Frontend (Streamlit UI)**: http://localhost:8501
-   **API (FastAPI Docs)**: http://localhost:8000/docs

### 5. Parar os Contêineres

Para parar e remover os contêineres, execute:

```bash
docker-compose -f docker-compose.local.yml down
```

##  Uso da Interface

1.  Acesse a UI no seu navegador (`http://localhost:8501`).
2.  Você verá uma caixa de texto pré-preenchida com um JSON de exemplo.
3.  **Cole o JSON do processo** que deseja analisar na caixa de texto.
    -   Certifique-se de incluir campos como `valorCausa` e `valorCondenacao`. Se `valorCondenacao` estiver ausente, o sistema pode retornar `incomplete` conforme as políticas.
4.  Clique em **" Analisar Processo"**.
5.  O resultado da análise (APROVADO, REJEITADO, INCOMPLETO), a justificativa e as políticas citadas serão exibidos.

##  Testando a Aplicação

Após iniciar os contêineres, você pode testar a aplicação de duas maneiras principais:

### 1. Teste End-to-End (via Frontend)

Esta é a forma mais simples de verificar o fluxo completo.

1.  Acesse a interface do Streamlit em `http://localhost:8501`.
2.  Cole diferentes variações do JSON na área de texto para testar os cenários:
    -   Um JSON válido que deve ser aprovado.
    -   Um JSON que viole uma política (ex: `valorCondenacao` abaixo de 1000) para ver a resposta `rejected`.
    -   Um JSON com campos obrigatórios faltando (ex: sem `valorCondenacao`) para ver a resposta `incomplete`.

### 2. Teste da API (via FastAPI Docs)

Para testar o backend de forma isolada, use a documentação interativa da API.

1.  Acesse `http://localhost:8000/docs`.
2.  Encontre o endpoint `POST /verify`, expanda-o e clique em **"Try it out"**.
3.  Cole o JSON de teste no campo `Request body`.
4.  Clique em **"Execute"** e observe a resposta do servidor diretamente.

##  Estrutura do Projeto

-   `app/`: Contém a lógica principal da aplicação.
    -   `engine.py`: Orquestra a cadeia RAG, LLM e define o prompt do sistema.
    -   `schemas.py`: Define os modelos de dados Pydantic para entrada e saída.
    -   `ui.py`: Código da interface Streamlit.
    -   `rag.py`: Lógica para setup e recuperação do banco de vetores (ChromaDB).
    -   `policies.txt`: Arquivo de texto com as políticas de negócio.
-   `Dockerfile.api`: Dockerfile para o serviço da API (FastAPI).
-   `Dockerfile.frontend`: Dockerfile para o serviço do Frontend (Streamlit).
-   `docker-compose.yml`: Configuração para ambiente de produção (com Nginx e Certbot).
-   `docker-compose.local.yml`: Configuração para ambiente de desenvolvimento local.
-   `.env`: Arquivo para variáveis de ambiente (não versionado).

## Autor

Projeto desenvolvido por **Albert Vinicius**.