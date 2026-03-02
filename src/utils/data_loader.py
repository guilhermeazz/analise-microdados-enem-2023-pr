import pandas as pd
import streamlit as st
from pathlib import Path
import os

DIRETORIO_ATUAL = Path(__file__).resolve().parent.parent.parent
CAMINHO_PARQUET = DIRETORIO_ATUAL / 'data' / 'MICRODADOS_ENEM_2023_OTIMIZADO.parquet'

@st.cache_data(show_spinner="Carregando Pipeline Otimizado...") 
def carregar_dados_projeto():
    try:
        if not CAMINHO_PARQUET.exists():
            st.error(f"Arquivo não encontrado: {CAMINHO_PARQUET}. Certifique-se de que o Parquet foi gerado.")
            return None, None, None

        df_base = pd.read_parquet(CAMINHO_PARQUET, engine='pyarrow')

        df_abstencao = df_base.copy()

        colunas_notas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
        df_performance = df_base.dropna(subset=colunas_notas, how='all').copy()

        df_pr = df_performance[df_performance['SG_UF_PROVA'] == 'PR'].copy()
        df_brasil_sem_pr = df_performance[df_performance['SG_UF_PROVA'] != 'PR'].copy()
        
        return df_pr, df_brasil_sem_pr, df_abstencao
        
    except Exception as e:
        st.error(f'Erro fatal no Pipeline de Dados: {e}')
        return None, None, None