import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import carregar_dados_projeto

st.set_page_config(page_title="Adensamento Domiciliar", page_icon="🏠", layout="wide")

df_pr, df_br, _ = carregar_dados_projeto()

if df_pr is not None and df_br is not None:
    st.header("16. Adensamento Domiciliar e Performance")
    st.write("O número de pessoas na residência afeta o desempenho? Análise do ambiente de estudo no Paraná.")

    st.subheader("Tendência: Nota Média por Número de Moradores")
    
    def preparar_tendencia(df, local):
        res = df.groupby('Q005', observed=True)['MEDIA_GERAL'].mean().reset_index()
        res['Local'] = local
        return res

    df_tendencia_pr = preparar_tendencia(df_pr, 'Paraná')
    df_tendencia_br = preparar_tendencia(df_br, 'Brasil (Excl. PR)')
    df_plot_line = pd.concat([df_tendencia_pr, df_tendencia_br])

    fig_line = px.line(
        df_plot_line, x='Q005', y='MEDIA_GERAL', color='Local',
        markers=True,
        title="Relação Direta: Moradores na Casa vs. Média Geral",
        labels={'Q005': 'Número de Moradores', 'MEDIA_GERAL': 'Nota Média'},
        color_discrete_map={'Paraná': '#1f77b4', 'Brasil (Excl. PR)': '#7f7f7f'}
    )
    fig_line.update_layout(height=450)
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")
    
    
    
    st.subheader("Performance por Tamanho de Família (PR)")
    
    ordem_grupos = ['1-2 (Pequena)', '3-4 (Média)', '5-6 (Grande)', '7+ (Numerosa)']
    res_grupos = df_pr.groupby('MORADORES_AGRUPADO', observed=True)['MEDIA_GERAL'].mean().reindex(ordem_grupos).reset_index()

    fig_bar = px.bar(
        res_grupos, x='MORADORES_AGRUPADO', y='MEDIA_GERAL',
        text_auto='.1f',
        title="Média Geral por Categoria de Adensamento no Paraná",
        labels={'MEDIA_GERAL': 'Média Geral', 'MORADORES_AGRUPADO': 'Tamanho da Família'},
        color='MEDIA_GERAL',
        color_continuous_scale='Blues_r'
    )
    fig_bar.update_layout(yaxis=dict(range=[400, 600]), height=450)
    st.plotly_chart(fig_bar, use_container_width=True)

    corr_pr = df_pr['Q005'].astype(float).corr(df_pr['MEDIA_GERAL'])
    
    st.info(f"""
    **Análise Técnica:**
    - A correlação de Pearson no Paraná é de **{corr_pr:.3f}**. 
    - O valor negativo confirma que o adensamento domiciliar atua como uma variável de pressão: quanto mais pessoas dividem o domicílio, menor tende a ser a nota média.
    - Isso reflete fatores como a dificuldade de encontrar um ambiente silencioso e a diluição de recursos tecnológicos por habitante.
    """)