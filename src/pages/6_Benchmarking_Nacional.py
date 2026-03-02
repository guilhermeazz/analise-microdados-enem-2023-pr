import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats

from utils.data_loader import carregar_dados_projeto

st.set_page_config(page_title="Benchmarking Nacional", page_icon="📈", layout="wide")

df_pr, df_br, _ = carregar_dados_projeto()

if df_pr is not None and df_br is not None:

    st.header("6. Benchmarking Nacional: Paraná vs. Brasil")
    st.write("Análise de significância estatística para validar a superioridade ou disparidade do desempenho paranaense.")

    provas = {
        'NU_NOTA_CN': 'Ciências Natureza',
        'NU_NOTA_CH': 'Ciências Humanas',
        'NU_NOTA_LC': 'Linguagens e Códigos',
        'NU_NOTA_MT': 'Matemática',
        'NU_NOTA_REDACAO': 'Redação'
    }

    resultados_testes = []

    for col, nome in provas.items():
        notas_pr = df_pr[col].dropna()
        notas_br = df_br[col].dropna()
        
        media_pr = notas_pr.mean()
        media_br = notas_br.mean()
        
        t_stat, p_valor = stats.ttest_ind(notas_pr, notas_br, equal_var=False, alternative='greater')
        
        significativo = "Sim" if p_valor < 0.05 else "Não"
        diferenca = media_pr - media_br
        
        resultados_testes.append({
            'Área': nome,
            'Média PR': media_pr,
            'Média Brasil': media_br,
            'Diferença (pontos)': diferenca,
            'P-Valor': p_valor,
            'Superioridade Significativa': significativo
        })

    df_resumo = pd.DataFrame(resultados_testes)

    cols = st.columns(5)
    for i, row in df_resumo.iterrows():
        with cols[i]:
            cor_delta = "normal" if row['Superioridade Significativa'] == "Sim" else "off"
            st.metric(
                label=row['Área'], 
                value=f"{row['Média PR']:.1f}", 
                delta=f"{row['Diferença (pontos)']:.1f}",
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
        color_discrete_map={'Média PR': '#1f77b4', 'Média Brasil': '#7f7f7f'}
    )
    fig.update_layout(yaxis=dict(range=[400, 680]), height=450, margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    
    st.subheader("Tabela de Evidência Estatística")

    def colorir_significancia(val):
        color = '#c8e6c9' if val == "Sim" else '#ffcdd2'
        return f'background-color: {color}; color: black; font-weight: bold'

    st.dataframe(
        df_resumo.style.applymap(colorir_significancia, subset=['Superioridade Significativa'])
        .format({
            'Média PR': '{:.2f}',
            'Média Brasil': '{:.2f}',
            'Diferença (pontos)': '{:+.2f}',
            'P-Valor': '{:.4e}'
        }),
        use_container_width=True
    )

    st.info("""
    **Interpretando a Evidência (Para o Slide):**
    - **P-Valor < 0.05:** Rejeitamos a hipótese nula. A superioridade do Paraná é estatisticamente real.
    - **P-Valor Científico:** Notações como `e-10` indicam valores extremamente próximos de zero, confirmando alta confiança nos dados.
    - O Paraná tende a superar a média nacional em áreas específicas; este benchmarking orienta onde o estado é referência.
    """)