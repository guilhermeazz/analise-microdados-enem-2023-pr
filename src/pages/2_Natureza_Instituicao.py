import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import carregar_dados_projeto

st.set_page_config(page_title="Escolas Públicas vs Privadas", page_icon="🏫", layout="wide")

df_pr, df_br, _ = carregar_dados_projeto()

if df_pr is not None and df_br is not None:

    st.header("2. Natureza da Instituição: Paraná x Brasil")
    st.write("Qual a proporção de alunos de escolas públicas vs. privadas no Paraná em comparação ao restante do Brasil?")
    
    st.markdown("---")
    
    st.info("💡 Nota: Candidatos que já concluíram o ensino médio ou são treineiros costumam aparecer como 'Não Respondeu'.")
    
    filtrar_declarados = st.checkbox("Focar apenas em candidatos de escolas declaradas (Pública vs Privada)", value=True)

    if filtrar_declarados:
        df_pr_analise = df_pr[df_pr['TP_ESCOLA_LABEL'].isin(['Pública', 'Privada'])]
        df_br_analise = df_br[df_br['TP_ESCOLA_LABEL'].isin(['Pública', 'Privada'])]
    else:
        df_pr_analise = df_pr
        df_br_analise = df_br

    def obter_proporcoes(df):
        prop = df['TP_ESCOLA_LABEL'].value_counts(normalize=True) * 100
        return prop.reset_index().rename(columns={'TP_ESCOLA_LABEL': 'Tipo de Escola', 'proportion': 'Porcentagem'})

    df_plot_pr = obter_proporcoes(df_pr_analise)
    df_plot_br = obter_proporcoes(df_br_analise)

    cores_mapa = {'Pública': '#1f77b4', 'Privada': '#ff7f0e', 'Não Respondeu': '#7f7f7f'}

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Paraná (PR)")
        fig_pr = px.pie(
            df_plot_pr, values='Porcentagem', names='Tipo de Escola', 
            hole=0.4, color='Tipo de Escola', color_discrete_map=cores_mapa
        )
        fig_pr.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pr, use_container_width=True)

    with col2:
        st.subheader("Brasil (Excl. PR)")
        fig_br = px.pie(
            df_plot_br, values='Porcentagem', names='Tipo de Escola', 
            hole=0.4, color='Tipo de Escola', color_discrete_map=cores_mapa
        )
        fig_br.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_br, use_container_width=True)
        
    st.markdown("---")
    st.subheader("Comparativo Quantitativo")

    abs_pr = df_pr_analise['TP_ESCOLA_LABEL'].value_counts()
    abs_br = df_br_analise['TP_ESCOLA_LABEL'].value_counts()
    
    pct_pr = (abs_pr / abs_pr.sum() * 100).round(2)
    pct_br = (abs_br / abs_br.sum() * 100).round(2)

    df_tabela = pd.DataFrame({
        'Paraná (Inscritos)': abs_pr,
        'Paraná (%)': pct_pr,
        'Brasil (Inscritos)': abs_br,
        'Brasil (%)': pct_br
    }).fillna(0)

    st.dataframe(df_tabela.style.format({
        'Paraná (%)': '{:.2f}%',
        'Brasil (%)': '{:.2f}%',
        'Paraná (Inscritos)': '{:,}',
        'Brasil (Inscritos)': '{:,}'
    }), use_container_width=True)

    st.caption("Fonte: Microdados ENEM 2023 | Processamento Modular Próprio")