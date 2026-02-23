import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats
from utils.data_loader import carregar_dados
from utils.dicionarios import mapa_lingua

st.set_page_config(page_title="Língua Estrangeira", page_icon="🌎", layout="wide")

df_brasil = carregar_dados()

if df_brasil is not None:
    df_parana = df_brasil[df_brasil['SG_UF_PROVA'] == 'PR'].copy()

    st.header("9. Escolha de Língua Estrangeira: Inglês vs. Espanhol")
    st.write("Análise da preferência idiomática e seu impacto na nota de Linguagens e Códigos.")

    st.subheader("Distribuição das Escolhas")
    
    prop_pr = df_parana['TP_LINGUA'].value_counts(normalize=True).rename(index=mapa_lingua) * 100
    prop_br = df_brasil['TP_LINGUA'].value_counts(normalize=True).rename(index=mapa_lingua) * 100

    df_prop = pd.DataFrame({
        'Idioma': prop_pr.index,
        'Paraná (%)': prop_pr.values,
        'Brasil (%)': prop_br.values
    }).melt(id_vars='Idioma', var_name='Local', value_name='Porcentagem')

    fig_prop = px.bar(
        df_prop, x='Idioma', y='Porcentagem', color='Local',
        barmode='group', text_auto='.1f',
        color_discrete_map={'Paraná (%)': '#1f77b4', 'Brasil (%)': '#7f7f7f'}
    )
    st.plotly_chart(fig_prop, use_container_width=True)

    st.markdown("---")

    st.subheader("Desempenho em Linguagens por Idioma (Paraná)")

    df_lc_pr = df_parana.dropna(subset=['NU_NOTA_LC'])
    
    medias_lingua = df_lc_pr.groupby('TP_LINGUA')['NU_NOTA_LC'].mean().rename(index=mapa_lingua)

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Média de Linguagens (Inglês)", f"{medias_lingua['Inglês']:.2f}")
    with c2:
        diff = medias_lingua['Espanhol'] - medias_lingua['Inglês']
        st.metric("Média de Linguagens (Espanhol)", f"{medias_lingua['Espanhol']:.2f}", delta=f"{diff:.2f}")

    df_lc_pr['Idioma'] = df_lc_pr['TP_LINGUA'].map(mapa_lingua)
    fig_box = px.box(
        df_lc_pr, x='Idioma', y='NU_NOTA_LC', color='Idioma',
        title="Dispersão da Nota de Linguagens por Escolha de Idioma no PR",
        color_discrete_map={'Inglês': '#1f77b4', 'Espanhol': '#d62728'}
    )
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")
    st.subheader("Validação Estatística")

    notas_ingles = df_lc_pr[df_lc_pr['TP_LINGUA'] == 0]['NU_NOTA_LC']
    notas_espanhol = df_lc_pr[df_lc_pr['TP_LINGUA'] == 1]['NU_NOTA_LC']

    t_stat, p_valor = stats.ttest_ind(notas_ingles, notas_espanhol, equal_var=False)

    if p_valor < 0.05:
        maior = "Inglês" if medias_lingua['Inglês'] > medias_lingua['Espanhol'] else "Espanhol"
        st.success(f"✅ **Diferença Estatisticamente Significativa:** O idioma **{maior}** apresenta notas superiores em Linguagens (p-valor: {p_valor:.4e}).")
    else:
        st.warning("⚠️ **Sem Diferença Significativa:** A escolha do idioma não parece afetar a média final de Linguagens de forma relevante.")

    st.info("""
    **Insight:** Frequentemente, candidatos com maior histórico de estudo formal (escolas particulares) optam pelo Inglês, enquanto o Espanhol é a escolha majoritária em contextos de menor exposição linguística prévia, o que pode explicar a disparidade nas notas.
    """)