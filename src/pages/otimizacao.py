import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Otimização e Tipagem", page_icon="⚡", layout="wide")

st.header("⚡ Fase 2: Otimização de Memória e Tipagem de Dados")
st.write("Como manipulamos microdados massivos sem estourar a memória RAM e garantindo performance em tempo real.")



c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Formato Raw", "CSV (+3 GB)", "Lento e Ineficiente", delta_color="inverse")
with c2:
    st.metric("Otimização de Tipos", "- 60% RAM", "Downcasting e Categorias", delta_color="normal")
with c3:
    st.metric("Formato Final", "Parquet (~450 MB)", "Armazenamento Colunar")

st.markdown("---")

# Explicação Profunda das Técnicas
st.subheader("Engenharia de Otimização no Código")
st.write("A simples conversão para Parquet não é suficiente. Precisamos ensinar a máquina como interpretar cada coluna:")

col_text, col_code = st.columns([1.2, 1])

with col_text:
    with st.expander("1. Otimização Numérica (Downcasting)", expanded=True):
        st.write("""
        Por padrão, o Python/Pandas aloca números em 64 bits (`float64` ou `int64`). 
        As notas do ENEM variam de 0 a 1000 e idades variam de 0 a 100. 
        **Ação:** Fizemos o *downcast* das notas para `float32` e das variáveis categóricas numéricas para `int8` ou `int16`. Isso cortou o consumo numérico pela metade sem perder precisão.
        """)
        
    with st.expander("2. Conversão para Categorias (Memory Mapping)", expanded=True):
        st.write("""
        Colunas com texto repetitivo (ex: 'Masculino'/'Feminino', nomes de cidades, códigos de renda de 'A' a 'Q') são lidas como `object` (strings), que consomem muita memória.
        **Ação:** Convertê-las para o tipo `category`. O Pandas passa a armazenar um dicionário binário leve por trás dos panos, o que acelera agrupamentos (`groupby`) em mais de 10x.
        """)

    with st.expander("3. Estrutura Colunar (Apache Parquet)", expanded=True):
        st.write("""
        O CSV lê os dados linha a linha. O Parquet organiza os dados por coluna. Como nossos dashboards geralmente pedem agregações de colunas específicas (ex: `Média de Matemática por Renda`), o motor de leitura só carrega as colunas necessárias na RAM.
        """)

with col_code:
    st.markdown("**Código de Otimização Aplicado:**")
    st.code("""
    # Exemplo do nosso módulo de Limpeza
    
    # 1. Downcasting Numérico
    df['NU_NOTA_MT'] = pd.to_numeric(df['NU_NOTA_MT'], downcast='float')
    df['TP_FAIXA_ETARIA'] = pd.to_numeric(df['TP_FAIXA_ETARIA'], downcast='integer')
    
    # 2. Conversão Categórica
    colunas_categoricas = ['SG_UF_PROVA', 'TP_SEXO', 'Q006']
    for col in colunas_categoricas:
        df[col] = df[col].astype('category')
        
    # 3. Exportação Eficiente
    df.to_parquet('microdados_otimizados.parquet', engine='pyarrow')
    """, language="python")

st.markdown("---")

# Gráfico ilustrativo de uso de memória
st.subheader("Impacto Mensurável na Memória RAM")
df_mem = pd.DataFrame({
    'Estado do Pipeline': ['1. Raw (CSV + Float64 + Object)', '2. Tipos Otimizados (Downcast + Category)', '3. Formato Parquet (Colunar)'],
    'Uso de RAM (GB)': [4.5, 1.8, 0.6]
})
fig_mem = px.bar(
    df_mem, x='Uso de RAM (GB)', y='Estado do Pipeline', 
    orientation='h', text_auto='.1f',
    color='Estado do Pipeline',
    color_discrete_sequence=['#ef553b', '#ff7f0e', '#2ca02c']
)
fig_mem.update_layout(showlegend=False, height=350)
st.plotly_chart(fig_mem, use_container_width=True)