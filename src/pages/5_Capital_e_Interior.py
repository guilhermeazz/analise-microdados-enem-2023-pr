import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import carregar_dados_projeto

st.set_page_config(page_title="Capital vs Interior", page_icon="🏙️", layout="wide")

df_pr, _, _ = carregar_dados_projeto()

if df_pr is not None:
    st.header("5. Disparidade: Capital vs. Polos Regionais vs. Interior")
    
    st.info("""
    **Nota Metodológica:** Os polos regionais analisados foram selecionados com base na influência econômica e 
    administrativa regional. Esta classificação permite identificar se o desempenho educacional está 
    concentrado apenas na capital ou se é distribuído pelos centros regionais.
    """)

    polos_regionais = ['LONDRINA', 'MARINGA', 'MARINGÁ', 'PONTA GROSSA', 'GUARAPUAVA', 'CASCAVEL']
    
    def categorizar_municipio(mun):
        mun_clean = str(mun).upper().strip()
        if mun_clean == 'CURITIBA':
            return 'Capital (Curitiba)'
        elif mun_clean in polos_regionais:
            return 'Polos Regionais'
        else:
            return 'Interior (Demais)'

    df_pr['CATEGORIA_GEOGRAFICA'] = df_pr['NO_MUNICIPIO_PROVA'].apply(categorizar_municipio)

    provas = {
        'NU_NOTA_CN': 'Ciências Natureza',
        'NU_NOTA_CH': 'Ciências Humanas',
        'NU_NOTA_LC': 'Linguagens e Códigos',
        'NU_NOTA_MT': 'Matemática',
        'NU_NOTA_REDACAO': 'Redação'
    }
    colunas_notas = list(provas.keys())

    medias_geo = df_pr.groupby('CATEGORIA_GEOGRAFICA')[colunas_notas + ['MEDIA_GERAL']].mean()
    maiores_notas = df_pr.groupby('CATEGORIA_GEOGRAFICA')[colunas_notas + ['MEDIA_GERAL']].max()

    c1, c2, c3 = st.columns(3)
    
    with c1:
        nota_cap = medias_geo.loc['Capital (Curitiba)', 'MEDIA_GERAL']
        max_cap = maiores_notas.loc['Capital (Curitiba)', 'MEDIA_GERAL']
        st.metric("Média Geral: Curitiba", f"{nota_cap:.2f}")
        st.caption(f"🚀 Recorde Categoria: {max_cap:.2f}")
    
    with c2:
        nota_polos = medias_geo.loc['Polos Regionais', 'MEDIA_GERAL']
        max_polos = maiores_notas.loc['Polos Regionais', 'MEDIA_GERAL']

        st.metric("Média Geral: Polos Regionais", f"{nota_polos:.2f}", delta=f"{nota_polos - nota_cap:.2f}")
        st.caption(f"🚀 Recorde Categoria: {max_polos:.2f}")

    with c3:
        nota_int = medias_geo.loc['Interior (Demais)', 'MEDIA_GERAL']
        max_int = maiores_notas.loc['Interior (Demais)', 'MEDIA_GERAL']
        st.metric("Média Geral: Interior", f"{nota_int:.2f}", delta=f"{nota_int - nota_cap:.2f}")
        st.caption(f"🚀 Recorde Categoria: {max_int:.2f}")

    st.markdown("---")
    
    df_plot_medias = medias_geo.drop(columns='MEDIA_GERAL').rename(columns=provas).reset_index().melt(id_vars='CATEGORIA_GEOGRAFICA')
    df_plot_medias.columns = ['Localidade', 'Área do Conhecimento', 'Nota Média']

    fig_medias = px.bar(
        df_plot_medias,
        x='Área do Conhecimento',
        y='Nota Média',
        color='Localidade',
        barmode='group',
        text_auto='.1f',
        color_discrete_map={
            'Capital (Curitiba)': '#1f77b4', 
            'Polos Regionais': '#2ca02c', 
            'Interior (Demais)': '#7f7f7f'
        }
    )
    fig_medias.update_layout(yaxis=dict(range=[480, 620]), height=500)
    st.plotly_chart(fig_medias, use_container_width=True)

    st.markdown("---")

    st.subheader("Detalhamento por Município")
    
    tabela_mun = df_pr.groupby('NO_MUNICIPIO_PROVA')[colunas_notas + ['MEDIA_GERAL']].mean().rename(columns=provas)
    tabela_mun.rename(columns={'MEDIA_GERAL': 'Média Geral'}, inplace=True)
    
    tabela_mun['Categoria'] = tabela_mun.index.map(categorizar_municipio)
    tabela_mun = tabela_mun.sort_values(by='Média Geral', ascending=False)

    def style_by_category(row):
        if row['Categoria'] == 'Capital (Curitiba)':
            return ['background-color: #bbdefb; color: black'] * len(row)
        elif row['Categoria'] == 'Polos Regionais':
            return ['background-color: #c8e6c9; color: black'] * len(row)
        return [''] * len(row)

    colunas_finais = list(provas.values()) + ['Média Geral']
    
    tabela_final = (tabela_mun.style
                    .apply(style_by_category, axis=1)
                    .highlight_max(subset=colunas_finais, props='background-color: #ffff00; color: black; font-weight: bold;')
                    .format(precision=2))

    st.dataframe(tabela_final, use_container_width=True, height=500)

    st.markdown(f"""
    **Legenda de Destaque:**
    * <span style="background-color: #bbdefb; padding: 2px 5px; border-radius: 3px; color: black;">**Azul:**</span> Capital (Curitiba)
    * <span style="background-color: #c8e6c9; padding: 2px 5px; border-radius: 3px; color: black;">**Verde:**</span> Polos Regionais (Ex: Londrina, Maringá)
    * <span style="background-color: #ffff00; padding: 2px 5px; border-radius: 3px; color: black;">**Amarelo:**</span> Maior média da coluna
    """, unsafe_allow_html=True)