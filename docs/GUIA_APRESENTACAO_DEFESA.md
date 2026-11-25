# Guia Completo da Apresentação e Defesa Oral da A3

> **Duração Total:** 8 minutos cronometrados  
> **Divisão Oficial:** 5 minutos de apresentação + demonstração ao vivo | 3 minutos de perguntas do professor  
> **Arquivo de Slides:** [`docs/APRESENTACAO_DEFESA_A3.pptx`](file:///Users/heitorwestphal/Downloads/A3Quarta/docs/APRESENTACAO_DEFESA_A3.pptx)  

---

## ⏱️ Roteiro Minuto a Minuto (5 Minutos de Apresentação)

## ⏱️ Roteiro Minuto a Minuto (6:30 de Apresentação + 1:30 de Perguntas)

### 00:00 – 01:45 | Introdução, Desafio de TI e Núcleo de IA/PLN (Slides 1 a 5)
* **Quem fala:** **Heitor Della Barba Westphal** (Líder / Engenharia de PLN)
* **O que dizer:**
  > "Boa noite, professor e colegas. Nosso projeto integrador A3 é o **TechAssist AI**, uma central corporativa inteligente de triagem e suporte técnico N1. Identificamos que entre 40% e 60% dos chamados de Helpdesk são solicitações repetitivas de N1 — como reset de senhas, falhas de VPN e lentidão de máquinas.
  > Para atender ao **Requisito Central R3**, concebemos uma arquitetura autoral híbrida (Opção C): normalização Unicode NFKD, remoção seletiva de stopwords, vetorização vetorial **TF-IDF n-grams (1, 2)**, classificação supervisionada via **Regressão Logística com Softmax** e **Similaridade por Cosseno**. Não recorremos a chamadas externas de LLMs: todo o cálculo vetorial é processado localmente em menos de 0.6 milissegundos com um limiar matemático de fallback calibrado em $\theta = 0.38$."

### 01:45 – 03:00 | Base de Conhecimento e Gestão de Sessão Multi-Turnos (Slides 3 e 4)
* **Quem fala:** **Ian Santiago Silveira** (Motor de Diálogo)
* **O que dizer:**
  > "O edital solicitava ao menos 3 categorias, mas estruturamos **8 intenções completas** na base semiestruturada JSON (`data/knowledge_base.json`), acompanhadas de um corpus supervisionado com mais de 100 sentenças balanceadas.
  > Implementei no `src/bot_engine.py` a orquestração conversacional com máquina de estados finitos. Quando o usuário necessita de atendimento humano especializado, o motor transiciona de estado, coleta os detalhes do incidente e formaliza o chamado técnico gerando um protocolo único (ex: `#TK-10842`), evitando alucinações e garantindo que o colaborador seja encaminhado diretamente à fila correta de N2."

### 03:00 – 04:15 | Persistência Relacional SQLite e Governança ITIL/LGPD (Slide 10 e 11)
* **Quem fala:** **Bruno Hudson Siebert Costa** (Engenharia de Dados & DevOps)
* **O que dizer:**
  > "Para atender aos padrões corporativos de governança **ITIL v4 e LGPD**, implementei a camada de persistência relacional em SQLite (`src/database.py` e `data/techassist.db`).
  > Todos os incidentes escalonados pelo chatbot são gravados atomicamente no banco com campos de auditoria: protocolo, solicitante, departamento, descrição, intenção inferida pela IA, score de confiança e status de atendimento — permitindo a transição do chamado de 'ABERTO' para 'EM_ATENDIMENTO' e 'RESOLVIDO' com data e hora de fechamento. Além disso, estruturei a esteira automatizada de CI/CD no GitHub Actions que valida o build e executa 100% dos testes a cada commit."

### 04:15 – 05:45 | Demonstração ao Vivo, Swagger UI e Live Test Runner (Slide 11 e 12)
* **Quem fala:** **João Víctor Muniz da Silva** (API REST & Interface Web)
* **O que dizer e mostrar na tela:**
  > "Desenvolvi a interface web moderna e a API RESTful corporativa em Flask (`src/app_web.py`).
  > 1. *(Demonstrar Chat e Telemetria):* No navegador em `http://localhost:5000`, envio a pergunta *'esqueci minha senha do computador'*. O bot responde imediatamente com o procedimento institucional e o painel lateral do **Chart.js** plota em tempo real a distribuição de probabilidades Softmax da IA e a latência de inferência (<1ms).
  > 2. *(Demonstrar Fallback Seguro):* Envio uma dúvida fora de escopo (*'qual a receita de bolo'*). O bot não alucina: ativa o fallback seguro com confiança < 0.38 e oferece suporte N2.
  > 3. *(Demonstrar Live Test Runner e Swagger):* Clico na aba *Live Test Runner* e executo os **25 testes formais do edital em tempo real na frente do professor**, exibindo acurácia de 72% (e 88% com corretor de Levenshtein ativado no Marco 5). Além disso, temos a documentação interativa em `/docs` compatível com a especificação OpenAPI 3.0."

### 05:45 – 06:30 | Conclusão, Resultados Científicos e Encerramento (Slide 13)
* **Quem fala:** **Toda a Equipe**
* **O que dizer:**
  > "Consolidamos nosso trabalho com 11 gráficos científicos de 300 DPI, relatório técnico formal com mais de 8 páginas e 30 testes unitários automatizados com 100% de aprovação no PyTest. Todos os requisitos (R1 a R7) foram integralmente superados. Estamos à disposição para as perguntas da banca!"

---

## 🎯 Como Responder às Perguntas da Banca (3 Minutos Finais)

### Pergunta 1: *"Onde está a Inteligência Artificial no código de vocês?"*
* **Resposta Ideal:**
  > "Está na classe `IntentClassifier`, localizada no arquivo `src/intent_classifier.py`. Lá nós instanciamos o `TfidfVectorizer` com n-grams de 1 e 2 palavras e treinamos o classificador supervisionado de `LogisticRegression` com balanceamento de pesos. Além disso, no método `predict()`, calculamos a similaridade de cossenos com a matriz de treinamento para compor a confiança híbrida e aplicar o limiar de fallback."

### Pergunta 2: *"O que acontece se eu digitar uma pergunta que o bot não conhece?" (Desafio Surpresa ao Vivo)*
* **Se o professor testar uma frase inédita (ex: 'meu mouse quebrou e parou de funcionar'):**
  * **Cenário A:** O bot classifica como abertura de chamado ou problema de máquina -> *"O modelo capturou a intenção com base nos vetores similares de problema técnico."*
  * **Cenário B:** O bot aciona fallback -> *"Professor, esse resultado comprova a eficácia do nosso Requisito R4: como a confiança ficou abaixo de 0.38, o bot não inventou respostas; ele acionou a abstenção segura e ofereceu abrir um chamado para o técnico N2."*

### Pergunta 3: *"Por que vocês não usaram apenas a API do ChatGPT / OpenAI?"*
* **Resposta Ideal:**
  > "Por três motivos fundamentais: primeiro, o Requisito R3 proíbe expressamente depender apenas de uma API pronta sem mecanismo próprio de IA; segundo, LLMs comerciais possuem custo recorrente e alta latência; terceiro, modelos generativos alucinam facilmente procedimentos técnicos, enquanto nosso classificador TF-IDF possui previsibilidade determinística e precisão de 100% no suporte."

### Pergunta 4: *"Qual foi a contribuição de cada um?"*
* **Heitor Westphal:** Arquitetura do pipeline de PLN, implementação do classificador TF-IDF e Regressão Logística, cálculo de similaridade e lógica de fallback.
* **Integrante 2:** Engenharia de requisitos de TI, curadoria da base de conhecimento JSON e dataset supervisionado com mais de 100 sentenças.
* **Integrante 3:** Criação da matriz de 25 testes (R5), script de avaliação automatizada (`evaluate.py`), cálculo da matriz de confusão e relatório estatístico.
* **Integrante 4:** Desenvolvimento da interface Web Flask responsiva, badges dinâmicos de IA e redação do relatório técnico formal.
