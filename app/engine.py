import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from app.schemas import ProcessoInput, AnaliseJuridicaOutput
from app.rag import get_retriever

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_analysis_chain():
    # Configura Gemini. Temperature 0 para ser determinístico (exigência jurídica)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    structured_llm = llm.with_structured_output(AnaliseJuridicaOutput)
    retriever = get_retriever()
 
    system_prompt = """Você é um analista jurídico sênior de uma fintech (JusCash).
    Sua tarefa é validar a elegibilidade de processos judiciais.
    
    Use ESTRITAMENTE as seguintes Políticas/Regras recuperadas da base de conhecimento:
    
    {context}
    
    Instruções de Saída:
    1. Se faltar documento essencial (ex: certidão de trânsito em julgado) -> decision: "incomplete".
    2. Se violar regras proibitivas (ex: valor baixo, trabalhista, óbito) -> decision: "rejected".
    3. Se cumprir os requisitos positivos -> decision: "approved".
    4. Sempre cite os IDs das políticas (ex: POL-1) no campo 'citacoes'.
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "Analise o seguinte processo JSON:\n\n{process_data}")
    ])
 
    chain = (
        {
            "context": retriever | format_docs, 
            "process_data": RunnablePassthrough()
        }
        | prompt
        | structured_llm
    )
    
    return chain

def analyze_process(processo: ProcessoInput) -> AnaliseJuridicaOutput:
    chain = get_analysis_chain()
    process_json = processo.model_dump_json()
    result = chain.invoke(process_json)
    return result