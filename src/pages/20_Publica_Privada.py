import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import carregar_dados
from utils.dicionarios import mapa_escola

st.set_page_config(page_title="Abismo Público-Privado", page_icon="🏫", layout="wide")

df_brasil = carregar_dados()

if df_brasil is not None:
    provas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    df_brasil['MEDIA_GERAL'] = df_brasil[provas].mean(axis=1)
    
    df_analise = df_brasil[df_brasil['TP_ESCOLA'].isin([2, 3])].copy()
    df_analise['Tipo_Escola'] = df_analise['TP_ESCOLA'].map(mapa_escola)
    
    df_pr = df_analise[df_analise['SG_UF_PROVA'] == 'PR']
    df_br = df_analise[df_analise['SG_UF_PROVA'] != 'PR']

    st.header("20. O Abismo Público-Privado")
    st.write("Comparativo de desempenho entre as redes de ensino no Paraná vs. Brasil.")

    def calc_gap_escola(df):
        medias = df.groupby('Tipo_Escola')['MEDIA_GERAL'].mean()
        return medias.get('Pública', 0), medias.get('Privada', 0)

    pub_pr, priv_pr = calc_gap_escola(df_pr)
    pub_br, priv_br = calc_gap_escola(df_br)
    
    gap_pr = priv_pr - pub_pr
    gap_br = priv_br - pub_br

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Média Escola Pública (PR)", f"{pub_pr:.2f}")
    with c2:
        st.metric("Média Escola Privada (PR)", f"{priv_pr:.2f}")
    with c3:
        st.metric("Tamanho do Abismo (Gap)", f"{gap_pr:.2f} pts", 
                  delta=f"{gap_pr - gap_br:.2f} vs Brasil", delta_color="inverse")

    st.markdown("---")

    st.subheader("Distribuição das Notas: Onde os grupos se cruzam?")
    
    fig_box = px.box(
        df_pr, x='Tipo_Escola', y='MEDIA_GERAL', color='Tipo_Escola',
        title="Dispersão de Notas no Paraná por Tipo de Escola",
        color_discrete_map={'Pública': '#ef553b', 'Privada': '#636efa'}
    )
    fig_box.add_hline(y=priv_pr, line_dash="dot", line_color="blue", 
                      annotation_text="Média da Privada")
    
    st.plotly_chart(fig_box, use_container_width=True)

    st.markdown("---")
    st.subheader("O Desafio da Ascensão")
    
    top_10_pub = df_pr[df_pr['Tipo_Escola'] == 'Pública']['MEDIA_GERAL'].quantile(0.90)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.write(f"**Performance de Elite:** Somente os 10% melhores alunos da escola pública no PR (Top 10%) superam a nota **{top_10_pub:.1f}**.")
    with col_b:
        porcentagem_supera = (df_pr[df_pr['Tipo_Escola'] == 'Pública']['MEDIA_GERAL'] > priv_pr).mean() * 100
        st.write(f"**Conclusão:** Apenas **{porcentagem_supera:.1f}%** dos alunos da rede pública conseguem tirar uma nota maior que a **média** da rede privada.")

    st.info("""
    **Interpretação:** O gráfico de caixa (boxplot) mostra que a base da escola privada muitas vezes começa onde o topo da escola pública termina. 
    Este gap reflete não apenas o ensino, mas todo o acúmulo de capital cultural e recursos socioeconômicos vistos nas páginas anteriores.
    """)