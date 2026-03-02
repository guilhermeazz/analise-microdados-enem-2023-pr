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
    **Autores:** Victor Hugo Aló e Guilherme Albuquerque Zaparolli [cite: 4, 5]  
    **Disciplina:** Ciência de Dados e Inteligência Artificial [cite: 3]  
    **Instituição:** Universidade de Sorocaba (UNISO) [cite: 1]
    """)
with col_inst:
    st.image("https://portal.inep.gov.br/image/layout_set_logo?img_id=11301", width=180)

st.divider()

# --- SEÇÃO 1: FLASH INSIGHTS (DADOS REAIS DO SEU ARTIGO) ---
st.write("### ⚡ Flash Insights: O Cenário Paranaense")
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Superioridade em Matemática", "553,2 pts", "+20,2 vs Brasil")
    st.caption("PR supera a média nacional em todas as áreas básicas[cite: 88, 90].")

with c2:
    st.metric("Eficiência de Mitigação", "40,38 pts", "Superior à média")
    st.caption("Capacidade do estado em amortecer o impacto da pobreza[cite: 37, 115].")

with c3:
    st.metric("Taxa de Abstenção", "31,07%", "Eficiência de 31,92% (BR)")
    st.caption("O Paraná demonstrou maior compromisso que a média nacional[cite: 84].")

with c4:
    st.metric("P-Valor (Escolas Federais)", "3,93e-97", "Significância Total")
    st.caption("Validação estatística da superioridade do ensino técnico/federal[cite: 114].")

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
    st.caption("Pipeline dividido em Sanidade, Transformação e Otimização[cite: 55].")
with cols_arq[2]:
    st.markdown("**Motor Estatístico**")
    st.code("SciPy / Pearson")
    st.caption("Cálculo de correlação $R$ e significância (p-valor)[cite: 58, 59].")
with cols_arq[3]:
    st.markdown("**Base de Dados**")
    st.code("ENEM 2023")
    st.caption("Microdados oficiais fornecidos pelo INEP[cite: 53].")

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
    **Objetivo:** Caracterizar o público paranaense e o engajamento no exame[cite: 63].
    - **Demografia:** Predomínio feminino e análise de raça/cor regional[cite: 67, 68].
    - **Engajamento:** 15,58% de treineiros contra 15,76% na média nacional[cite: 81].
    - **Abstenção:** Análise crítica de polos como Palmas (44% de ausentes)[cite: 85].
    """)

with tab2:
    st.markdown(f"""
    **Objetivo:** Analisar a competitividade acadêmica e pontos focais de ensino[cite: 88].
    - **Liderança Regional:** Curitiba (Matemática), Londrina (Humanas) e Maringá (Redação)[cite: 91, 92].
    - **Gargalo da Redação:** Defasagem de -7,56 pontos na Competência 4 (Intervenção)[cite: 96].
    - **Consistência:** PR é 10,79% mais estável na norma culta que o restante do país[cite: 97].
    """)

with tab3:
    st.markdown(f"""
    **Objetivo:** Quantificar o impacto das variáveis estocásticas[cite: 41, 49].
    - **Infraestrutura Digital:** Correlação de $R = 0,344$ entre posse de PC e nota de Matemática[cite: 103].
    - **Exclusão Digital:** Gap de até 64,6 pontos em centros urbanos como Curitiba[cite: 105].
    - **Capital Cultural:** A influência crítica da escolaridade parental e adensamento domiciliar[cite: 107, 111].
    """)

# Rodapé Final
st.markdown("---")
st.caption("Projeto desenvolvido em Python utilizando Pandas, Plotly e Streamlit[cite: 56]. Sorocaba/SP, 2026[cite: 7, 8].")