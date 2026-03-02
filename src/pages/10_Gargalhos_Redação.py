import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_loader import carregar_dados_projeto

st.set_page_config(page_title="Gargalos da Redação", page_icon="✍️", layout="wide")

df_pr, df_br, _ = carregar_dados_projeto()

if df_pr is not None and df_br is not None:
    df_pr_red = df_pr[df_pr['NU_NOTA_REDACAO'] > 0].copy()
    df_br_red = df_br[df_br['NU_NOTA_REDACAO'] > 0].copy()

    st.header("10. Análise das 5 Competências da Redação")
    st.write("Comparativo detalhado entre o Paraná e a média nacional nas competências específicas avaliadas pelo INEP.")

    competencias = {
        'NU_NOTA_COMP1': 'Norma Culta',
        'NU_NOTA_COMP2': 'Tema/Estrutura',
        'NU_NOTA_COMP3': 'Argumentação',
        'NU_NOTA_COMP4': 'Coesão',
        'NU_NOTA_COMP5': 'Intervenção'
    }

    medias_pr = df_pr_red[list(competencias.keys())].mean().values
    medias_br = df_br_red[list(competencias.keys())].mean().values
    
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
        name='Brasil (Excl. PR)',
        fillcolor='rgba(127, 127, 127, 0.2)',
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
                range=[110, 160],
                dtick=10,
                gridcolor='rgba(0,0,0,0.1)',
                angle=90,
                tickangle=90
            ),
            bgcolor="white"
        ),
        showlegend=True,
        title="Diferenças de Desempenho (Foco: 110 - 160 pontos)",
        height=600
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
        st.success(f"🌟 **Destaque do PR:** {ponto_forte['Competência']}")
        st.write(f"Superioridade de **{ponto_forte['Diferença']:.2f}** pontos sobre o Brasil.")

    with col2:
        st.error(f"⚠️ **Menor Vantagem:** {gargalo['Competência']}")
        st.write(f"Vantagem de apenas **{gargalo['Diferença']:.2f}** pontos.")

    st.markdown("---")
    st.dataframe(df_diff.style.format(precision=2), use_container_width=True)

    st.info("""
    **Interpretação:** O gráfico de radar (aranha) permite visualizar o equilíbrio entre as competências. 
    Uma forma mais 'esticada' indica especialização, enquanto uma forma regular indica equilíbrio pedagógico. 
    A escala foi ajustada entre 110 e 160 para evidenciar onde as linhas se distanciam.
    """)