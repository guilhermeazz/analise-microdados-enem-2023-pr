import pandas as pd
import streamlit as st
from pathlib import Path


DIRETORIO_ATUAL = Path(__file__).resolve().parent.parent.parent
CAMINHO_CSV = DIRETORIO_ATUAL / 'data' / 'MICRODADOS_ENEM_2023.csv'

COLUNAS_NECESSARIAS = [
    'SG_UF_PROVA', 'TP_SEXO', 'TP_COR_RACA', 'TP_FAIXA_ETARIA', 
    'NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO',
    'Q006', 'TP_ESCOLA' 
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