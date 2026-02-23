import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import carregar_dados
from utils.dicionarios import mapa_renda

st.set_page_config(page_title="Peso da Renda", page_icon="💰", layout="wide")

df_brasil = carregar_dados()

if df_brasil is not None:
    df_analise = df_brasil.dropna(subset=['Q006', 'NU_NOTA_REDACAO']).copy()
    
    ordem_renda = sorted(df_analise['Q006'].unique())
    mapa_numerico_renda = {letra: i+1 for i, letra in enumerate(ordem_renda)}
    df_analise['RENDA_NUMERICA'] = df_analise['Q006'].map(mapa_numerico_renda)

    df_pr = df_analise[df_analise['SG_UF_PROVA'] == 'PR']
    df_br = df_analise[df_analise['SG_UF_PROVA'] != 'PR']

    st.header("12. O Peso da Renda na Redação")
    st.write("Análise de correlação: Quanto a renda familiar influencia a nota final da Redação?")

    corr_pr = df_pr['RENDA_NUMERICA'].corr(df_pr['NU_NOTA_REDACAO'])
    corr_br = df_br['RENDA_NUMERICA'].corr(df_br['NU_NOTA_REDACAO'])

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Correlação no Paraná (R)", f"{corr_pr:.3f}")
    with c2:
        st.metric("Correlação no Brasil (R)", f"{corr_br:.3f}", delta=f"{corr_pr - corr_br:.3f}")

    st.markdown("---")

    st.subheader("Progressão da Nota Média por Faixa de Renda")
    
    def preparar_tendencia(df, local):
        res = df.groupby('Q006')['NU_NOTA_REDACAO'].mean().reset_index()
        res['Local'] = local
        res['Renda_Desc'] = res['Q006'].map(mapa_renda)
        return res

    tendencia_pr = preparar_tendencia(df_pr, 'Paraná')
    tendencia_br = preparar_tendencia(df_br, 'Brasil')
    df_plot = pd.concat([tendencia_pr, tendencia_br])

    fig_linha = px.line(
        df_plot, x='Q006', y='NU_NOTA_REDACAO', color='Local',
        markers=True,
        title="Nota Média da Redação por Classe Social (A -> Q)",
        labels={'NU_NOTA_REDACAO': 'Nota Média', 'Q006': 'Faixa de Renda (A-Q)'},
        color_discrete_map={'Paraná': '#1f77b4', 'Brasil': '#7f7f7f'},
        hover_data=['Renda_Desc']
    )
    st.plotly_chart(fig_linha, use_container_width=True)

    st.markdown("---")

    st.subheader("Distribuição Detalhada (PR)")
    fig_box = px.box(
        df_pr, x='Q006', y='NU_NOTA_REDACAO',
        color='Q006',
        title="Dispersão das Notas de Redação por Faixa de Renda no Paraná",
        category_orders={"Q006": ordem_renda},
        labels={'Q006': 'Faixa de Renda'}
    )
    st.plotly_chart(fig_box, use_container_width=True)

    st.info(f"""
    **Análise Técnica:**
    - O coeficiente **R = {corr_pr:.3f}** indica uma correlação positiva moderada. 
    - Se a correlação do Paraná for **{'maior' if corr_pr > corr_br else 'menor'}** que a do Brasil, isso sugere que a renda familiar tem um peso **{'mais' if corr_pr > corr_br else 'menos'}** decisivo no desempenho dos alunos paranaenses do que na média nacional.
    """)