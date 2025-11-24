import streamlit as st
import requests
import json

st.set_page_config(page_title="JusCash AI Verifier", page_icon="⚖️", layout="wide")

st.title("⚖️ JusCash - Verificador de Processos Judiciais")
st.markdown("""
Esta ferramenta utiliza **IA Generativa** e **RAG** para analisar a elegibilidade de compra de processos judiciais.
""")

API_URL = "http://api:8000/verify"

default_json = """{
  "numeroProcesso": "0004587-00.2021.4.05.8100",
  "classe": "Cumprimento de Sentença contra a Fazenda Pública",
  "orgaoJulgador": "1ª VARA FEDERAL SOBRAL/CE",
  "ultimaDistribuicao": "2024-11-18T23:15:44.1302",
  "valorCausa": 67592,
  "assunto": "Rural (Art. 48/51)",
  "segredoJustica": false,
  "justicaGratuita": true,
  "siglaTribunal": "TRF5",
  "esfera": "Federal",
  "valorCondenacao": 67592,
  "documentos": [
    {
      "id": "DOC-1",
      "dataHoraJuntada": "2023-09-10T10:00:00",
      "nome": "Certidão de Trânsito em Julgado",
      "texto": "Certifico que a sentença transitou em julgado."
    }
  ],
  "movimentos": [
    {
      "dataHora": "2024-01-20T11:22:33",
      "descricao": "Iniciado cumprimento definitivo de sentença."
    }
  ]
}"""

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Dados do Processo (JSON)")
    json_input = st.text_area("Cole o JSON do processo aqui:", value=default_json, height=600)
    analyze_btn = st.button("🔍 Analisar Processo", type="primary")

with col2:
    st.subheader("📊 Resultado da Análise")
    
    if analyze_btn:
        try:
            payload = json.loads(json_input)
            
            with st.spinner("Consultando o Oráculo Jurídico (Gemini + RAG)..."):
                response = requests.post(API_URL, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                decision = result.get("decision")
                
                if decision == "approved":
                    st.success(f"## ✅ APROVADO")
                elif decision == "rejected":
                    st.error(f"## ❌ REJEITADO")
                else:
                    st.warning(f"## ⚠️ INCOMPLETO")
                
                st.markdown("### 📝 Justificativa")
                st.info(result.get("rationale"))
                
                st.markdown("### 📜 Políticas Citadas")
                tags = result.get("citacoes", [])
                st.write(" ".join([f"`{tag}`" for tag in tags]))
                
                with st.expander("Ver JSON de Resposta Completo"):
                    st.json(result)
            else:
                st.error(f"Erro na API: {response.status_code}")
                st.write(response.text)
                
        except json.JSONDecodeError:
            st.error("O texto fornecido não é um JSON válido.")
        except requests.exceptions.ConnectionError:
            st.error("Não foi possível conectar à API. Verifique se o container Docker está rodando.")