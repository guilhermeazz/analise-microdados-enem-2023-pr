import streamlit as st
import pandas as pd
import plotly.graph_objects as go 

from utils.data_loader import carregar_dados
from utils.dicionarios import mapa_sexo, mapa_raca, mapa_idade

st.set_page_config(page_title="Perfil Comparativo", page_icon="👥", layout="wide")

df_brasil = carregar_dados()

if df_brasil is not None:
    df_parana = df_brasil[df_brasil['SG_UF_PROVA'] == 'PR'].copy()

    st.header("1. Perfil Comparativo: Paraná x Brasil")
    st.write("Como se caracteriza o candidato médio do Paraná em termos de faixa etária, cor/raça e sexo, e como esse perfil diverge da média nacional?")
    st.sidebar.success(f'Total Brasil: {len(df_brasil):,} \nTotal Paraná: {len(df_parana):,}')

    def gerar_comparativo(df_estado, df_nacional, coluna_alvo, dicionario_mapa):
        pct_estado = df_estado[coluna_alvo].value_counts(normalize=True).rename(index=dicionario_mapa) * 100
        pct_nacional = df_nacional[coluna_alvo].value_counts(normalize=True).rename(index=dicionario_mapa) * 100
        return pd.DataFrame({'Paraná (%)': pct_estado, 'Brasil (%)': pct_nacional}).fillna(0)

    def calcular_dados_piramide(df):
        df_agrupado = df.groupby(['TP_FAIXA_ETARIA', 'TP_SEXO']).size().unstack(fill_value=0)
        df_pct = (df_agrupado / df_agrupado.sum().sum()) * 100
        df_pct = df_pct.reindex(range(1, 21)).fillna(0)
        df_pct.index = df_pct.index.map(mapa_idade)
        return df_pct
    
    def plotar_piramide(df_pct, titulo):
        homens = df_pct.get('M', 0) * -1
        mulheres = df_pct.get('F', 0)
        idades = df_pct.index
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=idades,
            x=homens,
            name='Masculino',
            orientation='h',
            marker=dict(color='#1f77b4'),
            customdata=abs(homens).round(2),
            hovertemplate='Masculino: %{customdata}%<extra></extra>' 
        ))
        
        fig.add_trace(go.Bar(
            y=idades,
            x=mulheres,
            name='Feminino',
            orientation='h',
            marker=dict(color='#d62728'),
            customdata=mulheres.round(2),
            hovertemplate='Feminino: %{customdata}%<extra></extra>'
        ))
        
        fig.update_layout(
            title=titulo,
            barmode='relative',
            bargap=0.1,
            height=500,
            margin=dict(l=0, r=0, t=40, b=0),
            xaxis=dict(
                title='Distribuição (%)',
                tickvals=[-15, -10, -5, 0, 5, 10, 15], 
                ticktext=['15%', '10%', '5%', '0%', '5%', '10%', '15%']
            )
        )
        return fig
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Gênero")
        df_comp_sexo = gerar_comparativo(df_parana, df_brasil, 'TP_SEXO', mapa_sexo)
        st.bar_chart(df_comp_sexo)

    with col_b:
        st.subheader("Cor/Raça")
        df_comp_raca = gerar_comparativo(df_parana, df_brasil, 'TP_COR_RACA', mapa_raca)
        st.bar_chart(df_comp_raca)

    st.markdown("---")
    st.subheader("Faixa Etária")
    
    piramide_pr = calcular_dados_piramide(df_parana)
    piramide_br = calcular_dados_piramide(df_brasil)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plotar_piramide(piramide_pr, "Paraná (PR)"), use_container_width=True)
    with col2:
        st.plotly_chart(plotar_piramide(piramide_br, "Brasil Médio"), use_container_width=True)