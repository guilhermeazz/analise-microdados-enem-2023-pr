import streamlit as st

st.set_page_config(
    page_title="Análise ENEM 2023",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Análise dos Microdados do ENEM 2023")
st.markdown("""
Bem-vindo ao painel de análise socioeconômica e de desempenho do ENEM 2023.

Neste projeto, investigamos o perfil dos candidatos do estado do **Paraná** e o comparamos com a média nacional, respondendo a 20 perguntas de negócio através da análise exploratória de dados.

**Utilize o menu lateral para navegar entre as análises e perguntas.**
""")