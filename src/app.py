import streamlit as st
from utils.data_loader import carregar_dados_projeto

# Configuração da página para o tema Dark/Moderno
st.set_page_config(
    page_title="Dashboard ENEM 2023 - PR", 
    page_icon="📊", 
    layout="wide"
)

# Estilização CSS para métricas e visual
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #1f77b4; }
    .highlight { color: #ff4b4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Título Principal com Identificação Acadêmica
st.title("📊 Análise de Microdados: ENEM 2023")
st.subheader("Estudo de Caso: Eficiência Educacional e Disparidades no Paraná")

# Cabeçalho de Autoria (Baseado no seu documento UNISO)
col_auth, col_inst = st.columns([2, 1])
with col_auth:
    st.markdown(f"""
    **Autores:** Victor Hugo Aló e Guilherme Albuquerque Zaparolli   
    **Disciplina:** Ciência de Dados e Inteligência Artificial 
    **Instituição:** Universidade de Sorocaba (UNISO) 
    """)
with col_inst:
    st.image("https://portal.inep.gov.br/image/layout_set_logo?img_id=11301", width=180)

st.divider()

# --- SEÇÃO 1: FLASH INSIGHTS (DADOS REAIS DO SEU ARTIGO) ---
st.write("### ⚡ Flash Insights: O Cenário Paranaense")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Superioridade em Matemática", "553,2 pts", "+20,2 vs Brasil")
    st.caption("PR supera a média nacional em todas as áreas básicas.")

with c2:
    st.metric("Eficiência de Mitigação", "40,38 pts", "Superior à média")
    st.caption("Capacidade do estado em amortecer o impacto da pobreza.")

with c3:
    st.metric("Taxa de Abstenção", "31,07%", "Eficiência de 31,92% (BR)")
    st.caption("O Paraná demonstrou maior compromisso que a média nacional.")

with c4:
    st.metric("P-Valor (Escolas Federais)", "3,93e-97", "Significância Total")
    st.caption("Validação estatística da superioridade do ensino técnico/federal.")

st.divider()

# --- SEÇÃO 2: ARQUITETURA DO PIPELINE (CONFORME SUA IMAGEM) ---
st.write("### ⚙️ Arquitetura do Pipeline de Dados")


# Descrição técnica baseada na imagem e metodologia
cols_arq = st.columns(4)
with cols_arq[0]:
    st.markdown("**Formato de Dados**")
    st.code("Apache Parquet")
    st.caption("Armazenamento colunar otimizado para performance.")
with cols_arq[1]:
    st.markdown("**Limpeza**")
    st.code("Modular (SRP)")
    st.caption("Pipeline dividido em Sanidade, Transformação e Otimização.")
with cols_arq[2]:
    st.markdown("**Motor Estatístico**")
    st.code("SciPy / Pearson")
    st.caption("Cálculo de correlação $R$ e significância (p-valor).")
with cols_arq[3]:
    st.markdown("**Base de Dados**")
    st.code("ENEM 2023")
    st.caption("Microdados oficiais fornecidos pelo INEP.")

st.divider()

# --- SEÇÃO 3: ROTEIRO DA APRESENTAÇÃO ---
st.write("### 🗺️ Roteiro da Investigação")
tab1, tab2, tab3 = st.tabs([
    "📍 Eixo 1: Perfil e Fluxo", 
    "📈 Eixo 2: Desempenho e Benchmarking", 
    "⚖️ Eixo 3: Impacto Socioeconômico"
])

with tab1:
    st.markdown(f"""
    **Objetivo:** Caracterizar o público paranaense e o engajamento no exame.
    - **Demografia:** Predomínio feminino e análise de raça/cor regional.
    - **Engajamento:** 15,58% de treineiros contra 15,76% na média nacional.
    - **Abstenção:** Análise crítica de polos como Palmas (44% de ausentes).
    """)

with tab2:
    st.markdown(f"""
    **Objetivo:** Analisar a competitividade acadêmica e pontos focais de ensino.
    - **Liderança Regional:** Curitiba (Matemática), Londrina (Humanas) e Maringá (Redação).
    - **Gargalo da Redação:** Defasagem de -7,56 pontos na Competência 4 (Intervenção).
    - **Consistência:** PR é 10,79% mais estável na norma culta que o restante do país.
    """)

with tab3:
    st.markdown(f"""
    **Objetivo:** Quantificar o impacto das variáveis estocásticas.
    - **Infraestrutura Digital:** Correlação de $R = 0,344$ entre posse de PC e nota de Matemática.
    - **Exclusão Digital:** Gap de até 64,6 pontos em centros urbanos como Curitiba.
    - **Capital Cultural:** A influência crítica da escolaridade parental e adensamento domiciliar.
    """)

# Rodapé Final
st.markdown("---")
st.caption("Projeto desenvolvido em Python utilizando Pandas, Plotly e Streamlit. Sorocaba/SP, 2026.")