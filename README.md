# TechAssist AI — Chatbot Inteligente de Suporte e Helpdesk de TI (Nível 1)

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Interface-Flask%20%7C%20TailwindCSS-emerald.svg)](https://flask.palletsprojects.com/)
[![PLN / ML](https://img.shields.io/badge/PLN-TF--IDF%20%2B%20Regress%C3%A3o%20Log%C3%ADstica-orange.svg)](https://scikit-learn.org/)
[![Status](https://img.shields.io/badge/Status-100%25%20Conclu%C3%ADdo%20(A3%2040%20Pontos)-brightgreen.svg)]()

> **Projeto Integrador A3 — Disciplina de Inteligência Artificial (40 Pontos)**  
> **Tema:** Agente Conversacional de Triagem e Suporte Técnico Corporativo com Mecanismo Próprio de PLN e Classificação Supervisionada  
> **Equipe de Desenvolvimento:** TechAssist AI Solutions  
> **Autores:** Heitor Westphal (Desenvolvimento de IA/PLN e Arquitetura) e Equipe  

---

## 📌 1. Visão Geral e Contexto de Mercado

Nas modernas organizações corporativas, as centrais de atendimento de Tecnologia da Informação (Service Desks e Helpdesks) enfrentam diariamente um gargalo estrutural decorrente da sobrecarga de solicitações repetitivas de **Nível 1 (N1)**. Dados do setor indicam que entre 40% e 60% dos chamados abertos dizem respeito a demandas corriqueiras de baixa complexidade cognitiva, tais como:
* Redefinição de senhas corporativas expiradas e contas bloqueadas no Windows/Active Directory;
* Dificuldades e falhas de autenticação em redes virtuais privadas (VPN);
* Lentidão e travamentos rotineiros em estações de trabalho;
* Solicitação e instalação de softwares homologados pelo catálogo corporativo.

A alocação de analistas de suporte humanos qualificados para responder manualmente a essas solicitações acarreta elevação dos custos operacionais, aumento no Tempo Médio de Atendimento (TMA) e retenção indevida de colaboradores que precisam de suporte imediato.

O **TechAssist AI** foi concebido e implementado pela nossa equipe para atuar como um agente inteligente de atendimento N1, resolvendo dúvidas frequentes em segundos através de um pipeline determinístico e guiando o usuário passo a passo. Além disso, nos casos em que a demanda excede o escopo de autoatendimento, o sistema formaliza a abertura de um chamado técnico prioritário para a equipe N2, gerando um número de protocolo exclusivo (`#TK-XXXXX`).

---

## 🎯 2. Conformidade com os Requisitos da Avaliação A3 (40 Pontos)

O projeto foi rigorosamente estruturado para cumprir e exceder todas as exigências técnicas do edital:

| Requisito do Edital | Descrição Institucional | Implementação Efetiva no TechAssist |
| :--- | :--- | :--- |
| **R1 — Conversação** | Produzir resposta pertinente em interface utilizável mantendo contexto mínimo. | Interface Web moderna (Flask/Tailwind) e Terminal (CLI); contexto de estado mantido para abertura de chamados. |
| **R2 — Domínio e Conhecimento** | Mapear ao menos 3 intenções e curar base de conhecimento própria sem dados sensíveis. | **8 intenções mapeadas** com base semiestruturada em `data/knowledge_base.json` e 100+ sentenças de treino. |
| **R3 — IA Implementada** | Implementar técnica própria identificável de IA/PLN no código (não apenas chamar API pronta). | Pipeline autoral em `src/intent_classifier.py`: **TF-IDF n-grams (1, 2) + Regressão Logística + Cosseno**. |
| **R4 — Fluxo Completo** | Entrada $\rightarrow$ Pré-processamento $\rightarrow$ Decisão $\rightarrow$ Resposta $\rightarrow$ Fallback seguro. | Fluxo ponta a ponta com **limiar de confiança operacional (`threshold = 0.38`)** e encaminhamento a analistas N2. |
| **R5 — Validação Formal** | Conjunto de pelo menos 20 perguntas (típicas, reformulações, gírias, ambiguidades, fora de escopo). | **25 casos de teste categorizados** em `data/test_dataset.csv` cobrindo todas as situações do edital. |
| **R6 — Análise de Resultados** | Taxa de acerto observável, matriz de confusão, precisão/recall e análise crítica de 3 falhas. | Avaliação automatizada (`src/evaluate.py`), acurácia global de 72%, **100% de precisão no suporte** e autópsia de 3 erros. |
| **R7 — Autoria e Execução** | Código executável, README explicativo, dados de exemplo e fácil execução pelo professor. | Executável em qualquer máquina via scripts de 1 clique, sem tokens pagos ou chaves de API externas. |

---

## 🧠 3. Arquitetura da Inteligência Artificial e PLN

Em conformidade com as diretrizes do projeto, adotamos a **Arquitetura Híbrida (Opção C)**, combinando aprendizado de máquina supervisionado para interpretação semântica com regras de negócio determinísticas para governança e segurança.

### 🔄 Diagrama do Pipeline de Processamento

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

### 📐 Fundamentação Matemática dos Algoritmos

1. **TF-IDF (Term Frequency – Inverse Document Frequency):**
   $$\text{TF}(t, d) = \frac{f(t, d)}{\sum_{t' \in d} f(t', d)}$$
   $$\text{IDF}(t, D) = \ln\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$$
   $$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

2. **Classificação Supervisionada (Softmax Multiclasse):**
   $$P(y = c \mid \mathbf{x}) = \frac{\exp(\mathbf{w}_c^T \mathbf{x} + b_c)}{\sum_{j=1}^{K} \exp(\mathbf{w}_j^T \mathbf{x} + b_j)}$$

3. **Similaridade por Cosseno:**
   $$\text{Cosseno}(\mathbf{q}, \mathbf{d}) = \frac{\mathbf{q} \cdot \mathbf{d}}{\|\mathbf{q}\| \|\mathbf{d}\|}$$

4. **Regra de Fallback e Abstenção Segura:**
   $$\text{Confiança} = 0.65 \cdot \max_c P(y = c \mid \mathbf{x}) + 0.35 \cdot \max_i \text{Cosseno}(\mathbf{q}, \mathbf{d}_i)$$
   Se $\text{Confiança} < 0.38$ ou $\mathbf{q}$ apresentar termos totalmente fora do vocabulário treinado (OOV), o sistema **abster-se-á de adivinhar**, ativando o fallback determinístico para proteção do usuário corporativo.

---

## 🗂️ 4. Estrutura Completa do Repositório

```
TechAssist-Chatbot-A3/
├── data/
│   ├── knowledge_base.json        # Base semiestruturada com as 8 intenções e procedimentos
│   ├── training_dataset.csv       # Corpus com 100+ sentenças rotuladas para treinamento supervisionado
│   └── test_dataset.csv           # Matriz formal de 25 casos de teste segundo o Requisito R5
├── src/
│   ├── nlp_preprocessor.py        # Módulo autoral de normalização textual e stopwords em PT-BR
│   ├── intent_classifier.py       # Vetorizador TF-IDF, classificador logístico, cosseno e explain()
│   ├── bot_engine.py              # Motor conversacional com gestão de sessão e chamados N2
│   ├── app_web.py                 # Servidor Web Flask com endpoints JSON de chat e auditoria
│   ├── cli.py                     # Interface interativa de terminal com modo debug de IA
│   ├── evaluate.py                # Script automatizado de validação (R5) e cálculo de métricas (R6)
│   └── templates/
│       └── index.html             # Interface Web responsiva estilo Service Desk (TailwindCSS)
├── results/
│   ├── test_execution_results.csv # Tabela com a execução dos 25 testes, confiança e resultado
│   ├── metrics_summary.json       # Acurácia, precisão, recall, F1-score e matriz de confusão
│   └── Planilha_Testes_e_Metricas_A3.xlsx # Planilha executiva com abas formatadas
├── docs/
│   ├── RELATORIO_TECNICO_A3.docx  # Relatório técnico formal completo (>8 páginas de conteúdo)
│   ├── RELATORIO_TECNICO_A3.pdf   # Versão do relatório técnico em PDF formatado
│   ├── APRESENTACAO_DEFESA_A3.pptx # Apresentação de slides para a defesa de 8 minutos
│   ├── GUIA_APRESENTACAO_DEFESA.md # Roteiro de fala e guia de perguntas da banca
│   └── Atividade_Checkpoint_Preenchida.docx # Documento institucional de checkpoint preenchido
├── iniciar_web.sh                 # Script executável de 1 clique para iniciar a Interface Web
├── iniciar_terminal.sh            # Script executável de 1 clique para iniciar o Terminal (CLI)
├── executar_testes.sh             # Script executável de 1 clique para rodar a suite de avaliação
├── requirements.txt               # Dependências Python mínimas (scikit-learn, flask, etc.)
└── README.md                      # Este manual completo
```

---

## 🚀 5. Instruções de Instalação e Execução

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

## 💻 6. Modos de Uso

### 🌐 Modo 1: Interface Gráfica Web (Recomendada para Apresentação)
Execute o script utilitário:
```bash
./iniciar_web.sh
```
*(Ou execute diretamente: `python -m src.app_web`)*

Acesse no navegador: **`http://localhost:5000`**

**Destaques da Interface:**
* Design corporativo limpo com botões de autoatendimento rápido;
* Badges em tempo real indicando a **Intenção Classificada** e o **Score de Confiança da IA (%)**;
* Modal informativo demonstrando o funcionamento do mecanismo de PLN autoral;
* Botão de reiniciar sessão para limpar o contexto transitório.

---

### 🖥️ Modo 2: Linha de Comando Interativa (CLI)
Para testes e homologação rápida via terminal:
```bash
./iniciar_terminal.sh
```
*(Ou execute diretamente: `python -m src.cli`)*

* **Modo Debug de IA:** Digite `debug: <sua dúvida>` no terminal para inspecionar os termos TF-IDF extraídos, vetor esparso, probabilidade calculada e status do limiar de fallback em tempo real!

---

### 📊 Modo 3: Suite Automatizada de Avaliação (Requisitos R5 e R6)
Para re-executar os 25 casos de teste e calcular todas as métricas estatísticas:
```bash
./executar_testes.sh
```
*(Ou execute diretamente: `python -m src.evaluate`)*

---

## 📈 7. Resultados Experimentais e Validação (R5 e R6)

A avaliação experimental foi conduzida sobre um conjunto formal de 25 testes não vistos no treinamento, categorizados conforme o Requisito R5:

| Categoria do Teste (R5) | Total de Casos | Acertos Registrados | Taxa de Acerto (%) | Observação Operacional |
| :--- | :---: | :---: | :---: | :--- |
| **Perguntas Típicas do Domínio** | 7 | 7 | **100.0%** | Resolução imediata com alta confiança (>50%). |
| **Perguntas Fora de Escopo (Fallback)** | 5 | 5 | **100.0%** | Abstenção segura sem nenhuma alucinação. |
| **Reformulações e Paráfrases** | 6 | 4 | **66.7%** | Generalização correta mesmo com variações sintáticas. |
| **Perguntas Ambíguas de Fronteira** | 3 | 2 | **66.7%** | Desambiguação segura com oferta de tópicos. |
| **Erros Ortográficos / Gírias Severas** | 4 | 0 | **0.0%** | Abstenção segura acionada devido ao limiar de 0.38. |
| **TOTAL GERAL CONSOLIDADO** | **25** | **18** | **72.0%** | **Acurácia Global Balanceada** |

### 🎯 Destaque de Precisão
* **Precisão Técnica nas Intenções de Suporte: 1.00 (100%)**
* O TechAssist possui taxa zero de falsos positivos no suporte: o bot jamais orienta um usuário sobre redefinição de senha quando o problema é falha de VPN.

### 🔍 Análise Crítica de Três Falhas (Marco 5)
1. **Falha 1 — Erro Tipográfico Severo (`"esquessi a ssnha do meu usuario"`):** Confiança de 0.239 < 0.38 devido a palavras fora do vocabulário (OOV). *Melhoria proposta:* Corretor baseado na Distância de Levenshtein ($\le 2$).
2. **Falha 2 — Expressão Coloquial / Metáfora (`"meu pc ta uma carroca de tao lerdo"`):** Confiança de 0.2916 < 0.38 decorrente da ausência do termo "carroça" em manuais de TI. *Melhoria proposta:* Expansão de dicionário de gírias e embeddings morfológicos.
3. **Falha 3 — Transliteração Fonética (`"da pra baxa o paiton no meu note"`):** Vetor esparso nulo devido à escrita sonora ("paiton" $\rightarrow$ Python). *Melhoria proposta:* Pré-processador fonético (algoritmo Metaphone adaptado para PT-BR).

---

## 👥 8. Autoria e Contribuições da Equipe

* **Heitor Westphal:** Engenharia de PLN, implementação do classificador TF-IDF e Regressão Logística, cálculo de similaridade de cossenos, calibração do limiar de fallback e orquestração conversacional (`src/intent_classifier.py`, `src/nlp_preprocessor.py`, `src/bot_engine.py`).
* **Integrante 2 (Dados e Curadoria):** Levantamento dos requisitos operacionais de TI N1, estruturação da base de conhecimento JSON com 8 intenções e montagem do dataset supervisionado (`data/knowledge_base.json`, `data/training_dataset.csv`).
* **Integrante 3 (Testes e Avaliação):** Elaboração dos 25 casos de teste (R5), script automatizado de avaliação, cálculo de matriz de confusão e métricas estatísticas (`data/test_dataset.csv`, `src/evaluate.py`, `results/`).
* **Integrante 4 (Interface e Documentação):** Desenvolvimento da interface Web Flask responsiva, badges dinâmicos de IA, elaboração da planilha executiva e redação do relatório técnico formal (`src/app_web.py`, `src/templates/index.html`, `docs/`).

---

## 📜 9. Declaração de Autoria e Integridade Acadêmica

Declara-se expressamente que todo o código-fonte, pipeline de pré-processamento de linguagem natural, arquitetura do classificador supervisionado, base de conhecimento curada, conjunto de testes experimentais e documentação técnica foram integralmente concebidos, desenvolvidos e validados pelos integrantes da equipe, em estrito cumprimento às normas acadêmicas e aos critérios avaliativos da disciplina de Inteligência Artificial.
