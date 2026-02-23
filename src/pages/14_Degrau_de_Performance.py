import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import carregar_dados
from utils.dicionarios import mapa_renda

st.set_page_config(page_title="Degrau de Performance", page_icon="🪜", layout="wide")

df_brasil = carregar_dados()

if df_brasil is not None:
    provas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    df_brasil['MEDIA_GERAL'] = df_brasil[provas].mean(axis=1)
    df_pr = df_brasil[df_brasil['SG_UF_PROVA'] == 'PR'].dropna(subset=['Q006', 'MEDIA_GERAL']).copy()

    st.header("14. O 'Degrau' de Performance por Renda")
    st.write("Em qual transição de faixa de renda ocorre o maior salto de nota média no Paraná?")

    df_gradiente = df_pr.groupby('Q006')['MEDIA_GERAL'].mean().reset_index()
    ordem_renda = sorted(df_gradiente['Q006'].unique())
    df_gradiente['Q006'] = pd.Categorical(df_gradiente['Q006'], categories=ordem_renda, ordered=True)
    df_gradiente = df_gradiente.sort_values('Q006')

    df_gradiente['SALTO'] = df_gradiente['MEDIA_GERAL'].diff()
    
    df_gradiente['TRANSICAO'] = df_gradiente['Q006'].shift(1).astype(str) + " ➔ " + df_gradiente['Q006'].astype(str)
    
    maior_salto_idx = df_gradiente['SALTO'].idxmax()
    maior_salto_row = df_gradiente.loc[maior_salto_idx]
    
    col1, col2 = st.columns([2, 1])

    with col1:
        fig_bar = px.bar(
            df_gradiente.dropna(), 
            x='TRANSICAO', 
            y='SALTO',
            title="Intensidade do Salto de Performance entre Faixas de Renda",
            labels={'SALTO': 'Aumento na Média (pts)', 'TRANSICAO': 'Mudança de Faixa'},
            color='SALTO',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("O Maior Degrau")
        st.metric("Salto Máximo", f"+{maior_salto_row['SALTO']:.2f} pts")
        st.write(f"**Transição:** {maior_salto_row['TRANSICAO']}")
        
        f_origem = maior_salto_row['TRANSICAO'].split(" ➔ ")[0]
        f_destino = maior_salto_row['TRANSICAO'].split(" ➔ ")[1]
        
        st.caption(f"De: {mapa_renda.get(f_origem)}")
        st.caption(f"Para: {mapa_renda.get(f_destino)}")

    st.markdown("---")

    st.subheader("Evolução Absoluta das Notas")
    fig_evol = px.area(
        df_gradiente, x='Q006', y='MEDIA_GERAL',
        title="Curva de Acúmulo de Performance",
        labels={'MEDIA_GERAL': 'Nota Média', 'Q006': 'Faixa de Renda'},
        markers=True
    )
    fig_evol.add_annotation(
        x=maior_salto_row['Q006'], y=maior_salto_row['MEDIA_GERAL'],
        text="Maior Salto 🚀", showarrow=True, arrowhead=1
    )
    st.plotly_chart(fig_evol, use_container_width=True)

    st.info("""
    **O que isso indica?**
    O maior degrau geralmente marca a transição entre classes sociais onde o acesso a recursos 
    pedagógicos extras (cursinhos, livros, tempo de estudo) se torna viável, 
    causando uma ruptura no padrão de notas.
    """)