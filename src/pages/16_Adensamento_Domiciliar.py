import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import carregar_dados

st.set_page_config(page_title="Adensamento Domiciliar", page_icon="🏠", layout="wide")

df_brasil = carregar_dados()

if df_brasil is not None:
    provas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    df_brasil['MEDIA_GERAL'] = df_brasil[provas].mean(axis=1)
    
    df_brasil['Q005'] = pd.to_numeric(df_brasil['Q005'], errors='coerce')
    df_analise = df_brasil.dropna(subset=['Q005', 'MEDIA_GERAL']).copy()

    def agrupar_moradores(n):
        if n <= 2: return '1-2 (Pequena)'
        if n <= 4: return '3-4 (Média)'
        if n <= 6: return '5-6 (Grande)'
        return '7+ (Numerosa)'

    df_analise['Tamanho_Familia'] = df_analise['Q005'].apply(agrupar_moradores)
    
    df_pr = df_analise[df_analise['SG_UF_PROVA'] == 'PR']
    df_br = df_analise[df_analise['SG_UF_PROVA'] != 'PR']

    st.header("16. Adensamento Domiciliar e Performance")
    st.write("O número de pessoas na residência afeta o desempenho? Análise do ambiente de estudo no Paraná.")

    st.subheader("Tendência: Nota Média por Número de Moradores")
    
    df_tendencia_pr = df_pr.groupby('Q005')['MEDIA_GERAL'].mean().reset_index()
    df_tendencia_br = df_br.groupby('Q005')['MEDIA_GERAL'].mean().reset_index()
    
    df_tendencia_pr['Local'] = 'Paraná'
    df_tendencia_br['Local'] = 'Brasil'
    df_plot_line = pd.concat([df_tendencia_pr, df_tendencia_br])

    fig_line = px.line(
        df_plot_line, x='Q005', y='MEDIA_GERAL', color='Local',
        markers=True,
        title="Relação Direta: Moradores na Casa vs. Média Geral",
        labels={'Q005': 'Número de Moradores', 'MEDIA_GERAL': 'Nota Média'},
        color_discrete_map={'Paraná': '#1f77b4', 'Brasil': '#7f7f7f'}
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("---")
    st.subheader("Performance por Tamanho de Família (PR)")
    
    ordem_grupos = ['1-2 (Pequena)', '3-4 (Média)', '5-6 (Grande)', '7+ (Numerosa)']
    res_grupos = df_pr.groupby('Tamanho_Familia')['MEDIA_GERAL'].mean().reindex(ordem_grupos).reset_index()

    fig_bar = px.bar(
        res_grupos, x='Tamanho_Familia', y='MEDIA_GERAL',
        text_auto='.1f',
        title="Média Geral por Categoria de Adensamento",
        color='MEDIA_GERAL',
        color_continuous_scale='Blues_r'
    )
    fig_bar.update_layout(yaxis=dict(range=[400, 600]))
    st.plotly_chart(fig_bar, use_container_width=True)

    corr_pr = df_pr['Q005'].corr(df_pr['MEDIA_GERAL'])
    
    st.info(f"""
    **Análise Técnica:**
    - A correlação de Pearson no Paraná é de **{corr_pr:.3f}**. 
    - Um valor negativo indica que, à medida que o número de moradores aumenta, a nota média tende a diminuir.
    - Isso pode estar associado à falta de privacidade, maior ruído ambiental e menor divisão de recursos (como internet e computador) por habitante.
    """)