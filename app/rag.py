import os
import shutil
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
 
CHROMA_PATH = "/app/chroma_db"

def get_embedding_function():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def setup_vector_db():
    """Lê o arquivo de políticas e popula o ChromaDB."""
    embedding_function = get_embedding_function()
    
    print("--- Verificando Vector DB ---")
    if os.path.exists(CHROMA_PATH):
        print("--- Limpando banco vetorial antigo... ---")
        for filename in os.listdir(CHROMA_PATH):
            file_path = os.path.join(CHROMA_PATH, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Aviso: Não foi possível deletar {file_path}. Motivo: {e}")

    print("--- Criando e populando Vector DB (Embeddings Locais) ---")
    try:
        with open("app/policies.txt", "r") as f:
            text = f.read()
        
        lines = [line for line in text.split('\n') if line.strip()]
        docs = [Document(page_content=line, metadata={"source": "policies.txt"}) for line in lines]
        
        Chroma.from_documents(
            documents=docs,
            embedding=embedding_function,
            persist_directory=CHROMA_PATH
        )
        print("--- Vector DB populado com sucesso ---")
    except Exception as e:
        print(f"Erro crítico ao popular Vector DB: {e}")

def get_retriever():
    embedding_function = get_embedding_function()
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH, 
        embedding_function=embedding_function
    )
    return vectorstore.as_retriever(search_kwargs={"k": 8})