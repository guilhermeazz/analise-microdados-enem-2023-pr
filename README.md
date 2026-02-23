# 📊 Análise Exploratória dos Microdados do ENEM 2023

Este projeto de Ciência de Dados realiza uma análise aprofundada dos microdados do Exame Nacional do Ensino Médio (ENEM) de 2023, com foco em comparar o perfil socioeconômico e o desempenho dos candidatos do estado do **Paraná (PR)** em relação à média do **Brasil**.

O projeto responde a 20 perguntas estratégicas através de um painel interativo (Dashboard) construído em Python.

## 🛠️ Tecnologias Utilizadas
* **Linguagem:** Python 3.10+
* **Dashboard:** Streamlit
* **Manipulação de Dados:** Pandas
* **Visualização:** Plotly Express & Matplotlib

## 📁 Arquitetura do Projeto
Para garantir escalabilidade e manutenção, o projeto utiliza a arquitetura Multipage do Streamlit:

```text
/
├── data/                 # (Ignorado no Git) Arquivo MICRODADOS_ENEM_2023.csv
├── src/
│   ├── utils/            # Módulos de carregamento (Cache) e dicionários
│   ├── pages/            # Telas interativas para cada uma das 20 perguntas
│   └── app.py            # Página inicial do Dashboard
├── .gitignore
├── requirements.txt      # Dependências do projeto
└── README.md
```


---

# 🎯 As 20 Perguntas Estratégicas (Eixos de Análise)

---

## 📊 Eixo 1: Perfil Demográfico e Representatividade

Foco em entender **"quem" é o candidato** e como a amostra do PR se compara ao Brasil.

1. **Perfil Comparativo:** Como se caracteriza o candidato médio do Paraná (idade, cor/raça, sexo) e como esse perfil diverge da média nacional?  
2. **Natureza da Instituição:** Qual a proporção de alunos de escolas públicas vs. privadas no Paraná em comparação ao cenário brasileiro?  
3. **Engajamento Acadêmico:** O estado do Paraná possui uma taxa de "treineiros" superior à média nacional?  
4. **Taxa de Abstenção:** O Paraná teve uma taxa de ausentes (1º ou 2º dia) maior ou menor que a média nacional? Existe correlação entre o município do candidato e a desistência?  
5. **Capital vs. Interior:** Qual é a disparidade de notas médias entre Curitiba e as cidades do interior? Existem polos regionais (ex: Londrina, Maringá, Cascavel) que superam a capital em áreas específicas?  

---

## 📈 Eixo 2: Desempenho e Variabilidade Acadêmica

Foco na estatística de notas e validação da metodologia de ensino.

6. **Benchmarking Nacional:** Em quais áreas do conhecimento o Paraná supera a média nacional de forma estatisticamente significativa?  
7. **Variabilidade das Notas ($\sigma$):** Qual área do conhecimento apresenta a maior dispersão (desvio padrão) no Paraná? Essa inconsistência é maior ou menor que no restante do Brasil?  
8. **Ensino Técnico:** Alunos que cursaram o ensino médio em escolas técnicas (como IFPRs ou estaduais profissionalizantes) apresentam desempenho em Matemática superior à média estadual?  
9. **Língua Estrangeira:** Qual a proporção de escolha entre Inglês e Espanhol no PR vs. Brasil? Existe diferença significativa na nota de Linguagens baseada nessa escolha?  
10. **Gargalos da Redação:** Ao analisar as 5 competências da Redação, qual delas é o ponto forte do paranaense e qual apresenta a maior dificuldade em comparação ao Brasil?  

---

## ⚖️ Eixo 3: Desigualdade e Fatores Socioeconômicos

Foco em equidade e o impacto do contexto social no desempenho final.

11. **Gaps de Equidade:** A diferença de desempenho entre sexos e grupos de cor/raça no Paraná é mais ou menos acentuada do que no cenário nacional?  
12. **Peso da Renda:** Qual o coeficiente de correlação entre a renda familiar (Q006) e a nota da Redação no Paraná? A renda "pesa" mais no PR do que no Brasil?  
13. **Mitigação de Desigualdade:** O sistema educacional do Paraná consegue mitigar a desigualdade socioeconômica (menor impacto da renda na nota final) melhor que a média nacional?  
14. **O "Degrau" de Performance:** Em qual faixa de renda observa-se o maior salto (gradiente) de performance entre os candidatos do estado?  
15. **Herança Educacional:** Como o nível de instrução dos pais (Q001 e Q002) influencia a probabilidade de um aluno paranaense atingir mais de 700 pontos na média geral?  
16. **Binômio Trabalho-Estudo:** Qual a diferença de nota entre alunos que "apenas estudam" e alunos que "trabalham e estudam" no PR comparado ao cenário nacional?  

---

## 💻 Eixo 4: Tecnologia, Inclusão e Metodologia

Foco em infraestrutura digital e validação técnica dos dados.

17. **Inclusão Digital:** Candidatos do PR que não possuem acesso à internet em casa apresentam desempenho inferior em quais áreas? O impacto é maior no interior ou na capital?  
18. **Posse de Bens:** Existe uma correlação estatisticamente significativa entre a posse de computador em casa (Q024) e o desempenho em Matemática e Redação?  
19. **Distorção Idade-Série:** Como o desempenho dos concluintes na "idade ideal" se compara aos candidatos em atraso escolar no PR? Esse impacto é mais severo no estado do que na média BR?  
20. **Viés Metodológico:** A ordem das questões (cor da prova) demonstra alguma mudança significativa nos resultados dos candidatos paranaenses?  

---

# 🚀 Como Executar Localmente

## 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/analise-enem-2023-pr.git
cd analise-enem-2023-pr
```

## 2️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

## 3️⃣ Baixe os Dados do INEP
1. Faça o download dos Microdados do ENEM 2023 no portal do INEP.
2. Extraia o arquivo MICRODADOS_ENEM_2023.csv.
3. Coloque-o dentro da pasta:

```código
data/
```

## 4️⃣ Execute o Dashboard
```bash
streamlit run src/app.py
```

# 📌 Objetivo do Projeto
Fornecer uma visão estratégica, estatística e interativa sobre o desempenho e o perfil dos candidatos do Paraná no ENEM 2023, permitindo:
- Comparações diretas com a média nacional
- Análise de desigualdades estruturais
- Identificação de gargalos educacionais
- Apoio à tomada de decisão baseada em dados
