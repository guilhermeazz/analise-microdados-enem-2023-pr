import pandas as pd
from src.utils.data_loader import COLUNAS_NECESSARIAS
from src.utils.pre_processing import processar_dados_enem
from pathlib import Path

DIRETORIO_DATA = Path('data')
ARQUIVO_CSV = DIRETORIO_DATA / 'MICRODADOS_ENEM_2023.csv'
ARQUIVO_PARQUET = DIRETORIO_DATA / 'dados_enem_otimizados.parquet'

def converter_csv_para_parquet():
    print("Iniciando conversão.")
    
    df = pd.read_csv(
        ARQUIVO_CSV, 
        sep=';', 
        encoding='ISO-8859-1', 
        usecols=COLUNAS_NECESSARIAS
    )
    print("CSV carregado. Iniciando processamento.")

    df_processado = processar_dados_enem(df)
    print("Dados limpos, rotulados e otimizados.")

    df_processado.to_parquet(ARQUIVO_PARQUET, engine='pyarrow', compression='snappy')
    print(f"Sucesso! Arquivo gerado em: {ARQUIVO_PARQUET}")

if __name__ == "__main__":
    converter_csv_para_parquet()