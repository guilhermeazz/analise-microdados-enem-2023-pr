import pandas as pd
from .dicionarios import MAPA_MESTRE_ENEM, agrupar_moradores

def categorizar_desempenho(nota):
    if pd.isna(nota): return 'Nulo'
    if nota < 450: return 'Baixo'
    if nota < 650: return 'Médio'
    if nota < 800: return 'Alto'
    return 'Elite'

def criar_features_estatisticas(df):
    colunas_notas = ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO']
    
    df['MEDIA_GERAL'] = df[colunas_notas].mean(axis=1)
    
    df['NIVEL_DESEMPENHO'] = df['MEDIA_GERAL'].apply(categorizar_desempenho)
    
    if 'NO_MUNICIPIO_PROVA' in df.columns:
        df['REGIAO_PR'] = df['NO_MUNICIPIO_PROVA'].apply(
            lambda x: 'Capital' if str(x).upper() == 'CURITIBA' else 'Interior'
        )

    if 'Q005' in df.columns:
        df['MORADORES_AGRUPADO'] = df['Q005'].apply(agrupar_moradores)
        
    return df

def aplicar_mapeamento_dicionarios(df):
    for coluna, mapa in MAPA_MESTRE_ENEM.items():
        if coluna in df.columns:
            df[f'{coluna}_LABEL'] = df[coluna].map(mapa)
    return df

def criar_score_social(df):
    renda_pontos = {chr(i): i-64 for i in range(65, 82)} 
    if 'Q006' in df.columns:
        df['SCORE_RENDA'] = df['Q006'].map(renda_pontos).fillna(0)
    
    return df