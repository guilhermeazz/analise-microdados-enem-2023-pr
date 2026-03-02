import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import carregar_dados_projeto

st.set_page_config(page_title="Distorção Idade-Série", page_icon="⏳", layout="wide")

# 1. Carregamento: df_pr (Paraná) e df_br (Brasil SEM o Paraná)
# Utilizamos a ramificação de performance (já limpa de faltantes)
df_pr_all, df_br_all, _ = carregar_dados_projeto()

if df_pr_all is not None:
    
    # 2. Filtro de Concluintes (TP_ST_CONCLUSAO == 2: Conclui em 2023)
    # Analisamos a distorção apenas em quem deveria estar terminando o ciclo regular
    df_pr = df_pr_all[df_pr_all['TP_ST_CONCLUSAO'] == 2].copy()
    df_br = df_br_all[df_br_all['TP_ST_CONCLUSAO'] == 2].copy()

    # 3. Categorização da Distorção
    # No ENEM: 1 (<17), 2 (17), 3 (18). Acima disso considera-se atraso para o Ensino Médio.
    def categorizar_idade(x):
        return 'Idade Ideal (≤18)' if x <= 3 else 'Atraso Escolar (19+)'

    df_pr['Status_Idade'] = df_pr['TP_FAIXA_ETARIA'].apply(categorizar_idade)
    df_br['Status_Idade'] = df_br['TP_FAIXA_ETARIA'].apply(categorizar_idade)

    st.header("19. Distorção Idade-Série no Paraná")
    st.write("Análise do impacto do atraso escolar no desempenho dos alunos concluintes em 2023.")

    # 4. Cálculo de Gaps de Performance
    def calc_gap(df):
        medias = df.groupby('Status_Idade', observed=True)['MEDIA_GERAL'].mean()
        return medias.get('Idade Ideal (≤18)', 0), medias.get('Atraso Escolar (19+)', 0)

    ideal_pr, atraso_pr = calc_gap(df_pr)
    ideal_br, atraso_br = calc_gap(df_br)
    
    gap_pr = ideal_pr - atraso_pr
    gap_br = ideal_br - atraso_br

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Média Idade Ideal (PR)", f"{ideal_pr:.2f}")
    with c2:
        st.metric("Média com Atraso (PR)", f"{atraso_pr:.2f}")
    with c3:
        st.metric("Penalização do Atraso (Gap)", f"-{gap_pr:.2f} pts", 
                  delta=f"{gap_pr - gap_br:.2f} vs Brasil", delta_color="inverse")

    st.markdown("---")

    

    st.subheader("Distribuição das Notas: Ideal vs. Atraso")
    
    # Preparação de dados para o Boxplot
    df_plot_pr = df_pr[['Status_Idade', 'MEDIA_GERAL']].copy()
    df_plot_pr['Local'] = 'Paraná'
    
    df_plot_br = df_br[['Status_Idade', 'MEDIA_GERAL']].copy()
    df_plot_br['Local'] = 'Brasil (Excl. PR)'
    
    df_plot = pd.concat([df_plot_pr, df_plot_br])

    fig_box = px.box(
        df_plot, x='Status_Idade', y='MEDIA_GERAL', color='Local',
        title="Impacto do Atraso Escolar na Dispersão de Notas",
        labels={'MEDIA_GERAL': 'Média Geral', 'Status_Idade': 'Perfil do Aluno'},
        color_discrete_map={'Paraná': '#1f77b4', 'Brasil (Excl. PR)': '#7f7f7f'},
        points=False # Otimização de performance
    )
    fig_box.update_layout(height=500)
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")
    st.subheader("Percentual de Concluintes em Atraso")
    
    dist_pr = df_pr['Status_Idade'].value_counts(normalize=True) * 100
    dist_br = df_br['Status_Idade'].value_counts(normalize=True) * 100
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write(f"**Paraná:**")
        st.info(f"{dist_pr.get('Atraso Escolar (19+)', 0):.1f}% dos concluintes estão em atraso.")
    with col_b:
        st.write(f"**Brasil (Excl. PR):**")
        st.warning(f"{dist_br.get('Atraso Escolar (19+)', 0):.1f}% dos concluintes estão em atraso.")

    st.info(f"""
    **Análise Técnica:**
    - A distorção idade-série no Paraná resulta em um decréscimo de **{gap_pr:.2f} pontos** na média geral em relação aos alunos na idade ideal.
    - Este fenômeno indica que interrupções na trajetória escolar ou reprovações acumuladas impactam severamente a competitividade do candidato.
    - O Boxplot revela que, além da média ser menor, a variabilidade (dispersão) entre os alunos em atraso tende a ser diferente, refletindo trajetórias de vida mais heterogêneas.
    """)