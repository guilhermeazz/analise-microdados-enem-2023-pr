# src/utils/data_loader.py

import pandas as pd
import streamlit as st
from pathlib import Path
from .pre_processing import processar_dados_enem

DIRETORIO_ATUAL = Path(__file__).resolve().parent.parent.parent
CAMINHO_CSV = DIRETORIO_ATUAL / 'data' / 'MICRODADOS_ENEM_2023.csv'

COLUNAS_NECESSARIAS = [
    'SG_UF_PROVA', 'TP_SEXO', 'TP_COR_RACA', 'TP_FAIXA_ETARIA', 
    'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO',
    'Q006', 'TP_ESCOLA', 'IN_TREINEIRO', 'NO_MUNICIPIO_PROVA',
    'TP_PRESENCA_CN', 'TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT',
    'TP_DEPENDENCIA_ADM_ESC', 'TP_LINGUA',
    'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5',
    'Q001', 'Q002', 'Q005', 'Q021', 'Q024', 'Q025', 'TP_ST_CONCLUSAO', 'CO_PROVA_MT'
]

@st.cache_data 
def carregar_dados_projeto():
    try:
        df_raw = pd.read_csv(CAMINHO_CSV, sep=';', encoding='ISO-8859-1', usecols=COLUNAS_NECESSARIAS)
        
        df_base = processar_dados_enem(df_raw)

        df_abstencao = df_base.copy()

        colunas_notas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
        df_performance = df_base.dropna(subset=colunas_notas, how='all').copy()

        df_pr = df_performance[df_performance['SG_UF_PROVA'] == 'PR']
        df_brasil_sem_pr = df_performance[df_performance['SG_UF_PROVA'] != 'PR']
        
        return df_pr, df_brasil_sem_pr, df_abstencao
        
    except Exception as e:
        st.error(f'Erro fatal no Pipeline de Dados: {e}')
        return None, None, None