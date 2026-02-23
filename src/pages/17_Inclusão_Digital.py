import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import carregar_dados
from utils.dicionarios import mapa_internet

st.set_page_config(page_title="Inclusão Digital", page_icon="🌐", layout="wide")

df_brasil = carregar_dados()

if df_brasil is not None:
    # Filtrando Paraná e preparando colunas
    df_pr = df_brasil[df_brasil['SG_UF_PROVA'] == 'PR'].copy()
    provas = {
        'NU_NOTA_CN': 'C. Natureza',
        'NU_NOTA_CH': 'C. Humanas',
        'NU_NOTA_LC': 'Linguagens',
        'NU_NOTA_MT': 'Matemática',
        'NU_NOTA_REDACAO': 'Redação'
    }

    # Criando coluna de Localidade (Capital vs Interior)
    df_pr['Localidade'] = df_pr['NO_MUNICIPIO_PROVA'].apply(
        lambda x: 'Capital' if x.upper() == 'CURITIBA' else 'Interior'
    )

    st.header("17. Inclusão Digital e Desempenho Regional")
    st.write("Como a falta de internet impacta as notas e se esse impacto varia entre Curitiba e o restante do estado.")

    # ==========================================
    # 1. IMPACTO POR ÁREA DE CONHECIMENTO
    # ==========================================
    st.subheader("Desempenho por Área: Com vs. Sem Internet")
    
    # Calculando médias por Q025
    df_areas = df_pr.groupby('Q025')[list(provas.keys())].mean().rename(index=mapa_internet).reset_index()
    df_areas_melt = df_areas.melt(id_vars='Q025', var_name='Prova', value_name='Nota')
    df_areas_melt['Prova'] = df_areas_melt['Prova'].map(provas)

    fig_bar = px.bar(
        df_areas_melt, x='Prova', y='Nota', color='Q025',
        barmode='group', text_auto='.0f',
        title="Impacto da Internet em cada Disciplina",
        labels={'Q025': 'Acesso à Internet'},
        color_discrete_map={'Com Internet': '#1f77b4', 'Sem Internet': '#d62728'}
    )
    fig_bar.update_layout(yaxis=dict(range=[350, 650]))
    st.plotly_chart(fig_bar, use_container_width=True)

    # ==========================================
    # 2. COMPARATIVO CAPITAL VS INTERIOR
    # ==========================================
    st.markdown("---")
    st.subheader("O 'Gap Digital': Capital vs. Interior")

    # Calculando a média geral para simplificar o gap
    df_pr['MEDIA_GERAL'] = df_pr[list(provas.keys())].mean(axis=1)
    
    # Agrupando para calcular o gap
    gap_data = df_pr.groupby(['Localidade', 'Q025'])['MEDIA_GERAL'].mean().unstack()
    gap_data['Gap'] = gap_data['B'] - gap_data['A']
    gap_data = gap_data.reset_index()

    c1, c2 = st.columns(2)
    
    with c1:
        fig_gap = px.bar(
            gap_data, x='Localidade', y='Gap',
            text_auto='.1f',
            title="Diferença de Pontos (Com Internet - Sem Internet)",
            labels={'Gap': 'Tamanho do Gap (Pontos)'},
            color='Localidade',
            color_discrete_map={'Capital': '#2ca02c', 'Interior': '#9467bd'}
        )
        st.plotly_chart(fig_gap, use_container_width=True)

    with c2:
        st.write("#### Análise do Gap")
        gap_cap = gap_data[gap_data['Localidade'] == 'Capital']['Gap'].values[0]
        gap_int = gap_data[gap_data['Localidade'] == 'Interior']['Gap'].values[0]
        
        st.metric("Penalização na Capital", f"{gap_cap:.1f} pts")
        st.metric("Penalização no Interior", f"{gap_int:.1f} pts", 
                  delta=f"{gap_int - gap_cap:.1f} pts de diferença", delta_color="inverse")

    st.info(f"""
    **Conclusão:** - No Paraná, a área mais afetada pela falta de internet costuma ser **{'Matemática' if df_areas_melt[df_areas_melt['Q025'] == 'Sem Internet'].sort_values('Nota').iloc[0]['Prova'] == 'Matemática' else 'Redação'}**, onde o acesso a materiais extras é vital.
    - O impacto é **{'maior no Interior' if gap_int > gap_cap else 'maior na Capital'}**, sugerindo que a infraestrutura urbana/escolar da capital {'ajuda a compensar' if gap_int > gap_cap else 'não é suficiente para compensar'} a falta de conexão individual do aluno.
    """)