import streamlit as st
import pandas as pd

st.set_page_config(page_title="Transformação de Features", page_icon="🛠️", layout="wide")

st.header("🛠️ Fase 3: Transformação e Feature Engineering")
st.write("Criação de novas variáveis para enriquecer a inteligência estatística.")

st.info("""
A base do INEP vem repleta de códigos (ex: Q006 = 'C', TP_SEXO = 'M'). 
O módulo de transformação mapeia esses códigos para textos legíveis e cria métricas consolidadas, como a **Média Geral**, essencial para nossos testes de correlação.
""")

st.subheader("1. Geração da Média Geral")
st.code("""
# Consolidando as 5 notas em um único KPI de performance
provas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
df['MEDIA_GERAL'] = df[provas].mean(axis=1)
""", language="python")

st.markdown("---")
st.subheader("2. Normalização de Variáveis Categóricas ")
st.write("Visualização de como as colunas `_LABEL` são construídas no backend:")

df_exemplo = pd.DataFrame({
    'Coluna Original (INEP)': ['Q006', 'TP_COR_RACA', 'TP_ESCOLA', 'Q001'],
    'Dado Bruto': ["'C'", "3", "2", "'E'"],
    'Transformação': ['➔', '➔', '➔', '➔'],
    'Coluna Criada (Pipeline)': ['Q006_LABEL', 'TP_COR_RACA_LABEL', 'TP_ESCOLA_LABEL', 'Q001_LABEL'],
    'Dado Transformado': ["'De R$ 1.320,01 a R$ 1.980,00'", "'Parda'", "'Pública'", "'Ensino Médio Completo'"]
})

st.dataframe(df_exemplo, use_container_width=True, hide_index=True)

st.write("#### Benefício Prático")
st.write("""
Ao fazer essa normalização no **momento do carregamento (Data Loader)**, nossos scripts de análise gráfica (Plotly) e de modelagem não precisam fazer traduções pesadas. O gráfico já recebe a string pronta, o que agiliza a renderização na interface.
""")