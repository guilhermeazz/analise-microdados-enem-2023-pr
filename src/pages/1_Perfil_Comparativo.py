import streamlit as st
import pandas as pd
import plotly.graph_objects as go 

from utils.data_loader import carregar_dados_projeto
from utils.dicionarios import mapa_idade

st.set_page_config(page_title="Perfil Comparativo", page_icon="👥", layout="wide")

df_pr, df_brasil, _ = carregar_dados_projeto()

if df_pr is not None and df_brasil is not None:
    
    st.header("1. Perfil Comparativo: Paraná x Brasil")
    st.write("Como se caracteriza o candidato médio do Paraná e como esse perfil diverge da média nacional?")
    
    st.sidebar.success(f'Total Brasil: {len(df_brasil):,}')
    st.sidebar.info(f'Total Paraná: {len(df_pr):,}')

    def gerar_comparativo(df_estado, df_nacional, coluna_label):
        pct_estado = df_estado[coluna_label].value_counts(normalize=True) * 100
        pct_nacional = df_nacional[coluna_label].value_counts(normalize=True) * 100
        return pd.DataFrame({'Paraná (%)': pct_estado, 'Brasil (%)': pct_nacional}).fillna(0)

    def calcular_dados_piramide(df):
        df_agrupado = df.groupby(['TP_FAIXA_ETARIA', 'TP_SEXO_LABEL']).size().unstack(fill_value=0)
        df_pct = (df_agrupado / df_agrupado.sum().sum()) * 100
        
        df_pct = df_pct.reindex(range(1, 21)).fillna(0)
        
        df_pct.index = df_pct.index.map(mapa_idade)
        return df_pct
    
    def plotar_piramide(df_pct, titulo):
        homens = df_pct.get('Masculino', 0) * -1
        mulheres = df_pct.get('Feminino', 0)
        idades = df_pct.index
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=idades, x=homens, name='Masculino', orientation='h',
            marker=dict(color='#1f77b4'),
            customdata=abs(homens).round(2),
            hovertemplate='Masculino: %{customdata}%<extra></extra>' 
        ))
        
        fig.add_trace(go.Bar(
            y=idades, x=mulheres, name='Feminino', orientation='h',
            marker=dict(color='#d62728'),
            customdata=mulheres.round(2),
            hovertemplate='Feminino: %{customdata}%<extra></extra>'
        ))
        
        fig.update_layout(
            title=titulo, barmode='relative', bargap=0.1, height=500,
            xaxis=dict(
                title='Distribuição (%)',
                tickvals=[-10, -5, 0, 5, 10], 
                ticktext=['10%', '5%', '0%', '5%', '10%']
            )
        )
        return fig
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Gênero")
        df_comp_sexo = gerar_comparativo(df_pr, df_brasil, 'TP_SEXO_LABEL')
        st.bar_chart(df_comp_sexo)

    with col_b:
        st.subheader("Cor/Raça")
        df_comp_raca = gerar_comparativo(df_pr, df_brasil, 'TP_COR_RACA_LABEL')
        st.bar_chart(df_comp_raca)

    st.markdown("---")
    st.subheader("Pirâmide Etária: Distribuição por Idade e Sexo")
    
    col1, col2 = st.columns(2)
    with col1:
        piramide_pr = calcular_dados_piramide(df_pr)
        st.plotly_chart(plotar_piramide(piramide_pr, "Paraná (PR)"), use_container_width=True)
    with col2:
        piramide_br = calcular_dados_piramide(df_brasil)
        st.plotly_chart(plotar_piramide(piramide_br, "Brasil (Excl. PR)"), use_container_width=True)