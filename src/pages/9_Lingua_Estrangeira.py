import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats
from utils.data_loader import carregar_dados_projeto

st.set_page_config(page_title="Língua Estrangeira", page_icon="🌎", layout="wide")

df_pr, df_br, _ = carregar_dados_projeto()

if df_pr is not None and df_br is not None:

    st.header("9. Escolha de Língua Estrangeira: Inglês vs. Espanhol")
    st.write("Análise da preferência idiomática e seu impacto na nota de Linguagens e Códigos.")

    st.subheader("Distribuição das Escolhas")
    
    prop_pr = df_pr['TP_LINGUA_LABEL'].value_counts(normalize=True) * 100
    prop_br = df_br['TP_LINGUA_LABEL'].value_counts(normalize=True) * 100

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

    medias_lingua = df_pr.groupby('TP_LINGUA_LABEL')['NU_NOTA_LC'].mean()

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Média de Linguagens (Inglês)", f"{medias_lingua['Inglês']:.2f}")
    with c2:
        diff = medias_lingua['Espanhol'] - medias_lingua['Inglês']
        st.metric("Média de Linguagens (Espanhol)", f"{medias_lingua['Espanhol']:.2f}", delta=f"{diff:.2f}")

    fig_box = px.box(
        df_pr, x='TP_LINGUA_LABEL', y='NU_NOTA_LC', color='TP_LINGUA_LABEL',
        title="Dispersão da Nota de Linguagens por Escolha de Idioma no PR",
        labels={'TP_LINGUA_LABEL': 'Idioma', 'NU_NOTA_LC': 'Nota LC'},
        color_discrete_map={'Inglês': '#1f77b4', 'Espanhol': '#d62728'},
        points=False
    )
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")
    st.subheader("Validação Estatística")

    notas_ingles = df_pr[df_pr['TP_LINGUA_LABEL'] == 'Inglês']['NU_NOTA_LC'].dropna()
    notas_espanhol = df_pr[df_pr['TP_LINGUA_LABEL'] == 'Espanhol']['NU_NOTA_LC'].dropna()

    t_stat, p_valor = stats.ttest_ind(notas_ingles, notas_espanhol, equal_var=False)

    if p_valor < 0.05:
        maior = "Inglês" if medias_lingua['Inglês'] > medias_lingua['Espanhol'] else "Espanhol"
        st.success(f"✅ **Diferença Estatisticamente Significativa:** O idioma **{maior}** apresenta notas superiores em Linguagens (p-valor: {p_valor:.4e}).")
    else:
        st.warning("⚠️ **Sem Diferença Significativa:** A escolha do idioma não parece afetar a média final de Linguagens de forma relevante.")

    st.info("""
    **Insight:** Frequentemente, candidatos com maior histórico de estudo formal optam pelo Inglês, enquanto o Espanhol é uma escolha comum em contextos de menor exposição linguística prévia, o que reflete na disparidade das notas.
    """)