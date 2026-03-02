import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import carregar_dados_projeto

st.set_page_config(page_title="Gaps de Equidade", page_icon="⚖️", layout="wide")

df_pr, df_br, _ = carregar_dados_projeto()

if df_pr is not None and df_br is not None:

    st.header("11. Gaps de Equidade: Sexo e Cor/Raça")
    st.write("Análise detalhada das médias por grupo demográfico no Paraná vs. Brasil.")

    st.subheader("1. Desempenho por Gênero")
    
    def extrair_dados_sexo(df, local):
        res = df.groupby('TP_SEXO_LABEL', observed=True)['MEDIA_GERAL'].mean().reset_index()
        res.columns = ['Sexo', 'Média Geral']
        res['Local'] = local
        return res

    sexo_pr = extrair_dados_sexo(df_pr, 'Paraná')
    sexo_br = extrair_dados_sexo(df_br, 'Brasil (Excl. PR)')
    df_sexo_comp = pd.concat([sexo_pr, sexo_br])

    avg_m_pr = sexo_pr[sexo_pr['Sexo'] == 'Masculino']['Média Geral'].values[0]
    avg_f_pr = sexo_pr[sexo_pr['Sexo'] == 'Feminino']['Média Geral'].values[0]
    gap_pr = avg_m_pr - avg_f_pr

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Média Masculina (PR)", f"{avg_m_pr:.2f}")
    with c2:
        st.metric("Média Feminina (PR)", f"{avg_f_pr:.2f}")
    with c3:
        st.metric("Gap de Gênero (M - F)", f"{gap_pr:.2f} pts", delta=f"{gap_pr:.2f}", delta_color="off")

    fig_sexo = px.bar(
        df_sexo_comp, x='Sexo', y='Média Geral', color='Local',
        barmode='group', text_auto='.1f',
        title="Comparativo de Médias: Masculino vs. Feminino",
        color_discrete_map={'Paraná': '#1f77b4', 'Brasil (Excl. PR)': '#7f7f7f'}
    )
    fig_sexo.update_layout(yaxis=dict(range=[450, 600]), margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_sexo, use_container_width=True)

    st.markdown("---")
    st.subheader("2. Desempenho por Cor/Raça")

    

    def preparar_dados_raca(df, local):
        df_r = df.groupby('TP_COR_RACA_LABEL', observed=True)['MEDIA_GERAL'].mean().reset_index()
        df_r.columns = ['Cor/Raça', 'Nota Média']
        df_r['Local'] = local
        return df_r

    raca_pr = preparar_dados_raca(df_pr, 'Paraná')
    raca_br = preparar_dados_raca(df_br, 'Brasil (Excl. PR)')
    df_raca_comp = pd.concat([raca_pr, raca_br])

    fig_raca = px.bar(
        df_raca_comp, x='Cor/Raça', y='Nota Média', color='Local',
        barmode='group', text_auto='.1f',
        title="Média Geral por Cor/Raça",
        color_discrete_map={'Paraná': '#1f77b4', 'Brasil (Excl. PR)': '#7f7f7f'}
    )
    fig_raca.update_layout(yaxis=dict(range=[400, 600]), margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_raca, use_container_width=True)

    st.markdown("---")
    
    lider_sexo = sexo_pr.loc[sexo_pr['Média Geral'].idxmax(), 'Sexo']
    lider_raca = raca_pr.loc[raca_pr['Nota Média'].idxmax(), 'Cor/Raça']

    st.success(f"💡 **Destaques do Paraná:** O grupo com maior média por sexo é **{lider_sexo}** e por cor/raça é **{lider_raca}**.")

    st.info("""
    **Interpretação da Equidade:** A distância entre as barras de diferentes grupos demográficos no Paraná, comparada à mesma distância no Brasil, 
    indica o nível de desigualdade regional. Gaps menores no estado sugerem políticas de inclusão ou 
    distribuição educacional mais equilibrada.
    """)