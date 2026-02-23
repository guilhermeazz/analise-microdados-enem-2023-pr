import pandas as pd
import streamlit as st
from pathlib import Path


DIRETORIO_ATUAL = Path(__file__).resolve().parent.parent.parent
CAMINHO_CSV = DIRETORIO_ATUAL / 'data' / 'MICRODADOS_ENEM_2023.csv'


# src/utils/data_loader.py

COLUNAS_NECESSARIAS = [
    'SG_UF_PROVA', 'TP_SEXO', 'TP_COR_RACA', 'TP_FAIXA_ETARIA', 
    'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO',
    'Q006', 'TP_ESCOLA', 'IN_TREINEIRO', 'NO_MUNICIPIO_PROVA',
    'TP_PRESENCA_CN', 'TP_PRESENCA_CH', 'TP_PRESENCA_LC', 'TP_PRESENCA_MT',
    'TP_DEPENDENCIA_ADM_ESC', 'TP_LINGUA',
    'NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5',
    'Q001', 'Q002',
    'Q021','Q024', 'Q025'
]

@st.cache_data 
def carregar_dados():
    try:
        df = pd.read_csv(CAMINHO_CSV, sep=';', encoding='ISO-8859-1', usecols=COLUNAS_NECESSARIAS)
        
        colunas_numericas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
        for coluna in colunas_numericas:
            df[coluna] = pd.to_numeric(df[coluna], errors='coerce')
            
        return df
    except Exception as e:
        st.error(f'Erro ao carregar os dados. Verifique o caminho: {e}')
        return None