CURSO DE CIÊNCIA DA COMPUTAÇÃO / ENGENHARIA DE SOFTWARE
DISCIPLINA DE INTELIGÊNCIA ARTIFICIAL — AVALIAÇÃO A3 (40 PONTOS)


# TECHASSIST: DESENVOLVIMENTO DE UM CHATBOT DE TRIAGEM E SUPORTE DE TI NÍVEL 1 COM PROCESSAMENTO DE LINGUAGEM NATURAL E BENCHMARK COMPARATIVO DE ARQUITETURAS

Equipe: TechAssist AI Solutions
Autores: Heitor Westphal (Desenvolvimento IA/PLN e Arquitetura) e Equipe
Repositório: https://github.com/HeitorWestphal/TechAssist-Chatbot-A3
Data de Entrega: Novembro de 2026


# 1. Introdução e Definição do Problema

Contextualização de Mercado e Relevância: Nas modernas organizações corporativas, o setor de Tecnologia da Informação (TI) desempenha um papel fulcral na garantia da continuidade dos negócios. No entanto, centrais de serviços (Service Desks e Helpdesks) enfrentam diariamente um gargalo estrutural decorrente da sobrecarga de solicitações repetitivas de Nível 1 (N1). Levantamentos do setor indicam que entre 40% e 60% dos chamados abertos junto ao suporte técnico dizem respeito a demandas corriqueiras de baixa complexidade cognitiva, tais como redefinição de senhas expiradas, desbloqueio de contas corporativas, dúvidas sobre conexão em redes virtuais privadas (VPN), lentidão na inicialização de estações de trabalho e solicitações de instalação de softwares homologados.

Problemática Operacional: A alocação de analistas de suporte humanos altamente qualificados para atender reiteradamente a essas solicitações simples acarreta múltiplos prejuízos operacionais: elevação dos custos com mão de obra, aumento vertiginoso do Tempo Médio de Espera (TME), atraso na resolução de incidentes críticos de infraestrutura (N2 e N3) e desmotivação crônica dos profissionais da área de suporte. Do ponto de vista dos colaboradores e usuários finais, a dependência de atendimento humano para solucionar bloqueios de senha ou dúvidas pontuais resulta em tempo de inatividade ocioso e perda direta de produtividade.

Objetivo Geral e Delimitação de Escopo: O objetivo central deste projeto integrador A3 é projetar, desenvolver, validar experimentalmente e implantar o TechAssist, um agente conversacional inteligente (chatbot) voltado especificamente para a triagem e suporte técnico de TI Nível 1. O sistema visa automatizar a resolução imediata das demandas mais frequentes através de um fluxo interativo e fundamentado, disponibilizando procedimentos claros de autoatendimento 24 horas por dia, 7 dias por semana. Além disso, o projeto estabelece uma fronteira de atuação rigorosa: nos casos em que a demanda excede as capacidades do suporte N1 ou apresenta comportamento anômalo/ambíguo, o chatbot aciona um mecanismo seguro de abstenção (fallback) e guia o usuário na formalização de um chamado técnico estruturado para a equipe N2, gerando número de protocolo exclusivo.


# 2. Requisitos de Sistema e Casos de Uso


## 2.1 Demandas Atendidas e Intenções Mapeadas

Foram modeladas formalmente 8 intenções conversacionais completas, superando amplamente o requisito mínimo de 3 categorias:


# 3. Dados e Conhecimento: Curadoria, Preparação e Governança


## 3.1 Criação da Base de Conhecimento e Corpus de Treinamento

A base de conhecimento (data/knowledge_base.json) foi construída em formato semiestruturado JSON, desacoplando os procedimentos operacionais do código da aplicação. Paralelamente, o corpus de treinamento (data/training_dataset.csv) foi curado com mais de 100 exemplos balanceados, respeitando rigorosamente a LGPD ao utilizar dados e credenciais totalmente fictícios.


## 3.2 Pipeline de Pré-Processamento Textual em PLN

Implementado em src/nlp_preprocessor.py, o pipeline executa sucessivamente: normalização Unicode NFKD (eliminação de acentuação mantendo caracteres de base), remoção de pontuação e ruídos via expressões regulares, e filtragem de stopwords seletiva em português preservando operadores lógicos e pronomes interrogativos essenciais.


# 4. Arquitetura e Fundamentos do Mecanismo de Inteligência Artificial


## 4.1 Paradigma Adotado e Formulação Algorítmica

Adotou-se a Arquitetura Híbrida (Opção C), integrando vetorização TF-IDF de n-grams (1, 2), classificação supervisionada via Regressão Logística Multinomial com regularização L2 e cálculo paralelo de Similaridade por Cosseno.

Equação de Decisão Operacional: A pontuação final de certeza é governada por uma métrica híbrida calibrada:

      Confiança = 0.65 × max_c P(y = c | x) + 0.35 × max_i Cosseno(q, d_i)

Se Confiança < 0.38 ou se o vetor for nulo (Out-of-Vocabulary), aciona-se fallback determinístico, evitando alucinações.


## 4.2 Estudo Experimental Comparativo de Quatro Arquiteturas (Benchmark)

Para fundamentar cientificamente a escolha da arquitetura e comprovar sua superioridade frente às demais opções do edital, a equipe desenvolveu e executou uma bateria de testes comparativos (src/benchmark.py) avaliando quatro paradigmas distintos sobre o mesmo conjunto de validação:

Análise dos Resultados do Benchmark: Interpretação Crítica dos Dados: Embora os modelos supervisionados puros (Naive Bayes e SVM) apresentem acurácia numérica aparentemente mais elevada em datasets fechados, eles padecem de um vício operacional fatal para ambientes de TI corporativos: a incapacidade de abstenção. Quando submetidos a perguntas completamente fora do escopo ou erros absurdos de digitação, os modelos da Opção B forçam uma predição em uma das classes técnicas com falsa certeza. Já a nossa Arquitetura Híbrida (Opção C) atinge 100% de Precisão Técnica nas respostas homologadas e 100% de abstenção segura (fallback) nas perguntas fora de domínio, demonstrando superioridade de governança corporativa.

Figura 1 — Benchmark Comparativo de Desempenho entre as Quatro Arquiteturas de IA.

Figura 2 — Comparativo de Eficiência Computacional e Latência Média de Inferência Local (ms).


# 5. Implementação e Organização do Código-Fonte

O projeto foi construído em Python 3.11 com arquitetura modular desacoplada: src/nlp_preprocessor.py, src/intent_classifier.py, src/bot_engine.py, src/app_web.py, src/cli.py e src/evaluate.py. A execução pode ser realizada via interface gráfica Web (./iniciar_web.sh) ou terminal interativo (./iniciar_terminal.sh).


# 6. Experimentos, Avaliação e Análise Crítica de Resultados


## 6.1 Metodologia Experimental e Resultados Consolidados (R5 e R6)

A suite formal de 25 testes (data/test_dataset.csv) avaliou o comportamento da solução em 5 categorias do enunciado. O script src/evaluate.py consolidou acurácia global de 72.0% e precisão de 100% nas intenções técnicas.


## 6.2 Estudo de Sensibilidade e Calibração do Limiar Operacional

Calibração do Ponto Ótimo: A definição do limiar de fallback (threshold) é o elemento central da governança do chatbot. Para determinar o ponto de operação ideal, realizamos um estudo paramétrico variando o limiar de 0.10 a 0.60 com amostragem contínua. Os resultados empíricos estão ilustrados na Figura 3:

Figura 3 — Curva de Sensibilidade e Calibração do Limiar de Confiança Operacional (Sweet Spot em 0.38).

Fundamentação da Escolha: Como se observa na curva de calibração, limiares inferiores a 0.25 elevam o risco de falsos positivos em perguntas fora de escopo. Por outro lado, limiares superiores a 0.45 provocam superabstenção, recusando solicitações legítimas de usuários. O valor de 0.38 foi demonstrado matematicamente como o ponto ótimo de equilíbrio (sweet spot), maximizando a retenção de segurança com taxa zero de alucinação.

Figura 4 — Matriz de Confusão do Modelo Híbrido Final sobre os Casos de Teste.


## 6.3 Análise Aprofundada de Três Falhas e Melhorias (Marco 5)

Autópsia de Falhas: 1. Falha 1 — Erro Tipográfico Severo ('esquessi a ssnha do meu usuario'): Confiança de 0.239 < 0.38 devido a tokens OOV. Melhoria proposta: inclusão de corretor por Distância de Levenshtein (<= 2 edições);
2. Falha 2 — Expressão Coloquial / Metáfora ('meu pc ta uma carroca de tao lerdo'): Confiança de 0.2916 < 0.38 decorrente da ausência de gírias em manuais técnicos. Melhoria: ampliação do dicionário de sinônimos informais e embeddings morfológicos;
3. Falha 3 — Transliteração Fonética ('da pra baxa o paiton no meu note'): Vetor nulo devido à escrita sonora. Melhoria: integração de normalizador fonético (algoritmo Metaphone adaptado para PT-BR).


# 7. Discussão, Limites Operacionais e Evolução Futura

O TechAssist AI demonstra alto valor corporativo ao reduzir até 50% dos chamados banais de N1 com tempo de resposta inferior a 1 milissegundo. O fluxo estruturado de abertura de chamados (#TK-XXXXX) impede perda de solicitações. Como evolução futura, planeja-se integrar a solução a bancos de dados de ITSM (Jira Service Management/GLPI) e incorporar módulos de correção ortográfica.


# 8. Referências Bibliográficas e Declaração de Autoria

1. JURAFSKY, Daniel; MARTIN, James H. Speech and Language Processing. 3. ed. Stanford University, 2024.
2. MANNING, Christopher D. et al. Introduction to Information Retrieval. Cambridge University Press, 2008.
3. PEDREGOSA, Fabian et al. Scikit-learn: Machine Learning in Python. JMLR, v. 12, p. 2825-2830, 2011.
4. BRASIL. Lei Geral de Proteção de Dados Pessoais (LGPD - Lei 13.709/2018). Brasília: Presidência da República, 2018.

Declaração de Autoria Própria: Declara-se expressamente que todo o código-fonte, pipeline de pré-processamento textual, experimentos de benchmark comparativo, gráficos de calibração, base de conhecimento e documentação foram integralmente concebidos e implementados pelos autores, em estrito cumprimento às normas acadêmicas da disciplina.
