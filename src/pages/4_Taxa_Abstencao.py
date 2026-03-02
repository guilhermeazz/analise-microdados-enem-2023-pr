import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import chi2_contingency 

from utils.data_loader import carregar_dados_projeto

st.set_page_config(page_title="Taxa de Abstenção", page_icon="📉", layout="wide")

_, _, df_total = carregar_dados_projeto()

if df_total is not None:
    
    def calcular_status_presenca(df):
        presenca_dia1 = (df['TP_PRESENCA_CH'] == 1) & (df['TP_PRESENCA_LC'] == 1)
        presenca_dia2 = (df['TP_PRESENCA_CN'] == 1) & (df['TP_PRESENCA_MT'] == 1)
        
        df['ABSTENCAO'] = (df['TP_PRESENCA_CH'] == 0) & (df['TP_PRESENCA_MT'] == 0)
        
        df['DESISTENCIA'] = (df['TP_PRESENCA_CH'] == 1) & (df['TP_PRESENCA_MT'] == 0)
        return df

    df_total = calcular_status_presenca(df_total)
    
    df_parana = df_total[df_total['SG_UF_PROVA'] == 'PR'].copy()
    df_brasil_comparativo = df_total[df_total['SG_UF_PROVA'] != 'PR'].copy()

    st.header("4. Taxa de Abstenção e Desistência")
    st.write("O Paraná teve uma taxa de ausentes maior ou menor que a média nacional? Existe relação com o município?")

    taxa_abs_pr = df_parana['ABSTENCAO'].mean() * 100
    taxa_abs_br = df_brasil_comparativo['ABSTENCAO'].mean() * 100
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(
            label="Abstenção no Paraná", 
            value=f"{taxa_abs_pr:.2f}%"
        )
    with col2:
        st.metric(
            label="Abstenção no Brasil (Excl. PR)", 
            value=f"{taxa_abs_br:.2f}%", 
            delta=f"{taxa_abs_pr - taxa_abs_br:.2f} p.p.",
            delta_color="inverse" 
        )

    st.markdown("---")

    st.subheader("Análise Geográfica: Municípios do Paraná")
    st.write("Municípios com as maiores taxas de abstenção (mínimo de 100 candidatos):")

    mun_stats = df_parana.groupby('NO_MUNICIPIO_PROVA').agg({
        'ABSTENCAO': ['mean', 'count']
    })
    mun_stats.columns = ['Taxa_Abstencao', 'Total_Candidatos']
    mun_stats['Taxa_Abstencao'] *= 100
    
    mun_stats = mun_stats[mun_stats['Total_Candidatos'] >= 100].sort_values(by='Taxa_Abstencao', ascending=False)

    fig_mun = px.bar(
        mun_stats.head(10).reset_index(),
        x='Taxa_Abstencao',
        y='NO_MUNICIPIO_PROVA',
        orientation='h',
        title="Top 10 Municípios com Maior Abstenção no PR",
        labels={'Taxa_Abstencao': 'Abstenção (%)', 'NO_MUNICIPIO_PROVA': 'Município'},
        color='Taxa_Abstencao',
        color_continuous_scale='Reds'
    )
    fig_mun.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_mun, use_container_width=True)

    st.markdown("---")
    
    st.subheader("Existe correlação entre Município e Abstenção?")
    
    contingency_table = pd.crosstab(df_parana['NO_MUNICIPIO_PROVA'], df_parana['ABSTENCAO'])
    chi2, p, dof, ex = chi2_contingency(contingency_table)
    
    st.write(f"Utilizando o **Teste Qui-Quadrado de Independência** para os dados do Paraná:")
    st.write(f"- Valor de p (p-value): **{p:.4e}**")
    
    if p < 0.05:
        st.success("✅ **Resultado Significativo:** O município influencia estatisticamente a probabilidade de abstenção no PR.")
    else:
        st.warning("❌ **Resultado Não Significativo:** A abstenção parece ser distribuída de forma uniforme pelo estado.")

    st.info("💡 **Dica para o Slide:** Cite que fatores como distância dos locais de prova e infraestrutura urbana de cada cidade impactam esse resultado.")