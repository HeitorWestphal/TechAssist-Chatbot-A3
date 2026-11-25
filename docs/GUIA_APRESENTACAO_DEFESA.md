# Guia Completo da Apresentação e Defesa Oral da A3

> **Duração Total:** 8 minutos cronometrados  
> **Divisão Oficial:** 5 minutos de apresentação + demonstração ao vivo | 3 minutos de perguntas do professor  
> **Arquivo de Slides:** [`docs/APRESENTACAO_DEFESA_A3.pptx`](file:///Users/heitorwestphal/Downloads/A3Quarta/docs/APRESENTACAO_DEFESA_A3.pptx)  

---

## ⏱️ Roteiro Minuto a Minuto (5 Minutos de Apresentação)

### 00:00 – 00:45 | Introdução e Capa (Slide 1 e 2)
* **Quem fala:** Integrante 1 (ou Heitor)
* **O que dizer:**
  > "Boa noite, professor e colegas. Nosso projeto integrador A3 é o **TechAssist AI**, um chatbot inteligente de triagem e atendimento Nível 1 para Helpdesk corporativo de TI. Identificamos que mais de 50% dos chamados abertos em empresas são demandas repetitivas — como redefinição de senhas, lentidão e VPN. O TechAssist automatiza essas soluções e formaliza tickets N2 com protocolo, tudo através de um mecanismo autoral de IA e PLN, sem recorrer a APIs pagas."

### 00:45 – 01:30 | Domínio e Base de Conhecimento (Slide 3)
* **Quem fala:** Integrante 2 (Dados e Curadoria)
* **O que dizer:**
  > "O enunciado exigia ao menos 3 categorias, mas modelamos **8 intenções completas**: reset de senha, falhas na VPN, lentidão da máquina, catálogo de softwares, abertura de chamados, canais de atendimento, saudação e perguntas fora de escopo. Todos os dados foram estruturados em JSON e o corpus de treinamento foi construído com mais de 100 sentenças balanceadas, respeitando a privacidade e a LGPD com dados fictícios."

### 01:30 – 02:30 | O Mecanismo Próprio de IA e PLN (Slides 4 e 5) — *Ponto Crítico (R3)*
* **Quem fala:** Heitor Westphal (Desenvolvimento de IA)
* **O que dizer:**
  > "Para atender ao Requisito Central R3, implementamos um pipeline de IA próprio nos arquivos `src/nlp_preprocessor.py` e `src/intent_classifier.py`. Primeiro, a entrada passa por normalização Unicode NFKD, remoção de acentos e stopwords seletivas que preservam negações. Em seguida, vetorizamos o texto via **TF-IDF com unigramas e bigramas**. A predição utiliza **Regressão Logística Multinomial** combinada com **Similaridade de Cosseno**. Calculamos um score híbrido de confiança e, caso o valor seja menor que o limiar de **0.38**, o sistema não chuta: ele aciona abstenção segura (fallback)."

### 02:30 – 03:30 | Demonstração ao Vivo na Tela (Slide 8)
* **Quem fala:** Integrante 4 (ou responsável pela demonstração)
* **Passo a passo prático na tela:**
  1. Abrir o navegador em `http://localhost:5000` (ou rodar `./iniciar_web.sh`).
  2. Digitar uma pergunta típica: `"esqueci minha senha do computador"`.
     * *Mostrar:* O bot responde imediatamente com o passo a passo seguro do portal e o badge verde indica **Intenção: redefinicao_senha** e **Confiança de ~75%**.
  3. Digitar uma pergunta fora de escopo: `"qual o cardápio do almoço de hoje"`.
     * *Mostrar:* O bot aciona fallback seguro com badge âmbar, informa que não é do escopo de TI e sugere os tópicos homologados.
  4. Digitar `"quero abrir um chamado"`.
     * *Mostrar:* O bot solicita o relato do problema. Ao enviar `"tela azul após atualizar o windows"`, o bot gera o ticket estruturado com protocolo exclusivo (ex: `Ticket #TK-84920`).

### 03:30 – 04:30 | Resultados, Métricas e Análise de Falhas (Slides 6 e 7)
* **Quem fala:** Integrante 3 (Testes e Métricas)
* **O que dizer:**
  > "Executamos uma bateria formal com 25 casos de teste divididos nas 5 categorias do Requisito R5. Atingimos **72% de acurácia global**, com **100% de precisão técnica nas intenções de TI** — ou seja, o bot nunca confunde senha com VPN. Nas análises de falha exigidas no Marco 5, identificamos que os erros ocorreram em gírias severas ('carroça') e erros de digitação ('esquessi a ssnha'), onde o bot preferiu o fallback seguro. Como melhoria futura, propusemos um corretor por Distância de Levenshtein e embeddings morfológicos."

### 04:30 – 05:00 | Conclusão e Encerramento (Slide 10)
* **Quem fala:** Toda a equipe
* **O que dizer:**
  > "Todos os requisitos (R1 a R7), relatórios e artefatos foram entregues e testados. Estamos prontos para as perguntas do professor."

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
