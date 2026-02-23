import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats
from utils.data_loader import carregar_dados
from utils.dicionarios import mapa_dependencia_adm

st.set_page_config(page_title="Ensino Técnico e Federal", page_icon="⚙️", layout="wide")

df_brasil = carregar_dados()

if df_brasil is not None:
    df_parana = df_brasil[df_brasil['SG_UF_PROVA'] == 'PR'].copy()

    st.header("8. Desempenho: Ensino Técnico/Federal")
    st.write("Alunos de escolas Federais (IFPR/Técnicas) superam a média de Matemática do Paraná?")

    df_mt_pr = df_parana.dropna(subset=['NU_NOTA_MT'])

    media_estadual = df_mt_pr['NU_NOTA_MT'].mean()

    notas_federal = df_mt_pr[df_mt_pr['TP_DEPENDENCIA_ADM_ESC'] == 1]['NU_NOTA_MT']
    media_federal = notas_federal.mean()

    c1, c2 = st.columns(2)
    
    with c1:
        st.metric("Média Estadual (Matemática)", f"{media_estadual:.2f}")
    
    with c2:
        diff = media_federal - media_estadual
        st.metric("Média Escolas Federais/IFPR", f"{media_federal:.2f}", delta=f"{diff:.2f} pts acima")

    st.markdown("---")

    st.subheader("Distribuição por Dependência Administrativa")

    df_resumo_adm = df_mt_pr.groupby('TP_DEPENDENCIA_ADM_ESC')['NU_NOTA_MT'].agg(['mean', 'count']).reset_index()
    df_resumo_adm['Tipo'] = df_resumo_adm['TP_DEPENDENCIA_ADM_ESC'].map(mapa_dependencia_adm)
    
    df_resumo_adm = df_resumo_adm.sort_values(by='mean', ascending=False)

    fig_adm = px.bar(
        df_resumo_adm, 
        x='Tipo', 
        y='mean',
        text_auto='.1f',
        title="Nota Média em Matemática por Tipo de Escola no PR",
        labels={'mean': 'Nota Média', 'Tipo': 'Dependência Administrativa'},
        color='Tipo',
        color_discrete_map={'Federal (Técnicos/IFs)': '#2ca02c'}
    )

    fig_adm.add_hline(y=media_estadual, line_dash="dash", line_color="red", 
                      annotation_text=f"Média Estadual: {media_estadual:.1f}")
    
    st.plotly_chart(fig_adm, use_container_width=True)

    st.markdown("---")
    st.subheader("Validação Estatística")

    notas_outros = df_mt_pr[df_mt_pr['TP_DEPENDENCIA_ADM_ESC'] != 1]['NU_NOTA_MT']

    t_stat, p_valor = stats.ttest_ind(notas_federal, notas_outros, equal_var=False)

    if p_valor < 0.05:
        st.success(f"✅ **Diferença Significativa:** Com um p-valor de {p_valor:.4e}, confirmamos que o desempenho das escolas Federais/Técnicas em Matemática é superior ao restante da rede de forma estatisticamente relevante.")
    else:
        st.warning("⚠️ **Sem Diferença Significativa:** Não foi possível confirmar superioridade estatística.")

    st.info("""
    **Por que focar nas Escolas Federais?**
    Os Institutos Federais (IFs) possuem um modelo de ensino integrado ao técnico que, historicamente, apresenta alto desempenho no ENEM devido à infraestrutura e seleção por processo seletivo (vestibulinho).
    """)