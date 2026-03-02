import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import carregar_dados_projeto

st.set_page_config(page_title="Engajamento Acadêmico", page_icon="📚", layout="wide")

df_pr, df_br, _ = carregar_dados_projeto()

if df_pr is not None and df_br is not None:
    
    st.header("3. Engajamento Acadêmico: Treineiros")
    st.write("O estado do Paraná possui uma taxa de 'treineiros' superior à média nacional?")
    
    st.markdown("---")

    pct_treineiro_pr = df_pr['IN_TREINEIRO'].value_counts(normalize=True).get(1, 0) * 100
    pct_treineiro_br = df_br['IN_TREINEIRO'].value_counts(normalize=True).get(1, 0) * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Taxa de Treineiros - Paraná", 
            value=f"{pct_treineiro_pr:.2f}%"
        )
        
    with col2:
        delta_pp = pct_treineiro_pr - pct_treineiro_br
        st.metric(
            label="Taxa de Treineiros - Brasil (Excl. PR)", 
            value=f"{pct_treineiro_br:.2f}%", 
            delta=f"{delta_pp:.2f} p.p. (diferença vs PR)",
            delta_color="normal"
        )

    st.markdown("---")
    
    st.subheader("Distribuição Comparativa Geral")
    
    def gerar_dados_plot(df, local):
        prop = df['IN_TREINEIRO_LABEL'].value_counts(normalize=True) * 100
        return prop.reset_index().rename(columns={'IN_TREINEIRO_LABEL': 'Categoria', 'proportion': f'{local} (%)'})

    df_plot_pr = gerar_dados_plot(df_pr, 'Paraná')
    df_plot_br = gerar_dados_plot(df_br, 'Brasil')

    df_final = pd.merge(df_plot_pr, df_plot_br, on='Categoria')
    df_melt = df_final.melt(id_vars='Categoria', var_name='Local', value_name='Porcentagem')

    fig = px.bar(
        df_melt, 
        x='Categoria', 
        y='Porcentagem', 
        color='Local', 
        barmode='group',
        text_auto='.2f',
        color_discrete_map={'Paraná (%)': '#1f77b4', 'Brasil (%)': '#7f7f7f'}
    )
    
    fig.update_layout(
        yaxis_title="Porcentagem (%)",
        xaxis_title="",
        legend_title="Região",
        height=450,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    status = "superior" if pct_treineiro_pr > pct_treineiro_br else "inferior"
    st.info(f"💡 **Insight para o Slide:** A taxa de treineiros no Paraná ({pct_treineiro_pr:.2f}%) é **{status}** à média nacional ({pct_treineiro_br:.2f}%).")

    st.caption("Nota: 'Treineiros' são candidatos menores de 18 anos que ainda não concluíram o ensino médio.")