import pandas as pd

def otimizar_tipos_numericos(df):
    cols_float = df.select_dtypes(include=['float64']).columns
    for col in cols_float:
        df[col] = pd.to_numeric(df[col], downcast='float')

    cols_int = df.select_dtypes(include=['int64', 'Int64']).columns
    for col in cols_int:
        df[col] = pd.to_numeric(df[col], downcast='integer')
        
    return df

def converter_para_categorias(df):
    cols_para_categoria = [
        'SG_UF_PROVA', 'TP_SEXO_LABEL', 'TP_COR_RACA_LABEL', 
        'TP_ESCOLA_LABEL', 'Q006_LABEL', 'TP_LINGUA_LABEL',
        'MORADORES_AGRUPADO', 'TP_ST_CONCLUSAO_LABEL'
    ]
    
    for col in cols_para_categoria:
        if col in df.columns:
            df[col] = df[col].astype('category')
            
    return df

def remover_colunas_desnecessarias(df):
    colunas_originais_id = [
        'TP_SEXO', 'TP_COR_RACA', 'TP_ESCOLA', 'TP_LINGUA', 
        'TP_ST_CONCLUSAO', 'Q006'
    ]
    para_remover = [c for c in colunas_originais_id if f"{c}_LABEL" in df.columns]
    df = df.drop(columns=para_remover, errors='ignore')
    
    return df

def reduzir_consumo_memoria(df):
    df = otimizar_tipos_numericos(df)
    df = converter_para_categorias(df)
    df = remover_colunas_desnecessarias(df)
    
    df = df.copy() 
    
    return df