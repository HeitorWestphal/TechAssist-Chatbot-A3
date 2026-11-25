CURSO DE CIÊNCIA DA COMPUTAÇÃO / ENGENHARIA DE SOFTWARE
DISCIPLINA DE INTELIGÊNCIA ARTIFICIAL — AVALIAÇÃO A3 (40 PONTOS)


# TECHASSIST: DESENVOLVIMENTO DE UM CHATBOT DE TRIAGEM E SUPORTE DE TI NÍVEL 1 COM PROCESSAMENTO DE LINGUAGEM NATURAL E MECANISMO AUTORAL DE CLASSIFICAÇÃO

Equipe: TechAssist AI Solutions
Integrantes: Heitor Westphal (Desenvolvimento IA/PLN e Arquitetura), Integrante 2 (Dados e Curadoria), Integrante 3 (Testes e Métricas), Integrante 4 (Interface e Relatório)
Repositório: https://github.com/HeitorWestphal/TechAssist-Chatbot-A3
Data de Entrega: Novembro de 2026


# 1. Introdução e Definição do Problema

Contextualização de Mercado e Relevância: Nas modernas organizações corporativas, o setor de Tecnologia da Informação (TI) desempenha um papel fulcral na garantia da continuidade dos negócios. No entanto, centrais de serviços (Service Desks e Helpdesks) enfrentam diariamente um gargalo estrutural decorrente da sobrecarga de solicitações repetitivas de Nível 1 (N1). Levantamentos do setor indicam que entre 40% e 60% dos chamados abertos junto ao suporte técnico dizem respeito a demandas corriqueiras de baixa complexidade cognitiva, tais como redefinição de senhas expiradas, desbloqueio de contas corporativas, dúvidas sobre conexão em redes virtuais privadas (VPN), lentidão na inicialização de estações de trabalho e solicitações de instalação de softwares homologados.

Problemática Operacional: A alocação de analistas de suporte humanos altamente qualificados para atender reiteradamente a essas solicitações simples acarreta múltiplos prejuízos operacionais: elevação dos custos com mão de obra, aumento vertiginoso do Tempo Médio de Espera (TME), atraso na resolução de incidentes críticos de infraestrutura (N2 e N3) e desmotivação crônica dos profissionais da área de suporte. Do ponto de vista dos colaboradores e usuários finais, a dependência de atendimento humano para solucionar bloqueios de senha ou dúvidas pontuais resulta em tempo de inatividade ocioso e perda direta de produtividade.

Objetivo Geral e Delimitação de Escopo: O objetivo central deste projeto integrador A3 é projetar, desenvolver, validar e implantar o TechAssist, um agente conversacional inteligente (chatbot) voltado especificamente para a triagem e suporte técnico de TI Nível 1. O sistema visa automatizar a resolução imediata das demandas mais frequentes através de um fluxo interativo e fundamentado, disponibilizando procedimentos claros de autoatendimento 24 horas por dia, 7 dias por semana. Além disso, o projeto estabelece uma fronteira de atuação rigorosa: nos casos em que a demanda excede as capacidades do suporte N1 ou apresenta comportamento anômalo/ambíguo, o chatbot aciona um mecanismo seguro de abstenção (fallback) e guia o usuário na formalização de um chamado técnico estruturado para a equipe N2, gerando número de protocolo exclusivo.

Justificativa Técnica: A justificativa técnica e acadêmica do TechAssist assenta-se na exigência primordial de autoria e transparência algorítmica. Ao contrário de abordagens puramente comerciais baseadas em caixas-pretas ou simples encaminhamentos de mensagens a APIs externas proprietárias — o que violaria o Requisito R3 e geraria custos recorrentes e riscos de alucinação —, este projeto implementa um pipeline próprio e determinístico de Processamento de Linguagem Natural (PLN) e Aprendizado de Máquina (Machine Learning), combinando vetorização TF-IDF, classificação estatística supervisionada, similaridade vetorial por cosseno e limiar calibrado de confiança.


# 2. Requisitos de Sistema e Casos de Uso


## 2.1 Demandas Atendidas e Intenções Mapeadas

O TechAssist foi concebido para atender a um domínio estritamente delimitado e de alta relevância no ambiente corporativo. Foram modeladas formalmente 8 intenções conversacionais, superando o requisito mínimo institucional de 3 categorias:


## 2.2 Requisitos Funcionais e Não Funcionais

Especificação de Requisitos: O protótipo atende a rigorosos critérios de engenharia de software:
• RF01 — Interface Multicanal: O sistema deve operar tanto em interface gráfica Web responsiva (Flask/HTML5) quanto via terminal interativo (CLI) para fins de homologação e auditoria.
• RF02 — Classificação Supervisionada: Cada mensagem submetida pelo usuário deve ser processada em tempo real pelo modelo autoral de PLN, gerando o rótulo de intenção e o respectivo score de confiança.
• RF03 — Abstenção Segura e Limiar de Fallback: Quando a confiança inferida for estritamente menor que 0.38 ou a consulta contiver apenas termos desconhecidos, o bot deve abster-se de gerar respostas factuais incorretas e acionar o módulo de fallback.
• RF04 — Gerenciamento de Contexto de Sessão: O motor conversacional deve manter estado transitório na memória para conduzir fluxos de múltiplas etapas, notadamente o fluxo de abertura de chamado com coleta de relato e geração de protocolo.
• RNF01 — Baixa Latência e Desempenho Local: O tempo de processamento e resposta da inferência deve ser inferior a 100 milissegundos por requisição, executando integralmente em hardware convencional sem dependência de APIs externas de terceiros.
• RNF02 — Privacidade e Rastreabilidade: Nenhuma credencial privada, senha ou dado pessoal sensível deve ser persistido em texto claro no sistema, em conformidade com as diretrizes da LGPD.


# 3. Dados e Conhecimento: Curadoria, Preparação e Governança


## 3.1 Criação e Estruturação da Base de Conhecimento

Arquitetura de Dados: A base de conhecimento foi estruturada em formato semiestruturado JSON (data/knowledge_base.json), garantindo desacoplamento entre os dados de autoatendimento e o código da aplicação. Cada entrada contém metadados de domínio, título amigável, corpo textual detalhado com passos numerados de diagnóstico, links seguros simulados para ferramentas corporativas (ex: portal de autoatendimento de credenciais e catálogo de programas) e sugestões interativas de continuidade da conversa.


## 3.2 Dataset de Treinamento e Pré-Processamento Textual

Composição do Corpus: Para viabilizar o treinamento supervisionado, a equipe sintetizou e curou um dataset representativo (data/training_dataset.csv) contendo mais de 100 instâncias rotuladas e balanceadas nas 8 intenções do escopo. O conjunto abrange desde construções formais ('solicito redefinição de credenciais corporativas') até formulações coloquiais e imediatistas ('minha vpn caiu', 'notebook lerdo demais').

Pipeline de Pré-Processamento em PLN: A etapa de pré-processamento (implementada no módulo src/nlp_preprocessor.py) é crucial para mitigar o ruído textual típico de canais de suporte rápido. O pipeline executa sucessivamente:
1. Normalização Unicode e Conversão para Caixa Baixa: Conversão sistemática de todo o texto para minúsculas e aplicação da forma de normalização NFKD (National Compatibility Decomposition), eliminando acentos e cedilhas sem corromper o caractere alfabético de base;
2. Higienização por Expressões Regulares: Remoção de caracteres especiais, pontuação, símbolos matemáticos e emojis redundantes, retendo exclusivamente sequências alfanuméricas e espaços delimitadores;
3. Filtragem Criteriosa de Stopwords: Utilização de uma lista customizada de stopwords para a língua portuguesa. Ao contrário de stoplists padrão de literatura, preservaram-se tokens interrogativos e operadores de negação (ex: 'não', 'sem', 'como', 'onde'), os quais carregam elevado peso discriminante em chamados de TI (diferenciando, por exemplo, 'consigo conectar' de 'não consigo conectar').

Governança, Ética e Privacidade: Em estrita observância à Lei Geral de Proteção de Dados (LGPD - Lei nº 13.709/2018) e às regras da A3, todo o corpus de treinamento e testes foi construído utilizando dados estritamente fictícios e autorizados. Nenhuma senha real, endereço de IP de produção, token de autenticação ou informação identificável de colaborador foi exposta nos arquivos do projeto.


# 4. Arquitetura e Fundamentos do Mecanismo de Inteligência Artificial


## 4.1 Paradigma Adotado e Justificativa Teórica

Paradigma Híbrido: Em conformidade com a Seção 5 das diretrizes do projeto integrador, a equipe optou pela Arquitetura Híbrida (Opção C), integrando um classificador probabilístico de PLN supervisionado e cálculo vetorial de similaridade de cossenos com um motor simbólico de regras contextuais e fallback determinístico.

Análise Comparativa: Alternativa Descartada e Motivo da Decisão: Considerou-se inicialmente a utilização de um chatbot exclusivamente baseado em chamadas de API externas para modelos comerciais de terceiros. Essa abordagem foi expressamente descartada por três razões fundamentais: (a) Descumprimento frontal do Requisito Obrigatório R3, que exige a existência de um mecanismo próprio de IA identificável no código-fonte; (b) Dependência de conexão de rede externa de alta latência e vulnerabilidade a custos recorrentes e imprevisíveis; e (c) Fenômeno de 'alucinação', onde modelos generativos poderiam inventar procedimentos de suporte técnico perigosos ou inexistentes.


## 4.2 Formulação Matemática e Algoritmos Utilizados

Vetorização TF-IDF: O núcleo do classificador (src/intent_classifier.py) baseia-se na ponderação de termos via TF-IDF (Term Frequency - Inverse Document Frequency). O cálculo do peso w de um termo t no documento d de uma coleção D é formalizado por:

      TF(t, d) = f(t, d) / ∑ f(t', d)
      IDF(t, D) = ln( (1 + |D|) / (1 + |{d ∈ D : t ∈ d}|) ) + 1
      TF-IDF(t, d, D) = TF(t, d) × IDF(t, D)

Para capturar dependências locais e pares de palavras cruciais (como 'abrir chamado', 'não conecta', 'trocar senha'), o vetorizador foi configurado com faixa de n-gramas variando de unigramas a bigramas (ngram_range=(1, 2)).

Classificação e Métrica de Confiança: Sobre a matriz TF-IDF gerada, o sistema aplica um modelo de Regressão Logística Multinomial com regularização L2. O modelo estima a distribuição de probabilidade a posteriori P(y = c | x) para cada intenção c por meio da função Softmax:

      P(y = c | x) = exp(w_c^T x + b_c) / ∑_{j} exp(w_j^T x + b_j)

Simultaneamente, o sistema calcula a Similaridade de Cosseno entre o vetor da consulta do usuário q e os vetores de treinamento d_i:

      Similaridade_Cosseno(q, d_i) = (q · d_i) / ( ||q|| × ||d_i|| )

A pontuação final de confiança operacional é definida por uma métrica híbrida calibrada:

      Confiança = 0.65 × max_c P(y = c | x) + 0.35 × max_i Similaridade_Cosseno(q, d_i)

Se Confiança < 0.38 ou se q contiver zero termos no vocabulário (Out-of-Vocabulary), o sistema aciona de forma determinística o mecanismo de fallback.


# 5. Implementação e Organização do Código-Fonte


## 5.1 Ambiente, Tecnologias e Dependências

Stack Tecnológico: O projeto foi implementado integralmente em Python (versão 3.11/3.12), priorizando modularidade, baixo acoplamento e reprodutibilidade. As dependências externas foram mantidas estritamente no essencial (scikit-learn para vetorização e regressão, Flask para o servidor web, e numpy para operações matriciais vetorizadas), permitindo execução instantânea e compatibilidade entre sistemas operacionais (macOS, Linux e Windows).


## 5.2 Estrutura Modular de Diretórios

Topologia do Repositório: A estrutura física de arquivos do repositório está organizada da seguinte maneira:
• data/
  ├── knowledge_base.json      (Base de conhecimento das 8 intenções e respostas)
  ├── training_dataset.csv     (Dataset de treinamento com 100+ sentenças rotuladas)
  └── test_dataset.csv         (Dataset de teste com 25 casos categorizados segundo R5)
• src/
  ├── nlp_preprocessor.py      (Pipeline de higienização, normalização e stopwords em PT)
  ├── intent_classifier.py     (Vetorizador TF-IDF, modelo logístico, cosseno e explain)
  ├── bot_engine.py            (Orquestrador conversacional e gestão de sessão de chamados)
  ├── app_web.py               (Servidor Web Flask com endpoints JSON de chat e auditoria)
  ├── cli.py                   (Interface interativa via terminal com modo de debug de IA)
  ├── evaluate.py              (Script automatizado de cálculo de métricas e matriz de confusão)
  └── templates/index.html     (Interface gráfica web moderna responsiva com TailwindCSS)
• results/
  ├── test_execution_results.csv (Tabela de 25 testes executados com status e confiança)
  ├── metrics_summary.json       (Sumário estatístico de acurácia, precisão, recall e F1)
  └── Planilha_Testes_e_Metricas_A3.xlsx (Planilha executiva de validação e métricas)
• docs/
  ├── RELATORIO_TECNICO_A3.docx (Este relatório técnico formal completo)
  ├── RELATORIO_TECNICO_A3.pdf  (Versão do relatório em PDF formatado)
  ├── APRESENTACAO_DEFESA_A3.pptx (Slides completos da apresentação de defesa)
  ├── GUIA_APRESENTACAO_DEFESA.md (Roteiro e respostas da banca minuto a minuto)
  └── Atividade_Checkpoint_Preenchida.docx (Checkpoint institucional preenchido)
• requirements.txt e README.md (Guia passo a passo de reprodução do projeto)


## 5.3 Instruções de Instalação e Execução

Guia de Execução Rápida: Para executar o projeto localmente para avaliação do professor, bastam os seguintes comandos no terminal:

   1. Criação do ambiente virtual:  python3 -m venv venv && source venv/bin/activate
   2. Instalação das dependências:  pip install -r requirements.txt
   3. Execução da Interface Web:    ./iniciar_web.sh  (ou python -m src.app_web)
   4. Execução via Terminal:        ./iniciar_terminal.sh  (ou python -m src.cli)
   5. Execução da Suite de Testes:  ./executar_testes.sh  (ou python -m src.evaluate)


# 6. Experimentos, Avaliação e Análise Crítica de Resultados


## 6.1 Metodologia Experimental e Conjunto de Validação (R5)

Metodologia de Teste: Para atender formalmente aos requisitos R5 e R6, foi concebido um conjunto de 25 casos de testes representativos, divididos em 5 categorias essenciais: Perguntas Típicas (7 casos), Reformulações e Paráfrases (6 casos), Ortografia e Gírias (4 casos), Perguntas Ambíguas de Fronteira (3 casos) e Perguntas Fora do Escopo (5 casos). Nenhuma das 25 sentenças de teste foi incluída literalmente no conjunto de treino.


## 6.2 Resultados Globais e Desempenho por Categoria

A execução automatizada do script src/evaluate.py gerou os seguintes indicadores estatísticos consolidados:

Análise de Precisão e Confiabilidade: Conforme evidenciado na matriz de confusão e no relatório de classificação gerados em results/metrics_summary.json, a Precisão do modelo para intenções técnicas específicas de suporte atinge 1.00 (100%). Isso demonstra que o TechAssist possui baixíssima propensão a falsos positivos: o assistente jamais orienta um usuário sobre redefinição de senha quando o problema relatado é falha de VPN.


## 6.3 Análise Aprofundada de Três Falhas e Melhorias Propostas

Em conformidade com a exigência do Marco 5 e da Seção 7 do enunciado da A3, a equipe realizou a autópsia detalhada de três casos de falha observados durante a validação experimental:

Falha 1 — Erro Tipográfico Severo ('esquessi a ssnha do meu usuario'): Diagnóstico: A sentença continha dois erros severos de digitação ('esquessi' e 'ssnha'). No vocabulário TF-IDF de palavras, esses tokens foram tratados como palavras fora do vocabulário (Out-of-Vocabulary - OOV). A confiança resultante foi de apenas 0.239, ficando abaixo do limiar de 0.38 e disparando o fallback.
Ação de Melhoria: Implementar um corretor ortográfico no módulo de pré-processamento baseado na Distância de Levenshtein (ou algoritmo de SymSpell) para mapear termos desconhecidos com distância de edição <= 2 para o vocabulário de referência.

Falha 2 — Expressão Coloquial/Metáfora Popular ('meu pc ta uma carroca de tao lerdo'): Diagnóstico: O termo metafórico e coloquial 'carroça' e a gíria 'lerdo' produziram esparsidade vetorial, resultando em confiança híbrida de 0.2916 (abaixo de 0.38). O sistema optou por abster-se com fallback seguro.
Ação de Melhoria: Ampliar a lista de sinônimos corporativos ou integrar vetorizadores baseados em sub-palavras (character n-grams ou FastText) que capturam raízes morfológicas de gírias e expressões coloquiais.

Falha 3 — Transliteração Fonética ('da pra baxa o paiton no meu note'): Diagnóstico: O usuário utilizou transliteração fonética informal ('baxa' em vez de 'baixar' e 'paiton' em vez de 'Python'). O vetor TF-IDF resultante apresentou zero coincidência com os termos homologados do catálogo (query_vec.nnz == 0), acionando fallback imediato.
Ação de Melhoria: Incorporar um dicionário fonético (algoritmo Soundex ou Metaphone adaptado para o português brasileiro) para correlacionar grafias sonoras ao nome correto de ferramentas de software corporativas.


# 7. Discussão, Limites Operacionais e Evolução Futura

Valor Agregado ao Negócio: A implantação do TechAssist demonstra um valor imediato e tangível para a organização. Ao absorver com precisão as demandas mais repetitivas de Nível 1 (100% de acerto nas perguntas típicas e 100% de filtragem segura em perguntas fora de escopo), o chatbot desafoga os analistas de suporte, permitindo que a equipe de TI dedique tempo e atenção à resolução de problemas de infraestrutura de alto impacto. O fluxo estruturado de abertura de tickets (#TK-XXXXX) assegura que nenhuma solicitação fique desassistida quando o autoatendimento não for suficiente.

Limites e Gerenciamento de Risco: É imperativo reconhecer as fronteiras operacionais do projeto. O TechAssist não possui privilégios de execução direta no Active Directory ou em firewalls corporativos: todas as ações são orientativas ou baseadas em portais seguros com dupla autenticação (MFA). Decisões de concessão de licenças financeiras ou privilégios de administrador de domínio exigem obrigatoriamente validação humana. Essa salvaguarda mitiga vetores de engenharia social e garante conformidade com as melhores práticas de governança de TI (ITIL v4).

Evolução Futura e Aprendizados: Como trabalhos futuros, planeja-se:
1. Integração via API REST com sistemas de ITSM corporativos reais (Jira Service Management ou GLPI) para persistência de chamados em banco de dados relacional;
2. Implementação de módulos fonéticos e correção ortográfica automática para elevar a robustez contra erros graves de digitação;
3. Implementação de arquitetura de RAG (Retrieval-Augmented Generation) delimitada sobre manuais técnicos internos em PDF para responder a diagnósticos de hardware mais complexos.


# 8. Referências Bibliográficas e Contribuições da Equipe


## 8.1 Referências Bibliográficas

1. JURAFSKY, Daniel; MARTIN, James H. Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition. 3. ed. Stanford University: Draft, 2024.
2. MANNING, Christopher D.; RAGHAVAN, Prabhakar; SCHÜTZE, Hinrich. Introduction to Information Retrieval. Cambridge University Press, 2008.
3. PEDREGOSA, Fabian et al. Scikit-learn: Machine Learning in Python. Journal of Machine Learning Research, v. 12, p. 2825-2830, 2011.
4. GRINBERG, Miguel. Flask Web Development: Developing Web Applications with Python. 2. ed. O'Reilly Media, 2018.
5. BRASIL. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD). Brasília, DF: Presidência da República, 2018.
6. AXELOS. ITIL Foundation: ITIL 4 Edition. Norwich: TSO (The Stationery Office), 2019.


## 8.2 Declaração de Autoria e Contribuições Individuais

Declaração de Autoria: Declaração de Autoria Própria e Integridade Acadêmica: Declara-se expressamente que todo o código-fonte, pipeline de pré-processamento textual, modelo de classificação de intenções supervisionado, base de conhecimento de autoatendimento, scripts de testes automatizados e redação deste relatório foram integralmente concebidos, implementados e validados pelos integrantes da equipe, em estrita conformidade aos Requisitos R1 a R7 da disciplina de Inteligência Artificial.
