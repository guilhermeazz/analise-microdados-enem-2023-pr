import pandas as pd
import numpy as np

def corrigir_tipos_e_outliers(df):
    cols_notas = [c for c in df.columns if 'NU_NOTA' in c]
    for col in cols_notas:
        df[col] = pd.to_numeric(df[col], errors='coerce').astype('float32')
        df.loc[df[col] < 0, col] = np.nan

    cols_inteiras = [
        'TP_FAIXA_ETARIA', 'TP_ST_CONCLUSAO', 'TP_ESCOLA', 
        'IN_TREINEIRO', 'TP_PRESENCA_CN', 'TP_PRESENCA_CH', 
        'TP_PRESENCA_LC', 'TP_PRESENCA_MT', 'CO_PROVA_MT', 'Q005'
    ]
    for col in cols_inteiras:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
            
    return df

def validar_consistencia_logica(df):
    df.loc[df['TP_PRESENCA_MT'].isin([0, 2]), 'NU_NOTA_MT'] = np.nan
    df.loc[df['TP_PRESENCA_CN'].isin([0, 2]), 'NU_NOTA_CN'] = np.nan
    
    if 'IN_TREINEIRO' in df.columns and 'TP_ST_CONCLUSAO' in df.columns:
        df.loc[(df['IN_TREINEIRO'] == 1) & (df['TP_ST_CONCLUSAO'] == 2), 'TP_ST_CONCLUSAO'] = 4

    cols_comp = ['NU_NOTA_COMP1', 'NU_NOTA_COMP2', 'NU_NOTA_COMP3', 'NU_NOTA_COMP4', 'NU_NOTA_COMP5']
    if all(c in df.columns for c in cols_comp):
        soma_calculada = df[cols_comp].sum(axis=1)
        df['REDACAO_CONSISTENTE'] = (abs(soma_calculada - df['NU_NOTA_REDACAO']) < 0.1)
        
    return df