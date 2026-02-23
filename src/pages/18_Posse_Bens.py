import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats
from utils.data_loader import carregar_dados
from utils.dicionarios import mapa_computador

st.set_page_config(page_title="Posse de Bens e Notas", page_icon="💻", layout="wide")

df_brasil = carregar_dados()

if df_brasil is not None:
    df_pr = df_brasil[df_brasil['SG_UF_PROVA'] == 'PR'].copy()
    df_pr = df_pr.dropna(subset=['Q024', 'NU_NOTA_MT', 'NU_NOTA_REDACAO'])

    mapa_numerico = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    df_pr['PC_NUMERICO'] = df_pr['Q024'].map(mapa_numerico)

    st.header("18. Correlação: Computador vs. Desempenho")
    st.write("Existe uma relação estatística entre a quantidade de PCs em casa e o sucesso em Matemática e Redação?")

    corr_mt, p_mt = stats.pearsonr(df_pr['PC_NUMERICO'], df_pr['NU_NOTA_MT'])
    corr_red, p_red = stats.pearsonr(df_pr['PC_NUMERICO'], df_pr['NU_NOTA_REDACAO'])

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Correlação em Matemática", f"{corr_mt:.3f}", help="Varia de -1 a 1. Acima de 0.3 é considerada relevante.")
        if p_mt < 0.05:
            st.caption("✅ Estatisticamente Significativo")
    with c2:
        st.metric("Correlação em Redação", f"{corr_red:.3f}")
        if p_red < 0.05:
            st.caption("✅ Estatisticamente Significativo")

    st.markdown("---")

    st.subheader("Progressão de Notas por Quantidade de PCs")
    
    df_resumo = df_pr.groupby('Q024').agg({
        'NU_NOTA_MT': 'mean',
        'NU_NOTA_REDACAO': 'mean'
    }).rename(index=mapa_computador).reset_index()

    df_melt = df_resumo.melt(id_vars='Q024', var_name='Matéria', value_name='Nota')
    df_melt['Matéria'] = df_melt['Matéria'].replace({'NU_NOTA_MT': 'Matemática', 'NU_NOTA_REDACAO': 'Redação'})

    fig_bar = px.bar(
        df_melt, x='Q024', y='Nota', color='Matéria',
        barmode='group', text_auto='.0f',
        title="Notas Médias vs. Computadores na Residência (PR)",
        labels={'Q024': 'Posse de Computador', 'Nota': 'Nota Média'},
        color_discrete_map={'Matemática': '#636EFA', 'Redação': '#EF553B'}
    )
    fig_bar.update_layout(yaxis=dict(range=[400, 750]))
    st.plotly_chart(fig_bar, use_container_width=True)

    st.info(f"""
    **Análise Estatística:**
    - A correlação para Matemática ({corr_mt:.3f}) e Redação ({corr_red:.3f}) é **positiva**. 
    - Isso significa que, estatisticamente, cada computador adicional na casa tende a acompanhar um aumento nas notas.
    - Como o p-valor é menor que 0.05, descartamos a hipótese de que esse resultado seja obra do acaso.
    """)

    st.warning("""
    **Cuidado com a Causalidade:** Ter o computador causa a nota maior, ou famílias que têm condições de comprar computadores também têm acesso a melhores escolas e cursinhos? 
    Na Ciência de Dados, dizemos que a variável 'Computador' é um excelente **preditor**, mas o sucesso é multifatorial.
    """)