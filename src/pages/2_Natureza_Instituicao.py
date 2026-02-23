import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import carregar_dados
from utils.dicionarios import mapa_escola

st.set_page_config(page_title="Escolas Públicas vs Privadas", page_icon="🏫", layout="wide")

df_brasil = carregar_dados()

if df_brasil is not None:
    df_parana = df_brasil[df_brasil['SG_UF_PROVA'] == 'PR'].copy()

    st.header("2. Natureza da Instituição: Paraná x Brasil")
    st.write("Qual a proporção de alunos de escolas públicas vs. privadas no Paraná em comparação ao cenário brasileiro?")
    
    st.markdown("---")
    
    st.info("❗ Muitos candidatos já concluíram o ensino médio em anos anteriores e marcam 'Não Respondeu'.")
    filtrar_declarados = st.checkbox("Ocultar 'Não Respondeu' (Calcular proporção real apenas entre Pública e Privada)", value=True)

    if filtrar_declarados:
        df_br_analise = df_brasil[df_brasil['TP_ESCOLA'].isin([2, 3])]
        df_pr_analise = df_parana[df_parana['TP_ESCOLA'].isin([2, 3])]
    else:
        df_br_analise = df_brasil
        df_pr_analise = df_parana

    prop_pr = df_pr_analise['TP_ESCOLA'].value_counts(normalize=True).rename(index=mapa_escola) * 100
    prop_br = df_br_analise['TP_ESCOLA'].value_counts(normalize=True).rename(index=mapa_escola) * 100

    df_plot_pr = prop_pr.reset_index()
    df_plot_pr.columns = ['Tipo de Escola', 'Porcentagem']
    
    df_plot_br = prop_br.reset_index()
    df_plot_br.columns = ['Tipo de Escola', 'Porcentagem']

    col1, col2 = st.columns(2)

    cores_mapa = {'Pública': '#1f77b4', 'Privada': '#ff7f0e', 'Não Respondeu': '#7f7f7f'}

    with col1:
        st.subheader("Paraná (PR)")
        fig_pr = px.pie(df_plot_pr, values='Porcentagem', names='Tipo de Escola', hole=0.4, color='Tipo de Escola', color_discrete_map=cores_mapa)
        fig_pr.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pr, use_container_width=True)

    with col2:
        st.subheader("Brasil Médio")
        fig_br = px.pie(df_plot_br, values='Porcentagem', names='Tipo de Escola', hole=0.4, color='Tipo de Escola', color_discrete_map=cores_mapa)
        fig_br.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_br, use_container_width=True)
        
    
    st.markdown("---")
    st.subheader("Tabela Detalhada:")

    abs_pr = df_pr_analise['TP_ESCOLA'].value_counts().rename(index=mapa_escola)
    abs_br = df_br_analise['TP_ESCOLA'].value_counts().rename(index=mapa_escola)

    df_tabela = pd.DataFrame({
        'Paraná (Total)': abs_pr,
        'Paraná (%)': prop_pr,
        'Brasil (Total)': abs_br,
        'Brasil (%)': prop_br
    }).fillna(0) 
    
    df_tabela['Paraná (%)'] = df_tabela['Paraná (%)'].round(2)
    df_tabela['Brasil (%)'] = df_tabela['Brasil (%)'].round(2)
    
    df_tabela['Paraná (Total)'] = df_tabela['Paraná (Total)'].astype(int)
    df_tabela['Brasil (Total)'] = df_tabela['Brasil (Total)'].astype(int)

    st.dataframe(df_tabela, use_container_width=True)