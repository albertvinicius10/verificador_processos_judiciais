from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.schemas import ProcessoInput, AnaliseJuridicaOutput
from app.engine import analyze_process
from app.rag import setup_vector_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("juscash_api")

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_vector_db()
    yield

app = FastAPI(
    title="JusCash AI Verifier (Gemini + RAG)",
    lifespan=lifespan
)

@app.get("/health")
def health_check():
    return {"status": "ok", "llm": "Gemini-2.5", "rag": "ChromaDB"}
@app.post("/verify", response_model=AnaliseJuridicaOutput)
def verify_endpoint(processo: ProcessoInput):
    logger.info(f"Processing: {processo.numeroProcesso}")
    result = analyze_process(processo)
    return result