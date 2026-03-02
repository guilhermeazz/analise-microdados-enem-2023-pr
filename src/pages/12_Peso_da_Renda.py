import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import carregar_dados_projeto

st.set_page_config(page_title="Peso da Renda", page_icon="💰", layout="wide")

df_pr, df_br, _ = carregar_dados_projeto()

if df_pr is not None and df_br is not None:
    ordem_renda = sorted(df_pr['Q006'].unique())
    mapa_numerico_renda = {letra: i+1 for i, letra in enumerate(ordem_renda)}
    
    df_pr['RENDA_NUMERICA'] = df_pr['Q006'].map(mapa_numerico_renda)
    df_br['RENDA_NUMERICA'] = df_br['Q006'].map(mapa_numerico_renda)

    st.header("12. O Peso da Renda na Redação")
    st.write("Análise de correlação: Quanto a renda familiar influencia a nota final da Redação?")

    corr_pr = df_pr['RENDA_NUMERICA'].corr(df_pr['NU_NOTA_REDACAO'])
    corr_br = df_br['RENDA_NUMERICA'].corr(df_br['NU_NOTA_REDACAO'])

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Correlação no Paraná ($R$)", f"{corr_pr:.3f}")
    with c2:
        st.metric("Correlação no Brasil ($R$)", f"{corr_br:.3f}", delta=f"{corr_pr - corr_br:.3f}")

    st.markdown("---")

    st.subheader("Progressão da Nota Média por Faixa de Renda")
    
    def preparar_tendencia(df, local):
        res = df.groupby(['Q006', 'Q006_LABEL'], observed=True)['NU_NOTA_REDACAO'].mean().reset_index()
        res['Local'] = local
        return res

    tendencia_pr = preparar_tendencia(df_pr, 'Paraná')
    tendencia_br = preparar_tendencia(df_br, 'Brasil (Excl. PR)')
    df_plot = pd.concat([tendencia_pr, tendencia_br])

    fig_linha = px.line(
        df_plot, x='Q006', y='NU_NOTA_REDACAO', color='Local',
        markers=True,
        title="Nota Média da Redação por Classe Social (A -> Q)",
        labels={'NU_NOTA_REDACAO': 'Nota Média', 'Q006': 'Faixa de Renda', 'Q006_LABEL': 'Descrição'},
        color_discrete_map={'Paraná': '#1f77b4', 'Brasil (Excl. PR)': '#7f7f7f'},
        hover_data=['Q006_LABEL']
    )
    st.plotly_chart(fig_linha, use_container_width=True)

    st.markdown("---")
    
    

    st.subheader("Distribuição Detalhada (PR)")
    fig_box = px.box(
        df_pr, x='Q006_LABEL', y='NU_NOTA_REDACAO',
        color='Q006_LABEL',
        title="Dispersão das Notas de Redação por Faixa de Renda no Paraná",
        category_orders={"Q006_LABEL": [df_pr[df_pr['Q006'] == l]['Q006_LABEL'].iloc[0] for l in ordem_renda]},
        labels={'Q006_LABEL': 'Descrição da Renda', 'NU_NOTA_REDACAO': 'Nota Redação'},
        points=False
    )
    st.plotly_chart(fig_box, use_container_width=True)

    st.info(f"""
    **Análise Técnica:**
    - O coeficiente de correlação de Pearson **$R = {corr_pr:.3f}$** no Paraná indica uma relação positiva moderada. 
    - A inclinação da reta de tendência sugere que o capital financeiro familiar é um preditor relevante para o desempenho em produção textual.
    - Observar o "achatamento" ou "alongamento" dos boxplots ajuda a identificar em quais faixas de renda a desigualdade interna é maior.
    """)