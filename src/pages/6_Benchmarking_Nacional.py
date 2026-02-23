import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats

from utils.data_loader import carregar_dados

st.set_page_config(page_title="Benchmarking Nacional", page_icon="📈", layout="wide")

df_brasil = carregar_dados()

if df_brasil is not None:
    df_parana = df_brasil[df_brasil['SG_UF_PROVA'] == 'PR'].copy()
    
    df_resto_brasil = df_brasil[df_brasil['SG_UF_PROVA'] != 'PR'].copy()

    st.header("6. Benchmarking Nacional: Paraná vs. Brasil")
    st.write("Análise estatística para verificar em quais áreas o desempenho do Paraná é superior à média nacional com significância.")

    provas = {
        'NU_NOTA_CN': 'Ciências Natureza',
        'NU_NOTA_CH': 'Ciências Humanas',
        'NU_NOTA_LC': 'Linguagens e Códigos',
        'NU_NOTA_MT': 'Matemática',
        'NU_NOTA_REDACAO': 'Redação'
    }

    resultados_testes = []

    for col, nome in provas.items():
        notas_pr = df_parana[col].dropna()
        notas_br = df_resto_brasil[col].dropna()
        
        media_pr = notas_pr.mean()
        media_br = notas_br.mean()
        
        t_stat, p_valor = stats.ttest_ind(notas_pr, notas_br, equal_var=False, alternative='greater')
        
        significativo = "Sim" if p_valor < 0.05 else "Não"
        diferenca = media_pr - media_br
        
        resultados_testes.append({
            'Área': nome,
            'Média PR': media_pr,
            'Média Brasil': media_br,
            'Diferença (p.p)': diferenca,
            'P-Valor': p_valor,
            'Superioridade Significativa': significativo
        })

    df_resumo = pd.DataFrame(resultados_testes)

    cols = st.columns(5)
    for i, row in df_resumo.iterrows():
        with cols[i]:
            cor_delta = "normal" if row['Superioridade Significativa'] == "Sim" else "inverse"
            st.metric(
                label=row['Área'], 
                value=f"{row['Média PR']:.1f}", 
                delta=f"{row['Diferença (p.p)']:.1f}",
                delta_color=cor_delta
            )

    st.markdown("---")

    df_plot = df_resumo.melt(id_vars='Área', value_vars=['Média PR', 'Média Brasil'], var_name='Local', value_name='Nota')
    
    fig = px.bar(
        df_plot, 
        x='Área', 
        y='Nota', 
        color='Local', 
        barmode='group',
        text_auto='.1f',
        title="Comparativo de Médias: Paraná vs. Brasil",
        color_discrete_map={'Média PR': '#1f77b4', 'Média Brasil': '#7f7f7f'}
    )
    fig.update_layout(yaxis=dict(range=[400, 700]))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Tabela de Evidência Estatística")

    def colorir_significancia(val):
        color = '#c8e6c9' if val == "Sim" else '#ffcdd2'
        return f'background-color: {color}; color: black; font-weight: bold'

    st.dataframe(
        df_resumo.style.applymap(colorir_significancia, subset=['Superioridade Significativa']).format(precision=4),
        use_container_width=True
    )

    st.info("""
    **Interpretação Estatística:**
    - **P-Valor < 0.05:** Indica que a probabilidade da diferença ser ao acaso é menor que 5%. Confirmamos a superioridade.
    - **Diferença (p.p):** Diferença bruta em pontos entre as médias.
    - Devido ao alto número de candidatos (N), pequenas diferenças tornam-se estatisticamente significativas.
    """)