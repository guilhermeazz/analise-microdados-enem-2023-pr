from .limpeza import corrigir_tipos_e_outliers, validar_consistencia_logica
from .transformacao import criar_features_estatisticas, aplicar_mapeamento_dicionarios
from .otimizacao import reduzir_consumo_memoria

def processar_dados_enem(df):
    df = corrigir_tipos_e_outliers(df)
    df = validar_consistencia_logica(df)
    
    df = criar_features_estatisticas(df)
    df = aplicar_mapeamento_dicionarios(df)
    
    df = reduzir_consumo_memoria(df)
    
    return df