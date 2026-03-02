import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import carregar_dados_projeto

st.set_page_config(page_title="Herança Educacional", page_icon="🎓", layout="wide")

df_pr, _, _ = carregar_dados_projeto()

if df_pr is not None:
    st.header("15. Herança Educacional e Alta Performance")
    st.write("Qual a probabilidade de um aluno atingir média > 700 baseada na instrução dos pais?")

    df_pr['ALTA_PERFORMANCE'] = (df_pr['MEDIA_GERAL'] >= 700).astype(int)

    def calcular_probabilidade(df, col_label):
        prob = df.groupby(col_label, observed=True)['ALTA_PERFORMANCE'].mean().reset_index()
        prob['Probabilidade (%)'] = prob['ALTA_PERFORMANCE'] * 100
        prob.columns = ['Escolaridade', 'Média_Prob', 'Probabilidade (%)']
        return prob

    prob_pai = calcular_probabilidade(df_pr, 'Q001_LABEL')
    prob_mae = calcular_probabilidade(df_pr, 'Q002_LABEL')

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
    
    heatmap_raw = df_pr.pivot_table(
        index='Q002_LABEL', 
        columns='Q001_LABEL', 
        values='ALTA_PERFORMANCE', 
        aggfunc='mean',
        observed=True
    ) * 100
    
    fig_heat = px.imshow(
        heatmap_raw,
        labels=dict(x="Escolaridade do Pai", y="Escolaridade da Mãe", color="Probabilidade (%)"),
        color_continuous_scale='Viridis',
        aspect="auto",
        text_auto=".1f"
    )
    st.plotly_chart(fig_heat, use_container_width=True)

    st.info("""
    **Análise Técnica:**
    - A probabilidade é calculada como $P(Performance \geq 700 | Escolaridade)$.
    - O Heatmap revela o efeito sinérgico: as maiores probabilidades concentram-se no quadrante onde ambos os pais possuem nível superior ou pós-graduação.
    - Este fenômeno é frequentemente discutido na sociologia da educação como 'Capital Cultural', onde o ambiente instrucional familiar potencializa o desempenho acadêmico.
    """)