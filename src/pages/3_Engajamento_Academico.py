import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import carregar_dados
from utils.dicionarios import mapa_treineiro

st.set_page_config(page_title="Engajamento Acadêmico", page_icon="📚", layout="wide")

df_brasil = carregar_dados()

if df_brasil is not None:
    df_parana = df_brasil[df_brasil['SG_UF_PROVA'] == 'PR'].copy()

    st.header("3. Engajamento Acadêmico: Treineiros")
    st.write("O estado do Paraná possui uma taxa de 'treineiros' superior à média nacional?")
    
    st.markdown("---")

    pct_treineiro_pr = df_parana['IN_TREINEIRO'].value_counts(normalize=True).get(1, 0) * 100
    pct_treineiro_br = df_brasil['IN_TREINEIRO'].value_counts(normalize=True).get(1, 0) * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            label="Taxa de Treineiros - Paraná", 
            value=f"{pct_treineiro_pr:.2f}%"
        )
        
    with col2:
        delta_pp = pct_treineiro_pr - pct_treineiro_br
        st.metric(
            label="Taxa de Treineiros - Brasil (Média)", 
            value=f"{pct_treineiro_br:.2f}%", 
            delta=f"{delta_pp:.2f} p.p (diferença PR x BR)",
            delta_color="normal"
        )

    st.markdown("---")
    
    st.subheader("Distribuição Comparativa Geral")
    
    prop_pr = df_parana['IN_TREINEIRO'].value_counts(normalize=True).rename(index=mapa_treineiro) * 100
    prop_br = df_brasil['IN_TREINEIRO'].value_counts(normalize=True).rename(index=mapa_treineiro) * 100
    
    df_plot = pd.DataFrame({
        'Categoria': prop_pr.index,
        'Paraná (%)': prop_pr.values,
        'Brasil (%)': prop_br.values
    })
    
    df_melt = df_plot.melt(id_vars='Categoria', var_name='Local', value_name='Porcentagem')
    

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
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    status = "superior" if pct_treineiro_pr > pct_treineiro_br else "inferior"
    st.info(f"💡 **Resposta Direta:** A taxa de treineiros no Paraná ({pct_treineiro_pr:.2f}%) é **{status}** à média nacional ({pct_treineiro_br:.2f}%).")