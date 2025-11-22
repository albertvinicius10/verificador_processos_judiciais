from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime
 
class Documento(BaseModel):
    id: str
    dataHoraJuntada: Optional[datetime] = None
    nome: str
    texto: str

class Movimento(BaseModel):
    dataHora: datetime
    descricao: str

class Honorarios(BaseModel):
    contratuais: Optional[float] = 0.0
    periciais: Optional[float] = 0.0
    sucumbenciais: Optional[float] = 0.0

class ProcessoInput(BaseModel):
    numeroProcesso: str
    classe: str
    orgaoJulgador: str
    ultimaDistribuicao: Optional[datetime] = None
    assunto: Optional[str] = None
    segredoJustica: bool
    justicaGratuita: bool
    siglaTribunal: str
    esfera: str
    valorCausa: Optional[float] = 0.0
    valorCondenacao: Optional[float] = None
    documentos: List[Documento]
    movimentos: List[Movimento]
    honorarios: Optional[Honorarios] = None
 
class AnaliseJuridicaOutput(BaseModel):
    decision: Literal["approved", "rejected", "incomplete"] = Field(..., description="Decisão final baseada nas políticas.")
    rationale: str = Field(..., description="Justificativa clara para a decisão.")
    citacoes: List[str] = Field(..., description="Lista de IDs das políticas aplicadas (ex: POL-1, POL-3).")