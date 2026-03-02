import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import carregar_dados_projeto

st.set_page_config(page_title="Variabilidade das Notas", page_icon="📊", layout="wide")

df_pr, df_br, _ = carregar_dados_projeto()

if df_pr is not None and df_br is not None:
    st.header("7. Variabilidade das Notas (Dispersão)")
    st.write("Qual área do conhecimento apresenta a maior dispersão no Paraná e como ela se compara ao restante do Brasil?")

    provas = {
        'NU_NOTA_CN': 'Ciências Natureza',
        'NU_NOTA_CH': 'Ciências Humanas',
        'NU_NOTA_LC': 'Linguagens e Códigos',
        'NU_NOTA_MT': 'Matemática',
        'NU_NOTA_REDACAO': 'Redação'
    }

    stats_pr = df_pr[list(provas.keys())].std().rename(index=provas)
    stats_br = df_br[list(provas.keys())].std().rename(index=provas)

    df_sigma = pd.DataFrame({
        'Área': stats_pr.index,
        'Desvio Padrão PR': stats_pr.values,
        'Desvio Padrão Brasil': stats_br.values
    })
    
    df_sigma['Diferença (%)'] = ((df_sigma['Desvio Padrão PR'] / df_sigma['Desvio Padrão Brasil']) - 1) * 100

    col1, col2 = st.columns([2, 1])

    with col1:
        df_plot = df_sigma.melt(id_vars='Área', value_vars=['Desvio Padrão PR', 'Desvio Padrão Brasil'], 
                                var_name='Localidade', value_name='Sigma')
        
        fig_sigma = px.bar(
            df_plot, x='Área', y='Sigma', color='Localidade', barmode='group',
            title="Comparativo de Desvio Padrão (Foco em Dispersão)",
            color_discrete_map={'Desvio Padrão PR': '#1f77b4', 'Desvio Padrão Brasil': '#7f7f7f'},
            text_auto='.1f'
        )
        st.plotly_chart(fig_sigma, use_container_width=True)

    with col2:
        st.subheader("Consistência Relativa")
        for _, row in df_sigma.iterrows():
            label = "Mais consistente" if row['Diferença (%)'] < 0 else "Menos consistente"
            st.write(f"**{row['Área']}**")
            st.caption(f"PR é {abs(row['Diferença (%)']):.2f}% {label} que o BR")

    st.markdown("---")
    st.subheader("Distribuição Detalhada (Boxplot)")
    
    area_selecionada = st.selectbox("Selecione uma área para ver a distribuição:", list(provas.values()))
    cod_coluna = [k for k, v in provas.items() if v == area_selecionada][0]

    df_box_pr = df_pr[[cod_coluna]].dropna()
    df_box_pr['Local'] = 'Paraná'
    df_box_br = df_br[[cod_coluna]].dropna()
    df_box_br['Local'] = 'Resto do Brasil'
    
    df_box_total = pd.concat([df_box_pr, df_box_br])

    fig_box = px.box(
        df_box_total, x='Local', y=cod_coluna, color='Local',
        title=f"Distribuição de Notas: {area_selecionada}",
        color_discrete_map={'Paraná': '#1f77b4', 'Resto do Brasil': '#7f7f7f'},
        points=False 
    )
    st.plotly_chart(fig_box, use_container_width=True)

    maior_sigma_area = df_sigma.loc[df_sigma['Desvio Padrão PR'].idxmax(), 'Área']
    maior_sigma_val = df_sigma['Desvio Padrão PR'].max()

    st.success(f"💡 **Conclusão:** A área com maior dispersão no Paraná é **{maior_sigma_area}** ($\sigma$ = {maior_sigma_val:.2f}).")
    
    st.info("""
    **O que isso significa?**
    - Um desvio padrão elevado indica desigualdade educacional acentuada: há alunos dominando a matéria e outros com dificuldades básicas.
    - Se o Paraná possui um $\sigma$ menor que o Brasil, o ensino no estado é mais homogêneo.
    """)