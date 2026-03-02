import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import carregar_dados_projeto

st.set_page_config(page_title="Abismo Público-Privado", page_icon="⚖️", layout="wide")

df_pr, _, _ = carregar_dados_projeto()

if df_pr is not None:
    df_analise = df_pr[df_pr['TP_ESCOLA_LABEL'].isin(['Pública', 'Privada'])].copy()

    st.header("20. O Abismo Público-Privado no Paraná")
    st.markdown("#### *Análise de distribuição: Onde as notas das duas redes se cruzam?*")

    

    fig_abismo = px.box(
        df_analise, 
        x='TP_ESCOLA_LABEL', 
        y='MEDIA_GERAL', 
        color='TP_ESCOLA_LABEL',
        points="outliers", 
        notched=True,      
        title="Distribuição das Notas Médias por Rede de Ensino no PR",
        labels={'MEDIA_GERAL': 'Nota Média Geral', 'TP_ESCOLA_LABEL': 'Rede de Ensino'},
        color_discrete_map={'Pública': '#ef553b', 'Privada': '#636efa'}
    )

    media_privada = df_analise[df_analise['TP_ESCOLA_LABEL'] == 'Privada']['MEDIA_GERAL'].mean()
    
    fig_abismo.add_hline(
        y=media_privada, 
        line_dash="dot", 
        line_color="blue", 
        annotation_text=f"Média Privada: {media_privada:.1f}",
        annotation_position="top left"
    )

    fig_abismo.update_layout(height=600)
    st.plotly_chart(fig_abismo, use_container_width=True)

    q3_publica = df_analise[df_analise['TP_ESCOLA_LABEL'] == 'Pública']['MEDIA_GERAL'].quantile(0.75)
    st.info(f"""
    **Análise do Abismo:**
    - O terceiro quartil ($Q_3$) da Escola Pública está em **{q3_publica:.1f}**. 
    - Estatisticamente, isso indica que 75% dos alunos da rede pública paranaense possuem notas abaixo do que é a "base" (início do corpo do boxplot) da rede privada.
    - O **entalhe (notch)** no centro das caixas indica o intervalo de confiança da mediana; como os entalhes não se sobrepõem, a diferença entre as redes é estatisticamente significativa.
    """)

    st.warning("""
    **Insight para o Slide:** O desafio da equidade no Paraná não é apenas elevar a média, mas reduzir a dispersão da rede pública para que o seu topo ($Q_3$ e Outliers) consiga competir com a média da rede privada em cursos de alta concorrência.
    """)