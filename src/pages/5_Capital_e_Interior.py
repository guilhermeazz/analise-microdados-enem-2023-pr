import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_loader import carregar_dados

st.set_page_config(page_title="Capital vs Interior", page_icon="🏙️", layout="wide")

df_brasil = carregar_dados()

if df_brasil is not None:
    df_parana = df_brasil[df_brasil['SG_UF_PROVA'] == 'PR'].copy()

    st.header("5. Disparidade: Capital vs. Polos Regionais vs. Interior")
    
    st.info("""
    **Nota Metodológica:** Os polos regionais analisados nesta página foram selecionados com base na divisão 
    das **Mesorregiões do Estado do Paraná (IBGE 2017)**. Essa classificação agrupa os municípios 
    em torno de centros urbanos de influência econômica, social e administrativa.
    """)

    polos_regionais = ['LONDRINA', 'MARINGA', 'MARINGÁ', 'PONTA GROSSA', 'GUARAPUAVA', 'CASCAVEL']
    
    def categorizar_municipio(mun):
        mun = str(mun).upper().strip()
        if mun == 'CURITIBA':
            return 'Capital (Curitiba)'
        elif mun in polos_regionais:
            return 'Polos Regionais'
        else:
            return 'Interior (Demais)'

    df_parana['CATEGORIA_GEOGRAFICA'] = df_parana['NO_MUNICIPIO_PROVA'].apply(categorizar_municipio)

    provas = {
        'NU_NOTA_CN': 'Ciências Natureza',
        'NU_NOTA_CH': 'Ciências Humanas',
        'NU_NOTA_LC': 'Linguagens e Códigos',
        'NU_NOTA_MT': 'Matemática',
        'NU_NOTA_REDACAO': 'Redação'
    }

    medias_geo = df_parana.groupby('CATEGORIA_GEOGRAFICA')[list(provas.keys())].mean()
    medias_geo.rename(columns=provas, inplace=True)
    medias_geo['Média Geral'] = medias_geo.mean(axis=1)

    maiores_notas = df_parana.groupby('CATEGORIA_GEOGRAFICA')[list(provas.keys())].max()
    maiores_notas['Maior Média Geral'] = maiores_notas.mean(axis=1)

    c1, c2, c3 = st.columns(3)
    
    with c1:
        nota_cap = medias_geo.loc['Capital (Curitiba)', 'Média Geral']
        max_cap = maiores_notas.loc['Capital (Curitiba)', 'Maior Média Geral']
        st.metric("Média Geral: Curitiba", f"{nota_cap:.2f}")
        st.caption(f"🚀 Maior Nota Categoria: {max_cap:.2f}")
    
    with c2:
        nota_polos = medias_geo.loc['Polos Regionais', 'Média Geral']
        max_polos = maiores_notas.loc['Polos Regionais', 'Maior Média Geral']
        st.metric("Média Geral: Polos Regionais", f"{nota_polos:.2f}", delta=f"{nota_polos - nota_cap:.2f}")
        st.caption(f"🚀 Maior Nota Categoria: {max_polos:.2f}")

    with c3:
        nota_int = medias_geo.loc['Interior (Demais)', 'Média Geral']
        max_int = maiores_notas.loc['Interior (Demais)', 'Maior Média Geral']
        st.metric("Média Geral: Interior", f"{nota_int:.2f}", delta=f"{nota_int - nota_cap:.2f}")
        st.caption(f"🚀 Maior Nota Categoria: {max_int:.2f}")

    st.markdown("---")
    
    df_plot_medias = medias_geo.drop(columns='Média Geral').reset_index().melt(id_vars='CATEGORIA_GEOGRAFICA')
    df_plot_medias.columns = ['Localidade', 'Área do Conhecimento', 'Nota Média']

    fig_medias = px.bar(
        df_plot_medias,
        x='Área do Conhecimento',
        y='Nota Média',
        color='Localidade',
        barmode='group',
        text_auto='.1f',
        color_discrete_map={'Capital (Curitiba)': '#1f77b4', 'Polos Regionais': '#2ca02c', 'Interior (Demais)': '#7f7f7f'}
    )
    fig_medias.update_layout(yaxis=dict(range=[450, 650]))
    st.plotly_chart(fig_medias, use_container_width=True)

    st.markdown("---")
    st.subheader("Detalhamento por Município")
    
    tabela_mun = df_parana.groupby('NO_MUNICIPIO_PROVA')[list(provas.keys())].mean().rename(columns=provas)
    tabela_mun['Média Geral'] = tabela_mun.mean(axis=1)
    tabela_mun['Categoria'] = tabela_mun.index.map(categorizar_municipio)
    tabela_mun = tabela_mun.sort_values(by='Média Geral', ascending=False)

    def style_by_category(row):
        if row['Categoria'] == 'Capital (Curitiba)':
            return ['background-color: #bbdefb; color: black'] * len(row)
        elif row['Categoria'] == 'Polos Regionais':
            return ['background-color: #c8e6c9; color: black'] * len(row)
        return [''] * len(row)

    colunas_notas = list(provas.values()) + ['Média Geral']
    
    tabela_final = (tabela_mun.style
                    .apply(style_by_category, axis=1)
                    .highlight_max(subset=colunas_notas, props='background-color: #ffff00; color: black; font-weight: bold;')
                    .format(precision=2))

    st.dataframe(tabela_final, use_container_width=True, height=500)

    st.markdown(f"""
    **Legenda de Categorias:**
    * <span style="background-color: #bbdefb; padding: 2px 5px; border-radius: 3px; color: black;">**Azul:**</span> Capital (Curitiba)
    * <span style="background-color: #c8e6c9; padding: 2px 5px; border-radius: 3px; color: black;">**Verde:**</span> Polos Regionais (Londrina, Maringá, Ponta Grossa, Guarapuava, Cascavel)
    * <span style="background-color: #ffff00; padding: 2px 5px; border-radius: 3px; color: black;">**Amarelo:**</span> Maior nota da coluna (Destaque Geral)
    """, unsafe_allow_html=True)