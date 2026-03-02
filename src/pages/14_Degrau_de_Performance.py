import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import carregar_dados_projeto

st.set_page_config(page_title="Degrau de Performance", page_icon="🪜", layout="wide")

# 1. Carregamento: Pegamos o df_pr (Paraná filtrado para performance)
df_pr, _, _ = carregar_dados_projeto()

if df_pr is not None:
    st.header("14. O 'Degrau' de Performance por Renda")
    st.write("Em qual transição de faixa de renda ocorre o maior salto de nota média no Paraná?")

    # 2. Processamento do Gradiente de Notas
    # Q006 é o código (A, B, C...) que garante a ordenação correta
    df_gradiente = df_pr.groupby(['Q006', 'Q006_LABEL'], observed=True)['MEDIA_GERAL'].mean().reset_index()
    df_gradiente = df_gradiente.sort_values('Q006')

    # Cálculo do 'Salto' (Diferença entre a faixa atual e a anterior)
    df_gradiente['SALTO'] = df_gradiente['MEDIA_GERAL'].diff()
    
    # Criação da label de transição para o gráfico
    df_gradiente['TRANSICAO'] = df_gradiente['Q006'].shift(1).astype(str) + " ➔ " + df_gradiente['Q006'].astype(str)
    
    # Identificação do maior salto estatístico
    maior_salto_idx = df_gradiente['SALTO'].idxmax()
    maior_salto_row = df_gradiente.loc[maior_salto_idx]
    
    col1, col2 = st.columns([2, 1])

    with col1:
        # Gráfico de Barras: Intensidade da Mudança
        fig_bar = px.bar(
            df_gradiente.dropna(), 
            x='TRANSICAO', 
            y='SALTO',
            title="Intensidade do Salto de Performance entre Faixas de Renda",
            labels={'SALTO': 'Aumento na Média (pts)', 'TRANSICAO': 'Mudança de Faixa'},
            color='SALTO',
            color_continuous_scale='Blues'
        )
        fig_bar.update_layout(height=450)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # Métricas de Destaque para o Slide
        st.subheader("O Maior Degrau")
        st.metric("Salto Máximo", f"+{maior_salto_row['SALTO']:.2f} pts")
        st.write(f"**Transição:** {maior_salto_row['TRANSICAO']}")
        
        # Labels descritivas (vindas do pipeline)
        f_origem_label = df_gradiente.loc[maior_salto_idx - 1, 'Q006_LABEL']
        f_destino_label = maior_salto_row['Q006_LABEL']
        
        st.info(f"**De:** {f_origem_label}")
        st.success(f"**Para:** {f_destino_label}")

    st.markdown("---")

    

    st.subheader("Evolução Absoluta das Notas")
    # Gráfico de Área: Curva de Acúmulo
    fig_evol = px.area(
        df_gradiente, x='Q006', y='MEDIA_GERAL',
        title="Curva de Acúmulo de Performance (Crescimento de Notas)",
        labels={'MEDIA_GERAL': 'Nota Média', 'Q006': 'Faixa de Renda (Código)'},
        markers=True
    )
    
    # Anotação no ponto de maior ruptura
    fig_evol.add_annotation(
        x=maior_salto_row['Q006'], y=maior_salto_row['MEDIA_GERAL'],
        text="Ruptura de Performance 🚀", showarrow=True, arrowhead=1,
        bgcolor="rgba(255, 255, 255, 0.8)"
    )
    fig_evol.update_layout(yaxis=dict(range=[400, 700]), height=450)
    st.plotly_chart(fig_evol, use_container_width=True)

    st.info(f"""
    **Insight para a Banca:**
    - O maior degrau, identificado na transição **{maior_salto_row['TRANSICAO']}**, representa o ponto de maior ruptura socioeducacional. 
    - Estatisticamente, este salto de **{maior_salto_row['SALTO']:.2f} pontos** sugere onde o acesso a diferenciais (como cursinhos privados ou maior tempo livre) impacta decisivamente o resultado médio.
    """)