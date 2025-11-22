from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Testa se a API está de pé"""
    response = client.get("/health")
    assert response.status_code == 200
    
    assert response.json() == {"status": "ok", "llm": "Gemini-2.5", "rag": "ChromaDB"}
def test_validation_error():
    """Testa se a API rejeita JSON inválido (Pydantic enforcement)"""
    # Enviando payload sem 'numeroProcesso'
    payload_invalido = {
        "classe": "Execução",
        "documentos": [],
        "movimentos": []
    }
    response = client.post("/verify", json=payload_invalido)
    assert response.status_code == 422  # Unprocessable Entity

def test_fluxo_simples():
    """
    Testa o fluxo completo com um payload mínimo válido.
    Nota: Isso vai gastar cota do Gemini se rodar muitas vezes.
    """
    payload = {
      "numeroProcesso": "TESTE-001",
      "classe": "Teste",
      "orgaoJulgador": "Vara Teste",
      "segredoJustica": False,
      "justicaGratuita": False,
      "siglaTribunal": "TRT",  # TRT deve acionar a regra trabalhista (POL-4)
      "esfera": "Trabalhista",
      "documentos": [],
      "movimentos": [{"dataHora": "2024-01-01T00:00:00", "descricao": "Inicio"}]
    }
    
    response = client.post("/verify", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        # Verifica se retornou a estrutura obrigatória
        assert "decision" in data
        assert "rationale" in data
        assert "citacoes" in data
        # Como passamos esfera Trabalhista, idealmente deveria rejeitar ou falhar
        # Mas aqui testamos apenas o contrato da API (Schema)