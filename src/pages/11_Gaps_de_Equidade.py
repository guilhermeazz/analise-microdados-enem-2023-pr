import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import carregar_dados
from utils.dicionarios import mapa_sexo, mapa_raca

st.set_page_config(page_title="Gaps de Equidade", page_icon="⚖️", layout="wide")

df_brasil = carregar_dados()

if df_brasil is not None:
    provas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    df_brasil['MEDIA_GERAL'] = df_brasil[provas].mean(axis=1)
    
    df_pr = df_brasil[df_brasil['SG_UF_PROVA'] == 'PR'].copy()
    df_br = df_brasil[df_brasil['SG_UF_PROVA'] != 'PR'].copy()

    st.header("11. Gaps de Equidade: Sexo e Cor/Raça")
    st.write("Análise detalhada das médias por grupo demográfico no Paraná vs. Brasil.")

    st.subheader("1. Desempenho por Gênero")
    
    def extrair_dados_sexo(df, local):
        res = df.groupby('TP_SEXO')['MEDIA_GERAL'].mean().rename(index=mapa_sexo).reset_index()
        res['Local'] = local
        return res

    sexo_pr = extrair_dados_sexo(df_pr, 'Paraná')
    sexo_br = extrair_dados_sexo(df_br, 'Brasil')
    df_sexo_comp = pd.concat([sexo_pr, sexo_br])

    avg_m_pr = sexo_pr[sexo_pr['TP_SEXO'] == 'Masculino']['MEDIA_GERAL'].values[0]
    avg_f_pr = sexo_pr[sexo_pr['TP_SEXO'] == 'Feminino']['MEDIA_GERAL'].values[0]
    gap_pr = avg_m_pr - avg_f_pr

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Média Masculina (PR)", f"{avg_m_pr:.2f}")
    with c2:
        st.metric("Média Feminina (PR)", f"{avg_f_pr:.2f}")
    with c3:
        st.metric("Gap (M - F)", f"{gap_pr:.2f} pts", delta_color="off")

    fig_sexo = px.bar(
        df_sexo_comp, x='TP_SEXO', y='MEDIA_GERAL', color='Local',
        barmode='group', text_auto='.1f',
        title="Comparativo de Médias: Masculino vs. Feminino",
        labels={'MEDIA_GERAL': 'Média Geral', 'TP_SEXO': 'Sexo'},
        color_discrete_map={'Paraná': '#1f77b4', 'Brasil': '#7f7f7f'}
    )
    fig_sexo.update_layout(yaxis=dict(range=[450, 600]))
    st.plotly_chart(fig_sexo, use_container_width=True)

    st.markdown("---")
    st.subheader("2. Desempenho por Cor/Raça")

    def preparar_dados_raca(df, local):
        df_r = df.groupby('TP_COR_RACA')['MEDIA_GERAL'].mean().rename(index=mapa_raca).reset_index()
        df_r['Local'] = local
        return df_r

    raca_pr = preparar_dados_raca(df_pr, 'Paraná')
    raca_br = preparar_dados_raca(df_br, 'Brasil')
    df_raca_comp = pd.concat([raca_pr, raca_br])

    fig_raca = px.bar(
        df_raca_comp, x='TP_COR_RACA', y='MEDIA_GERAL', color='Local',
        barmode='group', text_auto='.1f',
        title="Média Geral por Cor/Raça",
        labels={'MEDIA_GERAL': 'Nota Média', 'TP_COR_RACA': 'Cor/Raça'},
        color_discrete_map={'Paraná': '#1f77b4', 'Brasil': '#7f7f7f'}
    )
    fig_raca.update_layout(yaxis=dict(range=[400, 600]))
    st.plotly_chart(fig_raca, use_container_width=True)

    st.markdown("---")
    
    lider_sexo = sexo_pr.loc[sexo_pr['MEDIA_GERAL'].idxmax(), 'TP_SEXO']
    lider_raca = raca_pr.loc[raca_pr['MEDIA_GERAL'].idxmax(), 'TP_COR_RACA']

    st.success(f"💡 **Destaques do Paraná:** O grupo com maior média por sexo é **{lider_sexo}** e por cor/raça é **{lider_raca}**.")

    st.info("""
    **Nota:** As disparidades de desempenho costumam refletir desigualdades históricas de acesso a recursos. 
    Observar se as barras do Paraná estão mais 'próximas' entre si do que as barras do Brasil indica o nível de equidade relativa do estado.
    """)