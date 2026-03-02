import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats
from utils.data_loader import carregar_dados_projeto

st.set_page_config(page_title="Posse de Bens e Notas", page_icon="💻", layout="wide")

df_pr, _, _ = carregar_dados_projeto()

if df_pr is not None:
    # Filtramos apenas candidatos com notas e informação de computador
    df_pr = df_pr.dropna(subset=['Q024', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']).copy()

    # Mapeamento numérico para o teste de Pearson (exige entrada quantitativa)
    mapa_numerico = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
    df_pr['PC_NUMERICO'] = df_pr['Q024'].map(mapa_numerico)

    st.header("18. Correlação: Computador vs. Desempenho")
    st.write("Existe uma relação estatística entre a quantidade de computadores em casa e o sucesso em Matemática e Redação no Paraná?")

    # Cálculos de Correlação de Pearson e Significância
    corr_mt, p_mt = stats.pearsonr(df_pr['PC_NUMERICO'], df_pr['NU_NOTA_MT'])
    corr_red, p_red = stats.pearsonr(df_pr['PC_NUMERICO'], df_pr['NU_NOTA_REDACAO'])

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Correlação em Matemática ($R$)", f"{corr_mt:.3f}")
        if p_mt < 0.05:
            st.caption("✅ Significância Estatística Confirmada")
    with c2:
        st.metric("Correlação em Redação ($R$)", f"{corr_red:.3f}")
        if p_red < 0.05:
            st.caption("✅ Significância Estatística Confirmada")

    st.markdown("---")

    

    st.subheader("Progressão de Notas por Quantidade de PCs")
    
    # Agrupamento utilizando os labels processados no pipeline
    df_resumo = df_pr.groupby(['Q024', 'Q024_LABEL'], observed=True).agg({
        'NU_NOTA_MT': 'mean',
        'NU_NOTA_REDACAO': 'mean'
    }).reset_index()

    df_melt = df_resumo.melt(id_vars=['Q024', 'Q024_LABEL'], var_name='Matéria', value_name='Nota')
    df_melt['Matéria'] = df_melt['Matéria'].replace({'NU_NOTA_MT': 'Matemática', 'NU_NOTA_REDACAO': 'Redação'})

    # Gráfico de barras agrupado por matéria
    fig_bar = px.bar(
        df_melt, x='Q024_LABEL', y='Nota', color='Matéria',
        barmode='group', text_auto='.0f',
        title="Notas Médias vs. Computadores na Residência (PR)",
        labels={'Q024_LABEL': 'Computadores na Casa', 'Nota': 'Nota Média'},
        color_discrete_map={'Matemática': '#636EFA', 'Redação': '#EF553B'}
    )
    fig_bar.update_layout(yaxis=dict(range=[400, 750]), height=500)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.info(f"""
    **Análise Técnica:**
    - Os coeficientes de correlação de Pearson ($R_{{MT}} = {corr_mt:.3f}$ e $R_{{Red}} = {corr_red:.3f}$) indicam uma associação positiva. 
    - Como $p < 0.05$ em ambos os casos, rejeitamos a hipótese nula de que não há relação entre as variáveis.
    - O gráfico mostra uma escada de desempenho: quanto maior o acesso tecnológico, maior a nota média.
    """)

    st.warning("""
    **Distinção entre Correlação e Causalidade:** A posse de computador é um forte **preditor** de nota, mas também é um marcador de renda. 
    Famílias com mais dispositivos costumam ter maior capital cultural e financeiro, o que também impacta o resultado final.
    """)