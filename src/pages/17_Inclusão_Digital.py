import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import carregar_dados_projeto

st.set_page_config(page_title="Inclusão Digital", page_icon="🌐", layout="wide")

df_pr, _, _ = carregar_dados_projeto()

if df_pr is not None:
    provas = {
        'NU_NOTA_CN': 'C. Natureza',
        'NU_NOTA_CH': 'C. Humanas',
        'NU_NOTA_LC': 'Linguagens',
        'NU_NOTA_MT': 'Matemática',
        'NU_NOTA_REDACAO': 'Redação'
    }

    df_pr['Localidade'] = df_pr['NO_MUNICIPIO_PROVA'].apply(
        lambda x: 'Capital' if str(x).upper().strip() == 'CURITIBA' else 'Interior'
    )

    st.header("17. Inclusão Digital e Desempenho Regional")
    st.write("Análise do impacto do acesso à internet nas notas e a variação desse 'Gap Digital' entre Curitiba e o interior.")

    st.subheader("Desempenho por Área: Com vs. Sem Internet")
    
    df_areas = df_pr.groupby('Q025_LABEL', observed=True)[list(provas.keys())].mean().reset_index()
    df_areas_melt = df_areas.melt(id_vars='Q025_LABEL', var_name='Prova', value_name='Nota')
    df_areas_melt['Prova'] = df_areas_melt['Prova'].map(provas)

    fig_bar = px.bar(
        df_areas_melt, x='Prova', y='Nota', color='Q025_LABEL',
        barmode='group', text_auto='.0f',
        title="Impacto do Acesso à Internet no Desempenho por Disciplina (PR)",
        labels={'Q025_LABEL': 'Acesso à Internet', 'Nota': 'Nota Média'},
        color_discrete_map={'Com Internet': '#1f77b4', 'Sem Internet': '#d62728'}
    )
    fig_bar.update_layout(yaxis=dict(range=[350, 650]), height=450)
    st.plotly_chart(fig_bar, use_container_width=True)

    

    st.markdown("---")
    st.subheader("O 'Gap Digital': Capital vs. Interior")

    gap_data = df_pr.groupby(['Localidade', 'Q025_LABEL'], observed=True)['MEDIA_GERAL'].mean().unstack()
    
    if 'Com Internet' in gap_data.columns and 'Sem Internet' in gap_data.columns:
        gap_data['Gap'] = gap_data['Com Internet'] - gap_data['Sem Internet']
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
            fig_gap.update_layout(height=400)
            st.plotly_chart(fig_gap, use_container_width=True)

        with c2:
            st.write("#### Penalização por Falta de Acesso")
            gap_cap = gap_data[gap_data['Localidade'] == 'Capital']['Gap'].values[0]
            gap_int = gap_data[gap_data['Localidade'] == 'Interior']['Gap'].values[0]
            
            st.metric("Redução na Capital", f"-{gap_cap:.1f} pts")
            st.metric("Redução no Interior", f"-{gap_int:.1f} pts", 
                      delta=f"{gap_int - gap_cap:.1f} pts de diferença", delta_color="inverse")

        area_mais_afetada = df_areas_melt[df_areas_melt['Q025_LABEL'] == 'Sem Internet'].sort_values('Nota').iloc[0]['Prova']
        maior_impacto_local = 'Interior' if gap_int > gap_cap else 'Capital'

        st.info(f"""
        **Conclusão Técnica:**
        - No Paraná, a disciplina que registra a menor média entre os sem internet é **{area_mais_afetada}**.
        - O impacto da exclusão digital é **{maior_impacto_local.lower()}**, indicando que, {'mesmo com infraestrutura urbana, a falta de rede privada' if gap_cap > gap_int else 'a infraestrutura do interior'} acentua a barreira de aprendizado.
        - Este dado é crucial para políticas de **Universalização da Banda Larga** escolar e domiciliar.
        """)
    else:
        st.warning("Dados insuficientes para calcular o Gap Digital (ausência de uma das categorias).")