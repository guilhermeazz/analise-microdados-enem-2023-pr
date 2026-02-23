import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_loader import carregar_dados

st.set_page_config(page_title="Gargalos da Redação", page_icon="✍️", layout="wide")

df_brasil = carregar_dados()

if df_brasil is not None:
    df_redacao = df_brasil[df_brasil['NU_NOTA_REDACAO'] > 0].copy()
    
    df_pr = df_redacao[df_redacao['SG_UF_PROVA'] == 'PR']
    df_br = df_redacao[df_redacao['SG_UF_PROVA'] != 'PR']

    st.header("10. Análise das 5 Competências da Redação")
    st.write("Comparativo detalhado: Escala ajustada para evidenciar disparidades sem distorcer a percepção de nota zero.")

    competencias = {
        'NU_NOTA_COMP1': 'Domínio da Norma Culta',
        'NU_NOTA_COMP2': 'Compreensão do Tema',
        'NU_NOTA_COMP3': 'Organização das Ideias',
        'NU_NOTA_COMP4': 'Mecanismos Coesivos',
        'NU_NOTA_COMP5': 'Proposta de Intervenção'
    }

    medias_pr = df_pr[list(competencias.keys())].mean().values
    medias_br = df_br[list(competencias.keys())].mean().values
    
    labels = list(competencias.values())
    labels.append(labels[0])

    r_pr = list(medias_pr)
    r_pr.append(r_pr[0])

    r_br = list(medias_br)
    r_br.append(r_br[0])

    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=r_br,
        theta=labels,
        fill='toself',
        name='Brasil',
        fillcolor='rgba(127, 127, 127, 0.3)',
        line=dict(color='#7f7f7f', width=2),
        marker=dict(symbol='circle', size=7),
        hovertemplate='%{theta}: %{r:.2f}'
    ))

    fig_radar.add_trace(go.Scatterpolar(
        r=r_pr,
        theta=labels,
        fill='toself',
        name='Paraná',
        fillcolor='rgba(31, 119, 180, 0.4)',
        line_color='#1f77b4',
        marker=dict(symbol='square', size=7),
        hovertemplate='%{theta}: %{r:.2f}'
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[80, 170],
                dtick=15,
                gridcolor='rgba(0,0,0,0.1)',
                angle=90,
                tickangle=90
            ),
            bgcolor="white"
        ),
        showlegend=True,
        title="Diferenças de Desempenho (Escala de Destaque: 80 - 170)",
        height=650
    )

    st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")

    df_diff = pd.DataFrame({
        'Competência': list(competencias.values()),
        'Média PR': medias_pr,
        'Média Brasil': medias_br
    })
    df_diff['Diferença'] = df_diff['Média PR'] - df_diff['Média Brasil']
    df_diff = df_diff.sort_values(by='Diferença', ascending=False)

    col1, col2 = st.columns(2)
    ponto_forte = df_diff.iloc[0]
    gargalo = df_diff.iloc[-1]

    with col1:
        st.success(f"🌟 **Ponto Forte:** {ponto_forte['Competência']}")
        st.write(f"Vantagem de **{ponto_forte['Diferença']:.2f}** pontos.")

    with col2:
        st.error(f"⚠️ **Gargalo Relativo:** {gargalo['Competência']}")
        st.write(f"Vantagem de apenas **{gargalo['Diferença']:.2f}** pontos.")

    st.markdown("---")
    st.dataframe(df_diff.style.format(precision=2), use_container_width=True)