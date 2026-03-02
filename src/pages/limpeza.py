import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Limpeza e Sanidade", page_icon="🧹", layout="wide")

st.header("🧹 Fase 1: Limpeza, Sanidade e Tratamento de Exceções")
st.write("Garantindo a integridade estatística da base de dados do INEP antes de qualquer análise.")

# 1. O Paradoxo dos Faltantes (Explicação Crucial para a Banca)
st.subheader("1. O Paradoxo dos Faltantes: Como limpar sem perder dados?")
st.info("""
**O Desafio:** Para calcular médias de notas precisas, precisamos remover alunos que faltaram (cujas notas são `NaN`). No entanto, se removermos os faltantes logo no início, como faremos a análise de Taxa de Abstenção (Pergunta 4)?

**A Solução (Bifurcação de Pipeline):** Nosso módulo `data_loader` não retorna apenas um DataFrame, mas ramifica a base em diferentes estágios de limpeza:
- `df_abstencao`: Mantém todos os inscritos (incluindo `NaNs`) exclusivamente para analisar padrões de presença e abstenção municipal.
- `df_performance`: Passa por um filtro rigoroso (`dropna`), retendo apenas quem teve provas corrigidas, garantindo que as médias e o Teste de Hipótese não sejam enviesados por zeros artificiais.
""")

st.markdown("---")

# 2. Validações Lógicas e Outliers
st.subheader("2. Validação de Consistência Lógica e Outliers")
st.write("Mesmo em dados oficiais, inconsistências ocorrem. Aplicamos regras de negócio para sanar a base:")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.error("**Inconsistência de Presença**")
    st.write("""
    **Problema:** Registros marcados como "Presente" (`TP_PRESENCA == 1`), mas com nota nula ou ausente na base.
    **Correção:** Cruzamento lógico obrigatório. Só mantivemos como válidos os candidatos onde `TP_PRESENCA == 1` **E** a nota era um valor numérico válido.
    """)

with col_b:
    st.warning("**Tratamento de Outliers**")
    st.write("""
    **Problema:** Notas extremas que desafiam a Teoria de Resposta ao Item (TRI) ou notas zero não justificadas pela redação.
    **Correção:** Garantia de que notas zeradas na Redação correspondiam a códigos de anulação (ex: fuga ao tema, folha em branco) e não a falhas de processamento.
    """)

with col_c:
    st.success("**Correção de Tipos Nativos**")
    st.write("""
    **Problema:** O Pandas muitas vezes importa códigos numéricos que na verdade são classes (ex: Município `4106902`).
    **Correção:** Forçamos a tipagem correta logo na ingestão, garantindo que identificadores não fossem somados acidentalmente em análises descritivas.
    """)

st.markdown("---")

# 3. Funil de Sanidade
st.subheader("3. O Funil de Retenção de Dados")
# Gráfico de Funil (Ilustrativo da redução de dimensionalidade)
fig_funnel = go.Figure(go.Funnel(
    y=[
        "1. Inscritos Totais (Raw Data)", 
        "2. Análise de Abstenção (df_abstencao)", 
        "3. Filtro de Presença e Consistência", 
        "4. Base de Performance Final (df_pr / df_br)"
    ],
    x=[3933955, 3933955, 2760520, 2734100],
    textinfo="value+percent initial",
    marker={"color": ["#7f7f7f", "#1f77b4", "#ff7f0e", "#2ca02c"]}
))
fig_funnel.update_layout(height=400, margin=dict(t=20, b=20))
st.plotly_chart(fig_funnel, use_container_width=True)