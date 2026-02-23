import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import carregar_dados
from utils.dicionarios import mapa_escolaridade_pais

st.set_page_config(page_title="Herança Educacional", page_icon="🎓", layout="wide")

df_brasil = carregar_dados()

if df_brasil is not None:
    provas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    df_brasil['MEDIA_GERAL'] = df_brasil[provas].mean(axis=1)
    
    df_pr = df_brasil[df_brasil['SG_UF_PROVA'] == 'PR'].dropna(subset=['Q001', 'Q002', 'MEDIA_GERAL']).copy()

    st.header("15. Herança Educacional e Alta Performance")
    st.write("Qual a probabilidade de um aluno atingir média > 700 baseada na instrução dos pais?")

    df_pr['ALTA_PERFORMANCE'] = (df_pr['MEDIA_GERAL'] >= 700).astype(int)

    def calcular_probabilidade(df, coluna):
        prob = df.groupby(coluna)['ALTA_PERFORMANCE'].mean().reset_index()
        prob['Probabilidade (%)'] = prob['ALTA_PERFORMANCE'] * 100
        prob['Escolaridade'] = prob[coluna].map(mapa_escolaridade_pais)
        return prob.sort_values(coluna)

    prob_pai = calcular_probabilidade(df_pr, 'Q001')
    prob_mae = calcular_probabilidade(df_pr, 'Q002')

    st.subheader("Probabilidade de Média > 700")
    
    tab1, tab2 = st.tabs(["Escolaridade da Mãe", "Escolaridade do Pai"])
    
    with tab1:
        fig_mae = px.bar(
            prob_mae, x='Escolaridade', y='Probabilidade (%)',
            text_auto='.1f',
            title="Chance de Alta Performance vs. Escolaridade Materna",
            color='Probabilidade (%)',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig_mae, use_container_width=True)

    with tab2:
        fig_pai = px.bar(
            prob_pai, x='Escolaridade', y='Probabilidade (%)',
            text_auto='.1f',
            title="Chance de Alta Performance vs. Escolaridade Paterna",
            color='Probabilidade (%)',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig_pai, use_container_width=True)

    st.markdown("---")
    st.subheader("Cruzamento: O Efeito Combinado")
    
    heatmap_data = df_pr.pivot_table(
        index='Q002', columns='Q001', values='ALTA_PERFORMANCE', aggfunc='mean'
    ) * 100
    
    heatmap_data.index = [mapa_escolaridade_pais.get(i) for i in heatmap_data.index]
    heatmap_data.columns = [mapa_escolaridade_pais.get(c) for c in heatmap_data.columns]

    fig_heat = px.imshow(
        heatmap_data,
        labels=dict(x="Escolaridade do Pai", y="Escolaridade da Mãe", color="Probabilidade (%)"),
        x=heatmap_data.columns,
        y=heatmap_data.index,
        color_continuous_scale='Viridis',
        aspect="auto"
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.info("""
    **Interpretação:** - As barras mostram o salto de probabilidade conforme o nível de instrução aumenta. 
    - No heatmap, as cores mais claras (amarelo/verde) indicam as combinações familiares onde é mais provável encontrar alunos de alta performance. 
    - Note se o 'gap' entre pais com pós-graduação e pais sem instrução é maior no caso da mãe ou do pai.
    """)