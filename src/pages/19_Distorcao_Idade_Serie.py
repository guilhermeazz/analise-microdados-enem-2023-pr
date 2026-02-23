import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import carregar_dados

st.set_page_config(page_title="Distorção Idade-Série", page_icon="⏳", layout="wide")

df_brasil = carregar_dados()

if df_brasil is not None:
    df_concluintes = df_brasil[df_brasil['TP_ST_CONCLUSAO'] == 2].copy()
    
    df_concluintes['Status_Idade'] = df_concluintes['TP_FAIXA_ETARIA'].apply(
        lambda x: 'Idade Ideal (≤18)' if x <= 3 else 'Atraso Escolar (19+)'
    )
    
    provas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    df_concluintes['MEDIA_GERAL'] = df_concluintes[provas].mean(axis=1)

    df_pr = df_concluintes[df_concluintes['SG_UF_PROVA'] == 'PR']
    df_br = df_concluintes[df_concluintes['SG_UF_PROVA'] != 'PR']

    st.header("19. Distorção Idade-Série no Paraná")
    st.write("Análise do impacto do atraso escolar no desempenho dos alunos que concluem o Ensino Médio.")

    def calc_gap(df):
        medias = df.groupby('Status_Idade')['MEDIA_GERAL'].mean()
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
    
    df_plot = pd.concat([
        df_pr.assign(Local='Paraná'),
        df_br.assign(Local='Brasil')
    ])

    fig_box = px.box(
        df_plot, x='Status_Idade', y='MEDIA_GERAL', color='Local',
        title="Comparativo de Dispersão de Notas",
        color_discrete_map={'Paraná': '#1f77b4', 'Brasil': '#7f7f7f'}
    )
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")
    st.subheader("Percentual de Concluintes em Atraso")
    
    dist_pr = df_pr['Status_Idade'].value_counts(normalize=True) * 100
    dist_br = df_br['Status_Idade'].value_counts(normalize=True) * 100
    
    col_a, col_b = st.columns(2)
    col_a.write(f"**Paraná:** {dist_pr.get('Atraso Escolar (19+)', 0):.1f}% dos concluintes estão fora da idade ideal.")
    col_b.write(f"**Brasil:** {dist_br.get('Atraso Escolar (19+)', 0):.1f}% dos concluintes estão fora da idade ideal.")

    st.info(f"""
    **Conclusão da Análise:** - No Paraná, o atraso escolar gera uma perda de **{gap_pr:.2f} pontos**. 
    - Comparado ao Brasil, esse impacto é **{'mais' if gap_pr > gap_br else 'menos'}** severo.
    - O atraso escolar é um forte indicador de interrupções na trajetória de aprendizagem, o que reflete diretamente na base de conhecimentos necessária para o ENEM.
    """)