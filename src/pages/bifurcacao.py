import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Separação PR vs BR", page_icon="🔀", layout="wide")

st.header("🔀 Fase 4: Bifurcação Geográfica (Benchmarking)")
st.write("A lógica estatística por trás da comparação entre o Paraná e o restante do país.")



c1, c2 = st.columns([1.5, 1])

with c1:
    st.write("### O Erro Comum do Benchmarking")
    st.write("""
    Muitas análises comparam a "Média do Estado" com a "Média do Brasil". 
    No entanto, como o Brasil **inclui** os dados do Estado, a média nacional é "puxada" pela nota do próprio Estado, diluindo a diferença real.
    """)
    
    st.write("### A Nossa Metodologia")
    st.write("""
    Para que o Teste T de Student fosse válido, adotamos o isolamento exclusivo dos candidatos do Paraná. 
    Dividimos a base limpa em duas frentes estritamente independentes:
    """)
    
    st.code("""
    # 1. Isolando o Objeto de Estudo (Paraná)
    df_pr = df_total[df_total['SG_UF_PROVA'] == 'PR']
    
    # 2. Criando o Grupo de Controle (Brasil SEM o Paraná)
    df_br = df_total[df_total['SG_UF_PROVA'] != 'PR']
    """, language="python")

with c2:
    df_pie = pd.DataFrame({
        'Dataset': ['Paraná (df_pr)', 'Brasil Controle (df_br)'],
        'Proporção': [4.5, 95.5] 
    })
    
    fig_pie = px.pie(
        df_pie, values='Proporção', names='Dataset', 
        hole=0.4, title="Separação Final do Data Loader",
        color='Dataset',
        color_discrete_map={'Paraná (df_pr)': '#1f77b4', 'Brasil Controle (df_br)': '#7f7f7f'}
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.info("""
**Impacto na Análise:** Graças a essa separação, quando dizemos que o Paraná supera a média em Matemática, estamos afirmando matematicamente que a amostra `df_pr` é superior à amostra `df_br`, sem sobreposição de indivíduos. Isso garante a validade do p-valor nos nossos testes de hipótese.
""")