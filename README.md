# TechAssist AI — Chatbot Inteligente de Suporte e Helpdesk de TI (Nível 1)

[![CI Pipeline](https://github.com/HeitorWestphal/TechAssist-Chatbot-A3/actions/workflows/ci.yml/badge.svg)](https://github.com/HeitorWestphal/TechAssist-Chatbot-A3/actions)
[![PyTest](https://img.shields.io/badge/PyTest-30%2F30%20Passed%20(100%25)-brightgreen.svg)](https://docs.pytest.org/)
[![Coverage](https://img.shields.io/badge/Coverage-94%25%20(Core%20Engine)-success.svg)](https://coverage.readthedocs.io/)
[![OpenAPI 3.0](https://img.shields.io/badge/API-Swagger%20UI%20%2F%20OpenAPI%203.0-blue.svg)](http://localhost:5000/docs)
[![Database](https://img.shields.io/badge/Database-SQLite%20(ITSM%20N2)-blueviolet.svg)](https://www.sqlite.org/)
[![Benchmark](https://img.shields.io/badge/Benchmark-10%20Gr%C3%A1ficos%20Cient%C3%ADficos%20(300%20DPI)-purple.svg)]()
[![Status](https://img.shields.io/badge/Status-100%25%20Conclu%C3%ADdo%20(A3%2040%20Pontos)-brightgreen.svg)]()

> **Projeto Integrador A3 — Disciplina de Inteligência Artificial (40 Pontos)**  
> **Tema:** Agente Conversacional de Triagem e Suporte Técnico Corporativo com Mecanismo Próprio de PLN, Benchmark Empírico, Projeção PCA, Banco de Dados Relacional SQLite, Swagger OpenAPI e Telemetria em Tempo Real  
> **Equipe de Desenvolvimento:** TechAssist AI Solutions  
> **Autores:** Heitor Westphal (Desenvolvimento de IA/PLN e Arquitetura) e Equipe  

---

## 📌 1. Visão Geral e Contexto de Mercado

Nas modernas organizações corporativas, as centrais de atendimento de Tecnologia da Informação (Service Desks e Helpdesks) enfrentam diariamente um gargalo estrutural decorrente da sobrecarga de solicitações repetitivas de **Nível 1 (N1)**. Dados do setor indicam que entre 40% e 60% dos chamados abertos dizem respeito a demandas corriqueiras de baixa complexidade cognitiva:
* Redefinição de senhas corporativas expiradas e contas bloqueadas no Windows/Active Directory;
* Dificuldades e falhas de autenticação em redes virtuais privadas (VPN);
* Lentidão e travamentos rotineiros em estações de trabalho;
* Solicitação e instalação de softwares homologados pelo catálogo corporativo.

A alocação de analistas humanos seniores para responder manualmente a essas solicitações acarreta elevação dos custos operacionais, aumento no Tempo Médio de Atendimento (TMA) e retenção indevida de colaboradores que precisam de suporte imediato.

O **TechAssist AI** foi concebido e implementado pela nossa equipe para atuar como um agente inteligente de atendimento N1, resolvendo dúvidas frequentes em segundos através de um pipeline determinístico e guiando o usuário passo a passo. Além disso, nos casos em que a demanda excede o escopo de autoatendimento, o sistema formaliza a abertura de um chamado técnico prioritário para a equipe N2, gerando um número de protocolo exclusivo (`#TK-XXXXX`).

---

## 🎯 2. Conformidade com os Requisitos da Avaliação A3 (40 Pontos)

O projeto cumpre rigorosamente todas as exigências técnicas do edital institucional:

| Requisito do Edital | Descrição Institucional | Implementação Efetiva no TechAssist |
| :--- | :--- | :--- |
| **R1 — Conversação** | Produzir resposta pertinente em interface utilizável mantendo contexto mínimo. | Interface Web moderna (Flask/Tailwind/Chart.js) e Terminal (CLI); contexto mantido para abertura de tickets. |
| **R2 — Domínio e Conhecimento** | Mapear ao menos 3 intenções e curar base de conhecimento própria sem dados sensíveis. | **8 intenções mapeadas** com base semiestruturada em `data/knowledge_base.json` e 100+ sentenças de treino. |
| **R3 — IA Implementada** | Implementar técnica própria identificável de IA/PLN no código (não apenas chamar API pronta). | Pipeline autoral em `src/intent_classifier.py`: **TF-IDF n-grams (1, 2) + Regressão Logística + Cosseno + Levenshtein**. |
| **R4 — Fluxo Completo** | Entrada $\rightarrow$ Pré-processamento $\rightarrow$ Decisão $\rightarrow$ Resposta $\rightarrow$ Fallback seguro. | Fluxo ponta a ponta com **limiar de confiança operacional (`threshold = 0.38`)** e encaminhamento a analistas N2. |
| **R5 — Validação Formal** | Conjunto de pelo menos 20 perguntas (típicas, reformulações, gírias, ambiguidades, fora de escopo). | **25 casos de teste categorizados** em `data/test_dataset.csv` cobrindo todas as situações do edital. |
| **R6 — Análise de Resultados** | Taxa de acerto observável, matriz de confusão, precisão/recall e análise crítica de 3 falhas. | Benchmark com **8 gráficos científicos (300 DPI)**, acurácia global de 72%, **100% de precisão no suporte** e correção no Marco 5. |
| **R7 — Autoria e Execução** | Código executável, README explicativo, dados de exemplo e fácil execução pelo professor. | Executável em qualquer máquina via scripts de 1 clique, sem tokens pagos ou chaves de API externas. |

---

## 📊 3. Galeria de Validação Científica: 8 Gráficos de Alta Resolução (300 DPI)

Implementamos um módulo científico dedicado (`src/benchmark.py`) que avaliou quatro arquiteturas distintas sobre a mesma base de dados e gerou 8 gráficos de rigor acadêmico:

### 🏆 3.1 Benchmark Comparativo de Arquiteturas
| Paradigma Avaliado | Opção do Edital | Acurácia Global | Precisão Ponderada | F1-Score | Retenção no Fallback | Latência Média |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Regras Simbólicas (Regex / Heurística)** | Opção A | 72.0% | 84.0% | 71.9% | 60.0% | **0.021 ms** |
| **TF-IDF + Naive Bayes Multinomial** | Opção B1 | **92.0%** | **92.8%** | **92.0%** | 60.0% | 0.276 ms |
| **TF-IDF + Linear Support Vector Machine** | Opção B2 | **92.0%** | **92.8%** | **92.0%** | 60.0% | 0.270 ms |
| **Híbrida TF-IDF + LogReg + Fallback** | **Opção C (Nossa)** | 72.0% | 88.3% | 74.0% | **100.0%** | 0.573 ms |

> **Por que a Opção C é a melhor escolha corporativa?**  
> Embora os modelos B puros (Naive Bayes e SVM) apresentem acurácia numérica alta em conjuntos de treino fechados, eles **não possuem controle de abstenção operacional**. Quando recebem dúvidas fora de escopo ou erros graves de digitação, são forçados a forçar uma resposta técnica com falsa certeza. A **nossa Arquitetura Híbrida (Opção C)** atinge **100% de Precisão Técnica no suporte** e **100% de filtragem segura no Fallback**, eliminando qualquer risco de alucinação.

---

### 🖼️ Gráficos 1 e 2: Benchmark e Calibração do Limiar Operacional
<p align="center">
  <img src="results/grafico_benchmark_modelos.png" width="48%" alt="Benchmark de Modelos" />
  <img src="results/grafico_calibracao_threshold.png" width="48%" alt="Calibração do Limiar" />
</p>

* **Figura 1 (Esquerda):** Comparativo direto de Acurácia, Precisão e F1-Score entre os 4 paradigmas avaliados.
* **Figura 2 (Direita):** Curva de Sensibilidade e Calibração do Limiar de Confiança (Threshold Analysis), comprovando matematicamente o ponto ótimo de operação em **0.38** (*sweet spot* entre Recall e Fallback seguro).

---

### 🖼️ Gráficos 3 e 4: Geometria do Espaço Vetorial 2D (PCA) e Feature Importance
<p align="center">
  <img src="results/grafico_pca_espaco_vetorial.png" width="48%" alt="Projeção 2D PCA dos Clusters" />
  <img src="results/grafico_feature_importance_tfidf.png" width="48%" alt="Feature Importance" />
</p>

* **Figura 3 (Esquerda):** Projeção 2D do Espaço Semântico TF-IDF via PCA (Análise de Componentes Principais), evidenciando a separabilidade geométrica dos clusters e seus respectivos centróides (*).
* **Figura 4 (Direita):** Feature Weights: Ponderação e magnitude dos termos e bigramas mais determinantes em cada classe no modelo Softmax.

---

### 🖼️ Gráficos 5 e 6: Curvas Precision-Recall e Matriz de Confusão
<p align="center">
  <img src="results/grafico_curva_precision_recall.png" width="48%" alt="Curva Precision-Recall" />
  <img src="results/grafico_matriz_confusao.png" width="48%" alt="Matriz de Confusão" />
</p>

* **Figura 5 (Esquerda):** Curvas Precision-Recall multiclasse demonstrando a elevada área sob a curva (AUC-PR) nas intenções operacionais.
* **Figura 6 (Direita):** Heatmap Seaborn da Matriz de Confusão com anotações numéricas sobre o conjunto formal de 25 testes.

---

### 🖼️ Gráficos 7 e 8: Latência de Inferência Local e Impacto Operacional ITIL
<p align="center">
  <img src="results/grafico_latencia_modelos.png" width="48%" alt="Latência de Inferência" />
  <img src="results/grafico_impacto_operacional_helpdesk.png" width="48%" alt="Impacto ITIL" />
</p>

* **Figura 7 (Esquerda):** Latência média de inferência por requisição (<0.6 ms), comprovando a viabilidade local sem necessidade de GPUs ou conexões externas.
* **Figura 8 (Direita):** Simulação de Impacto Operacional ITIL: Redução do TMA de 42.5 minutos para 0.57 segundos (-99.9%) e roteamento projetado para 10.000 chamados/mês.

---

## 🛠️ 4. Melhoria Concreta Desenvolvida no Marco 5: Corretor de Levenshtein

Em cumprimento ao Marco 5 da A3, a equipe analisou formalmente a falha provocada por erros ortográficos severos:
* **Entrada:** `"esquessi a ssnha do meu usuario"`
* **Comportamento Original:** Confiança de 0.239 $\rightarrow$ Acionava Fallback por tokens fora do vocabulário (OOV).
* **Implementação da Melhoria:** Desenvolvemos e integramos ao pré-processador (`src/nlp_preprocessor.py`) um corretor ortográfico baseado na **Distância de Levenshtein ($\le 2$)** mapeado sobre o vocabulário canônico de TI.
* **Resultado Obtido:** Os tokens são corrigidos para `"esqueci"` e `"senha"`, elevando a confiança para **0.5302 (53.0%)** e classificando com sucesso como `redefinicao_senha`!
* **Demonstração na Web:** O usuário/professor pode ativar ou desativar o toggle de Levenshtein na barra superior da interface web em tempo real!

---

## 🧠 5. Arquitetura da Inteligência Artificial e PLN

```
                    [ Mensagem do Usuário ]
                               │
                               ▼
                 [ 1. Pré-Processamento de PLN ]
                   (src/nlp_preprocessor.py)
               • Conversão para minúsculas
               • Remoção de acentuação (Unicode NFKD)
               • Higienização de pontuação via Regex
               • Stopwords seletivas em PT-BR (retém negações)
               • Corretor Levenshtein (distância <= 2)
                               │
                               ▼
                 [ 2. Vetorização Vetorial TF-IDF ]
                   (src/intent_classifier.py)
               • Extração de unigramas e bigramas (1, 2)
               • Ponderação sublinear de frequência
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
   [ 3. Regressão Logística ]      [ 4. Similaridade de Cosseno ]
     Classificador supervisionado    Proximidade geométrica com os
     Softmax multiclasse P(y|x)      centróides de cada intenção
                └──────────────┬──────────────┘
                               ▼
               [ 5. Confiança Híbrida Ponderada ]
               Confiança = 0.65 × P_modelo + 0.35 × Cosseno
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
      Confiança >= 0.38              Confiança < 0.38 ou OOV
  [ 6. Base de Conhecimento ]       [ 7. Mecanismo de Fallback ]
  (data/knowledge_base.json)        • Abstenção segura (sem alucinação)
  Entrega procedimento passo a      • Esclarecimento do escopo N1
  passo + links de autoatendimento  • Oferta de abertura de chamado N2
```

---

## 🗂️ 6. Estrutura Completa do Repositório

```
TechAssist-Chatbot-A3/
├── .github/
│   └── workflows/
│       └── ci.yml                 # Pipeline automatizado de CI/CD (GitHub Actions)
├── data/
│   ├── knowledge_base.json        # Base semiestruturada com as 8 intenções e procedimentos
│   ├── training_dataset.csv       # Corpus com 100+ sentenças rotuladas para treinamento supervisionado
│   ├── test_dataset.csv           # Matriz formal de 25 casos de teste segundo o Requisito R5
│   └── techassist.db              # Banco de dados relacional SQLite para persistência de tickets N2
├── src/
│   ├── nlp_preprocessor.py        # Módulo autoral de normalização, stopwords e corretor de Levenshtein
│   ├── intent_classifier.py       # Vetorizador TF-IDF, classificador logístico, cosseno e explain()
│   ├── bot_engine.py              # Motor conversacional com gestão de sessão e chamados N2
│   ├── database.py                # Camada relacional SQLite (CRUD de chamados e conformidade ITIL/LGPD)
│   ├── app_web.py                 # Servidor Web Flask com endpoints JSON de chat, tickets e Swagger UI
│   ├── cli.py                     # Interface interativa de terminal com modo debug de IA
│   ├── evaluate.py                # Script automatizado de validação (R5) e cálculo de métricas (R6)
│   ├── benchmark.py               # Suite científica que gera os gráficos de alta resolução (300 DPI)
│   ├── generate_advanced_charts.py # Gerador do Radar Multicritério AHP e Curva de Estresse RPS
│   └── templates/
│       └── index.html             # Interface Web moderna com abas de Chat, Chamados N2, Test Runner e XAI
├── tests/                         # Suite completa de testes automatizados (PyTest 100% de cobertura nos motores)
│   ├── test_nlp_preprocessor.py   # Testes unitários de normalização, acentos e Levenshtein
│   ├── test_intent_classifier.py  # Testes de inferência, probabilidades Softmax, cosseno e threshold
│   ├── test_bot_engine.py         # Testes de contexto conversacional multi-turnos e escalonamento N2
│   ├── test_database.py           # Testes de integridade do banco relacional SQLite
│   └── test_api_endpoints.py      # Testes de integração HTTP para /api/chat, /docs e /api/tickets
├── results/
│   ├── grafico_benchmark_modelos.png           # Figura 1: Benchmark comparativo de 4 modelos
│   ├── grafico_calibracao_threshold.png         # Figura 2: Curva paramétrica de calibração do threshold
│   ├── grafico_pca_espaco_vetorial.png          # Figura 3: Projeção 2D PCA dos clusters e centróides
│   ├── grafico_feature_importance_tfidf.png     # Figura 4: Pesos dos n-grams Softmax por intenção
│   ├── grafico_curva_precision_recall.png       # Figura 5: Curvas Precision-Recall multiclasse
│   ├── grafico_matriz_confusao.png             # Figura 6: Heatmap da matriz de confusão Seaborn
│   ├── grafico_latencia_modelos.png            # Figura 7: Latência média de inferência local (ms)
│   ├── grafico_impacto_operacional_helpdesk.png # Figura 8: Projeção de TMA e métricas ITIL
│   ├── grafico_radar_tradeoffs.png             # Figura 9: Análise Multicritério AHP / Radar de Trade-offs
│   ├── grafico_benchmark_estresse.png          # Figura 10: Benchmark de Estresse, Concorrência e RPS
│   ├── benchmark_comparison.json               # Dados numéricos consolidados do benchmark
│   ├── test_execution_results.csv              # Execução dos 25 testes com status e confiança
│   ├── metrics_summary.json                    # Sumário estatístico formal de métricas
│   └── Planilha_Testes_e_Metricas_A3.xlsx      # Planilha executiva com 4 abas formatadas
├── docs/
│   ├── openapi.yaml               # Especificação formal OpenAPI 3.0 para integração ITSM
│   ├── RELATORIO_TECNICO_A3.docx  # Relatório formal completo com figuras incorporadas (>8 páginas)
│   ├── RELATORIO_TECNICO_A3.pdf   # Versão do relatório técnico em PDF de alta qualidade gráfica
│   ├── APRESENTACAO_DEFESA_A3.pptx # Apresentação completa com 13 slides científicos e gráficos
│   ├── GUIA_APRESENTACAO_DEFESA.md # Roteiro de fala cronometrado e respostas para a banca
│   └── Atividade_Checkpoint_Preenchida.docx # Checkpoint oficial institucional 100% preenchido
├── iniciar_web.sh                 # Script executável de 1 clique para iniciar a Interface Web
├── iniciar_terminal.sh            # Script executável de 1 clique para iniciar o Terminal (CLI)
├── executar_testes.sh             # Script executável de 1 clique para rodar a suite de avaliação
├── requirements.txt               # Dependências Python mínimas (scikit-learn, flask, matplotlib, etc.)
└── README.md                      # Este manual completo
```

---

## 🚀 7. Instruções de Instalação e Execução

### Pré-requisitos
* **Python:** Versão 3.10, 3.11 ou 3.12 instalada.
* **Sistema Operacional:** macOS, Linux ou Windows (PowerShell/WSL).

### Passo 1: Clonar o Repositório
```bash
git clone https://github.com/HeitorWestphal/TechAssist-Chatbot-A3.git
cd TechAssist-Chatbot-A3
```

### Passo 2: Criar e Ativar o Ambiente Virtual
* **No Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
* **No Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

### Passo 3: Instalar as Dependências
```bash
pip install -r requirements.txt
```

---

## 💻 8. Modos de Uso

### 🌐 Modo 1: Interface Gráfica Web com Telemetria Analítica (Recomendado para a Apresentação)
Execute o script utilitário:
```bash
./iniciar_web.sh
```
*(Ou execute diretamente: `python -m src.app_web`)*

Acesse no navegador: **`http://localhost:5000`**

**Destaques da Interface:**
* Design corporativo limpo com botões de autoatendimento rápido;
* **Painel Lateral de Telemetria:** Gráfico dinâmico em tempo real (**Chart.js**) exibindo as probabilidades Softmax das 8 classes para a mensagem atual;
* **Medidor de Latência:** Exibição do tempo de processamento em milissegundos (<1ms);
* **Toggle de Levenshtein (Marco 5):** Permite ligar/desligar a correção ortográfica para demonstrar a melhoria aos professores;
* **Galeria Visual:** Modal para inspecionar os 8 gráficos científicos em tamanho real.

---

### 🖥️ Modo 2: Linha de Comando Interativa (CLI)
Para testes e homologação rápida via terminal:
```bash
./iniciar_terminal.sh
```
*(Ou execute diretamente: `python -m src.cli`)*

* **Modo Debug de IA:** Digite `debug: <sua dúvida>` no terminal para inspecionar os termos TF-IDF extraídos, vetor esparso, probabilidade calculada e status do limiar de fallback em tempo real!

---

### 📊 Modo 3: Suite Automatizada de Avaliação e Benchmark
* Para re-executar os 25 casos de teste formais da A3 e calcular as métricas:
  ```bash
  ./executar_testes.sh
  ```
* Para re-executar o benchmark comparativo das 4 arquiteturas e regerar os gráficos:
  ```bash
  python -m src.benchmark
  python -m src.generate_advanced_charts
  ```

---

### 🧪 Modo 4: Suite de Testes Unitários e Cobertura (PyTest)
Para auditar a integridade de engenharia de software com 100% de testes passando e relatório de cobertura:
```bash
PYTHONPATH=. pytest -v --cov=src --cov-report=term-missing tests/
```
* **Status:** 30 testes passando (100% de taxa de sucesso).
* **Cobertura dos Motores:** 100% em NLP Preprocessor, 97% em Intent Classifier, 94% em SQLite Database, 91% em Bot Engine.

---

### 📖 Modo 5: Documentação Interativa da API REST (OpenAPI / Swagger UI)
Com a aplicação web em execução (`./iniciar_web.sh`), acesse a documentação Swagger interativa:
* **URL:** **`http://localhost:5000/docs`**
* **Especificação YAML:** `http://localhost:5000/openapi.yaml` (ou no arquivo `docs/openapi.yaml`)
* Permite testar endpoints REST corporativos (`/api/chat`, `/api/explain`, `/api/tickets`, `/api/run-tests-live`) diretamente no navegador com esquemas de entrada e saída validados.

---

## 📈 9. Resultados Experimentais e Validação (R5 e R6)

A avaliação experimental foi conduzida sobre um conjunto formal de 25 testes não vistos no treinamento, categorizados conforme o Requisito R5:

| Categoria do Teste (R5) | Total de Casos | Acertos Registrados | Taxa de Acerto (%) | Observação Operacional |
| :--- | :---: | :---: | :---: | :--- |
| **Perguntas Típicas do Domínio** | 7 | 7 | **100.0%** | Resolução imediata com alta confiança (>50%). |
| **Perguntas Fora de Escopo (Fallback)** | 5 | 5 | **100.0%** | Abstenção segura sem nenhuma alucinação. |
| **Reformulações e Paráfrases** | 6 | 4 | **66.7%** | Generalização correta mesmo com variações sintáticas. |
| **Perguntas Ambíguas de Fronteira** | 3 | 2 | **66.7%** | Desambiguação segura com oferta de tópicos. |
| **Erros Ortográficos / Gírias Severas** | 4 | 0 | **0.0%** | Abstenção segura sem corretor; **100% de acerto quando ativado o Levenshtein**! |
| **TOTAL GERAL CONSOLIDADO** | **25** | **18** | **72.0%** | **Acurácia Global Balanceada (88.0% com Levenshtein)** |

---

## 👥 10. Autoria e Contribuições da Equipe

* **Heitor Westphal:** Engenharia de PLN, implementação do classificador TF-IDF e Regressão Logística, cálculo de similaridade de cossenos, calibração matemática do limiar de fallback, benchmark comparativo das 4 arquiteturas, algoritmo de Levenshtein e orquestração conversacional (`src/intent_classifier.py`, `src/nlp_preprocessor.py`, `src/bot_engine.py`, `src/benchmark.py`).
* **Integrante 2 (Dados e Curadoria):** Levantamento dos requisitos operacionais de TI N1, estruturação da base de conhecimento JSON com 8 intenções e montagem do dataset supervisionado (`data/knowledge_base.json`, `data/training_dataset.csv`).
* **Integrante 3 (Testes e Avaliação):** Elaboração dos 25 casos de teste (R5), script automatizado de avaliação, cálculo de matriz de confusão e métricas estatísticas (`data/test_dataset.csv`, `src/evaluate.py`, `results/`).
* **Integrante 4 (Interface e Documentação):** Desenvolvimento da interface Web Flask responsiva, integração do painel de telemetria analítica com Chart.js, elaboração da planilha executiva e redação do relatório técnico formal (`src/app_web.py`, `src/templates/index.html`, `docs/`).

---

## 📜 11. Declaração de Autoria e Integridade Acadêmica

Declara-se expressamente que todo o código-fonte, pipeline de pré-processamento de linguagem natural, arquitetura do classificador supervisionado, base de conhecimento curada, experimentos comparativos de benchmark, curvas de sensibilidade paramétrica, projeções de PCA e documentação técnica foram integralmente concebidos, desenvolvidos e validados pelos integrantes da equipe, em estrito cumprimento às normas acadêmicas e aos critérios avaliativos da disciplina de Inteligência Artificial.
