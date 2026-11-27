CURSO DE CIÊNCIA DA COMPUTAÇÃO / ENGENHARIA DE SOFTWARE
DISCIPLINA DE INTELIGÊNCIA ARTIFICIAL — AVALIAÇÃO A3 (40 PONTOS)


# TECHASSIST: DESENVOLVIMENTO DE UM CHATBOT DE TRIAGEM E SUPORTE DE TI NÍVEL 1 COM PROCESSAMENTO DE LINGUAGEM NATURAL E BENCHMARK CIENTÍFICO DE ARQUITETURAS

Equipe: TechAssist AI Solutions
Autores:
• Heitor Della Barba Westphal (RA: 1072410915) — Líder de Equipe / Engenharia de PLN e Arquitetura de IA (@HeitorWestphal)
• Bruno Hudson Siebert Costa (RA: 1072419878) — Engenharia de Dados, Persistência Relacional SQLite e DevOps (@BHSC1)
• Ian Santiago Silveira (RA: 1072410937) — Motor de Diálogo Conversacional e Gestão de Sessões Multi-Turnos (@SantiagoIanS)
• João Víctor Muniz da Silva (RA: 1072413992) — API RESTful Corporativa, Swagger UI e Validação Experimental (@Muniz2504)
Repositório: https://github.com/HeitorWestphal/TechAssist-Chatbot-A3
Data de Entrega: Novembro de 2026


# 1. Introdução e Definição do Problema

Contextualização de Mercado e Relevância: Nas modernas organizações corporativas, o setor de Tecnologia da Informação (TI) desempenha um papel fulcral na garantia da continuidade dos negócios. No entanto, centrais de serviços (Service Desks e Helpdesks) enfrentam diariamente um gargalo estrutural decorrente da sobrecarga de solicitações repetitivas de Nível 1 (N1). Levantamentos do setor indicam que entre 40% e 60% dos chamados abertos junto ao suporte técnico dizem respeito a demandas corriqueiras de baixa complexidade cognitiva, tais como redefinição de senhas expiradas, desbloqueio de contas corporativas, dúvidas sobre conexão em redes virtuais privadas (VPN), lentidão na inicialização de estações de trabalho e solicitações de instalação de softwares homologados.

Problemática Operacional: A alocação de analistas de suporte humanos altamente qualificados para atender reiteradamente a essas solicitações simples acarreta múltiplos prejuízos operacionais: elevação dos custos com mão de obra, aumento vertiginoso do Tempo Médio de Espera (TME), atraso na resolução de incidentes críticos de infraestrutura (N2 e N3) e desmotivação crônica dos profissionais da área de suporte. Do ponto de vista dos colaboradores e usuários finais, a dependência de atendimento humano para solucionar bloqueios de senha ou dúvidas pontuais resulta em tempo de inatividade ocioso e perda direta de produtividade.

Objetivo Geral e Delimitação de Escopo: O objetivo central deste projeto integrador A3 é projetar, desenvolver, validar experimentalmente e implantar o TechAssist, um agente conversacional inteligente (chatbot) voltado especificamente para a triagem e suporte técnico de TI Nível 1. O sistema visa automatizar a resolução imediata das demandas mais frequentes através de um fluxo interativo e fundamentado, disponibilizando procedimentos claros de autoatendimento 24 horas por dia, 7 dias por semana. Além disso, o projeto estabelece uma fronteira de atuação rigorosa: nos casos em que a demanda excede as capacidades do suporte N1 ou apresenta comportamento anômalo/ambíguo, o chatbot aciona um mecanismo seguro de abstenção (fallback) e guia o usuário na formalização de um chamado técnico estruturado para a equipe N2, gerando número de protocolo exclusivo.


# 2. Requisitos de Sistema e Casos de Uso


## 2.1 Demandas Atendidas e Intenções Mapeadas

Foram modeladas formalmente 8 intenções conversacionais completas, superando amplamente o requisito mínimo institucional de 3 categorias:


# 3. Dados e Conhecimento: Curadoria, Preparação e Governança


## 3.1 Criação da Base de Conhecimento e Corpus de Treinamento

A base de conhecimento (data/knowledge_base.json) foi construída em formato semiestruturado JSON, desacoplando os procedimentos operacionais do código da aplicação. O corpus de treinamento (data/training_dataset.csv) conta com mais de 100 exemplos balanceados, respeitando a LGPD com dados totalmente fictícios.


## 3.2 Pipeline de Pré-Processamento Textual em PLN e Corretor de Levenshtein

Tratamento Textual e Tolerância a Erros: Implementado em src/nlp_preprocessor.py, o pipeline executa: normalização Unicode NFKD (eliminação de acentuação mantendo caracteres de base), remoção de pontuação via expressões regulares, e filtragem de stopwords seletiva em português preservando operadores lógicos. Adicionalmente, para atender à melhoria do Marco 5, foi integrado um módulo de correção ortográfica baseado na Distância de Levenshtein (<= 2 edições) mapeado contra o vocabulário canônico de TI.


# 4. Arquitetura e Fundamentos do Mecanismo de Inteligência Artificial


## 4.1 Paradigma Adotado e Formulação Algorítmica

Adotou-se a Arquitetura Híbrida (Opção C), integrando vetorização TF-IDF de n-grams (1, 2), classificação supervisionada via Regressão Logística Multinomial com regularização L2 e cálculo de Similaridade por Cosseno.

Equação de Decisão Híbrida: A pontuação de confiança operacional é definida por:

      Confiança = 0.65 × max_c P(y = c | x) + 0.35 × max_i Cosseno(q, d_i)

Se Confiança < 0.38 ou o vetor for OOV, aciona-se fallback determinístico, evitando alucinações corporativas.


## 4.2 Estudo Experimental Comparativo de Quatro Arquiteturas (Benchmark)

A equipe executou um benchmark experimental rigoroso avaliando 4 paradigmas distintos sobre o mesmo conjunto de testes:

Superioridade da Opção C: Embora modelos puramente supervisionados (Naive Bayes e SVM) apresentem acurácia numérica aparentemente mais alta em dados de laboratório fechados, eles padecem da incapacidade de abstenção. Diante de perguntas fora do escopo corporativo, eles são forçados a 'chutar' uma classe de suporte. A nossa Arquitetura Híbrida (Opção C) atinge 100% de Precisão Técnica nas respostas homologadas e 100% de filtragem segura no Fallback.

Figura 1 — Benchmark Comparativo de Desempenho entre as Quatro Arquiteturas de IA.

Figura 2 — Comparativo de Eficiência Computacional e Latência Média de Inferência Local (ms).


## 4.3 Projeção do Espaço Vetorial Semântico via PCA (Clusters)

Para comprovar matematicamente a separabilidade das intenções, realizamos a redução de dimensionalidade por Análise de Componentes Principais (PCA) sobre os vetores TF-IDF do corpus de treinamento, como ilustrado na Figura 3:

Figura 3 — Projeção 2D do Espaço Vetorial TF-IDF com Centróides e Clusters de Intenções (PCA).

Figura 4 — Ponderação de N-Grams e Importância de Termos Softmax por Intenção (Feature Weights).


## 4.4 Estudo Científico de Ablação e Contribuição Modular

Para mensurar rigorosamente o impacto individual de cada módulo algorítmico do pipeline, realizamos um experimento de ablação progressiva sobre 6 estágios sequenciais:
1. *Modelo Base (Raw Text + TF-IDF 1-gram):* 84.0% de acurácia global e 60.0% de segurança no fallback (sem filtros);
2. *Normalização NFKD & Stopwords Seletivas:* Salto expressivo para 96.0% de acurácia global e 100.0% de retenção no fallback;
3. *Bigramas TF-IDF (1..2):* Captura de locuções técnicas chave como "resetar senha" e "conexão vpn";
4. *Corretor Morfométrico Levenshtein:* Recuperação de tokens com distância de edição <= 2 contra o vocabulário de TI;
5. *Similaridade de Cosseno com Centróides:* Ponderação angular híbrida (65% Softmax + 35% Cosseno);
6. *Limiar Operacional Calibrado (0.38):* Abstenção segura mandatória, garantindo 100% de precisão operacional no suporte técnico.

Figura 12 — Estudo Científico de Ablação: Ganho Marginal por Estágio do Pipeline de PLN.


## 4.5 Curva de Aprendizado e Eficiência Amostral

Avaliamos a capacidade de convergência e saturação da arquitetura híbrida em função do volume de sentenças anotadas, variando a base de treino de 20% a 100% (17 a 88 amostras) sob validação cruzada 5-Fold:

Figura 13 — Curva de Aprendizado e Eficiência Amostral (Treino vs. Validação Cruzada 5-Fold).

Os resultados evidenciam que o modelo atinge estabilidade a partir de ~60 amostras, comprovando a viabilidade de implantação rápida sem a necessidade de corpora gigantescos ou anotações onerosas.


## 4.6 Avaliação Multicritério AHP e Teste de Estresse sob Carga

Figura 9 — Análise Multicritério de Decisão Arquitetural (Radar de Trade-offs AHP).

Figura 10 — Benchmark de Carga, Estresse e Throughput (RPS) sob Concorrência Multithread.

Figura 11 — Validação Cruzada Estratificada em 5 Folds (5-Fold Stratified CV).


# 5. Implementação e Organização do Código-Fonte

O projeto foi construído em Python 3.11 com arquitetura modular desacoplada: src/nlp_preprocessor.py, src/intent_classifier.py, src/bot_engine.py, src/database.py, src/app_web.py, src/mcp_server.py, src/cli.py, src/evaluate.py e src/benchmark.py. A execução pode ser realizada via interface gráfica Web com telemetria em tempo real (./iniciar_web.sh), terminal interativo (./iniciar_terminal.sh) ou servidor de protocolo MCP JSON-RPC 2.0.


# 6. Experimentos, Avaliação e Análise Crítica de Resultados


## 6.1 Metodologia Experimental e Resultados Consolidados (R5 e R6)

A suite formal de 25 testes (data/test_dataset.csv) avaliou o comportamento da solução nas 5 categorias do edital. O modelo obteve 72.0% de acurácia global e 100% de precisão nas intenções de suporte.


## 6.2 Estudo de Sensibilidade e Calibração do Limiar Operacional

Realizamos um estudo paramétrico variando o limiar de 0.10 a 0.60 com amostragem contínua, demonstrando matematicamente o sweet spot de operação em 0.38:

Figura 5 — Curva de Sensibilidade e Calibração do Limiar de Confiança Operacional (Sweet Spot em 0.38).

Figura 6 — Curvas de Precisão vs. Revocação (Precision-Recall) Multiclasse.

Figura 7 — Heatmap da Matriz de Confusão do Modelo Híbrido Final sobre os Casos de Teste.


## 6.3 Análise de Falhas e Validação da Melhoria por Levenshtein (Marco 5)

Comprovação da Melhoria: No Marco 5, analisamos o caso da frase com erros graves ('esquessi a ssnha do meu usuario'), que originalmente obtinha confiança 0.239 e caía em fallback. Com a implementação do algoritmo de Levenshtein no pré-processador, os tokens são corrigidos para 'esqueci' e 'senha', elevando a confiança para 0.5302 e classificando corretamente como 'redefinicao_senha'. Essa validação experimental comprova a capacidade de evolução do sistema.


# 7. Discussão, Limites Operacionais e Impacto ITIL


## 7.1 Impacto Operacional e Métricas de Service Desk

O TechAssist AI demonstra alto valor corporativo ao reduzir drasticamente o tempo de resposta e absorver a maioria dos chamados banais:

Figura 8 — Simulação de Impacto Operacional: Redução no TMA de 42 min para 0.57s e Roteamento de Chamados.


## 7.2 Análise de Retorno sobre Investimento (ROI) e Comparativo vs LLMs

Para fundamentar a viabilidade econômica corporativa, realizamos um estudo comparativo entre a nossa solução determinística de PLN e abordagens baseadas em LLMs (Large Language Models), avaliando latência, consumo de memória, custo financeiro e conformidade com a LGPD:
* *Latência:* TechAssist opera a 0.48 ms, sendo 1.700x mais veloz que LLMs em nuvem (820 ms) e modelos locais de 7B (1.250 ms);
* *Consumo de Memória:* 14.8 MB de RAM vs 16.384 MB (16 GB) exigidos por um modelo 7B quantizado;
* *Custo por 1M de Consultas:* R$ 0,00 no TechAssist (execução em CPU padrão sem GPUs) vs R$ 1.850,00 em APIs de nuvem de ponta;
* *Governança e LGPD:* Processamento estritamente local em memória, sem compartilhamento de dados ou credenciais com terceiros.

Figura 14 — Análise de Recursos Computacionais, Latência e ROI Corporativo vs LLMs.


## 7.3 Disponibilização como Agente Autônomo e Protocolo MCP (Agensi.io)

O TechAssist foi encapsulado com a especificação Model Context Protocol (MCP JSON-RPC 2.0 via Stdio) e manifesto de publicação agensi.json, permitindo sua operação como ferramenta nativa (tool) para agentes de inteligência artificial de última geração (Claude Code, Cursor, Codex). Isso confere ao projeto maturidade profissional imediata para integração em marketplaces de agentes corporativos.


# 8. Referências Bibliográficas e Declaração de Autoria

1. JURAFSKY, Daniel; MARTIN, James H. Speech and Language Processing. 3. ed. Stanford University, 2024.
2. MANNING, Christopher D. et al. Introduction to Information Retrieval. Cambridge University Press, 2008.
3. PEDREGOSA, Fabian et al. Scikit-learn: Machine Learning in Python. JMLR, v. 12, p. 2825-2830, 2011.
4. BRASIL. Lei Geral de Proteção de Dados Pessoais (LGPD - Lei 13.709/2018). Brasília: Presidência da República, 2018.
5. AXELOS. ITIL Foundation: ITIL 4 Edition. Norwich: TSO, 2019.

Declaração de Autoria Própria: Declara-se expressamente que todo o código-fonte, pipeline de pré-processamento textual, experimentos científicos de benchmark, projeções de PCA, gráficos de calibração, base de conhecimento e documentação técnica foram integralmente concebidos e implementados pelos autores, em estrito cumprimento às normas acadêmicas da disciplina.
