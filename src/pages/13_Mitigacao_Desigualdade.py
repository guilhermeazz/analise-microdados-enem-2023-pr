import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_loader import carregar_dados_projeto

st.set_page_config(page_title="Mitigação de Desigualdade", page_icon="⚖️", layout="wide")

df_pr, df_br, _ = carregar_dados_projeto()

if df_pr is not None and df_br is not None:
    st.header("13. Mitigação de Desigualdade Socioeconômica")
    st.write("O Paraná é mais eficiente que o Brasil em reduzir a distância entre extremos de renda no ENEM?")

    def calcular_gap_extremos(df):
        media_baixa = df[df['Q006'] == 'A']['MEDIA_GERAL'].mean()
        media_alta = df[df['Q006'] == 'Q']['MEDIA_GERAL'].mean()
        return media_alta - media_baixa, media_baixa, media_alta

    gap_pr, min_pr, max_pr = calcular_gap_extremos(df_pr)
    gap_br, min_br, max_br = calcular_gap_extremos(df_br)

    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.metric("Gap de Desigualdade (PR)", f"{gap_pr:.2f} pts")
    
    with c2:
        diff_gap = gap_pr - gap_br
        st.metric("Gap de Desigualdade (Brasil Excl. PR)", f"{gap_br:.2f} pts", 
                  delta=f"{diff_gap:.2f} pts", delta_color="inverse")

    with c3:
        equidade_pr = (min_pr / max_pr) * 100
        st.metric("Índice de Equidade (PR)", f"{equidade_pr:.1f}%")

    st.markdown("---")

    

    st.subheader("Curva de Desigualdade: PR vs Brasil")
    
    def preparar_curva(df):
        return df.groupby('Q006', observed=True)['MEDIA_GERAL'].mean().reset_index()

    curva_pr = preparar_curva(df_pr)
    curva_br = preparar_curva(df_br)

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=curva_br['Q006'], y=curva_br['MEDIA_GERAL'],
                             mode='lines+markers', name='Brasil (Excl. PR)',
                             line=dict(color='#7f7f7f', width=2, dash='dot'),
                             hovertemplate='Brasil: %{y:.2f}'))

    fig.add_trace(go.Scatter(x=curva_pr['Q006'], y=curva_pr['MEDIA_GERAL'],
                             mode='lines+markers', name='Paraná',
                             line=dict(color='#1f77b4', width=4),
                             hovertemplate='Paraná: %{y:.2f}'))

    fig.update_layout(
        title="Impacto da Renda na Nota Média Geral",
        xaxis_title="Faixa de Renda (A: Sem Renda -> Q: Acima de 24k)",
        yaxis_title="Média Geral",
        hovermode="x unified",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    if gap_pr < gap_br:
        st.success(f"✅ **Veredito:** O Paraná mitiga a desigualdade **melhor** que a média nacional. O gap entre os extremos no estado é {abs(diff_gap):.2f} pontos menor que no Brasil.")
    else:
        st.warning(f"⚠️ **Veredito:** A desigualdade socioeconômica no Paraná é **mais acentuada** que na média nacional. O gap entre os extremos é {diff_gap:.2f} pontos maior.")

    st.info("""
    **Análise Técnica:**
    O **Índice de Equidade** indica o quanto a base da pirâmide (Classe A) consegue performar em relação ao topo (Classe Q). 
    Quanto mais próximo de 100%, mais 'imune' ao fator financeiro é o sistema educacional do estado.
    """)