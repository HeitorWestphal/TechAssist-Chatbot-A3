---
name: techassist
description: Central corporativa inteligente de triagem N1 e suporte técnico de TI com mecanismo próprio de PLN (TF-IDF + Regressão Logística), gestão de chamados SQLite e conformidade ITIL.
---

# TechAssist AI — IT Helpdesk Tier-1 Skill

Esta skill habilita o agente a atuar como um analista autônomo de Helpdesk de Nível 1 (N1), solucionando dúvidas rotineiras de TI com latência sub-milissegundo (<0.6ms), sem alucinação (fallback calibrado em $\theta = 0.38$) e escalonando chamados N2 diretamente no banco relacional SQLite (`data/techassist.db`).

## Ferramentas Disponíveis (MCP Tools)

### 1. `techassist_classify_intent`
Recebe a mensagem de texto do usuário e retorna a intenção detectada, pontuação de confiança (0.0 a 1.0) e distribuição probabilística Softmax.
* **Argumentos:**
  * `query` (string, obrigatório): A pergunta ou relato do colaborador.
  * `apply_spellcheck` (bool, opcional): Habilita o corretor por distância de Levenshtein ($d \le 2$).

### 2. `techassist_get_solution`
Recupera o procedimento operacional homologado pela governança de TI para a intenção fornecida.
* **Argumentos:**
  * `intent` (string, obrigatório): Identificador canônico da intenção.

### 3. `techassist_create_ticket`
Registra e persiste atomicamente um chamado de suporte técnico N2 quando a dúvida excede o escopo de autoatendimento.
* **Argumentos:**
  * `description` (string, obrigatório): Descrição do problema relatado.
  * `requester` (string, opcional): Nome do colaborador.
  * `department` (string, opcional): Departamento.
  * `priority` (string, opcional: "BAIXA", "PADRAO", "ALTA", "CRITICA").

### 4. `techassist_list_tickets`
Lista os chamados técnicos persistidos permitindo filtragem por status (`ABERTO`, `EM_ATENDIMENTO`, `RESOLVIDO`) ou prioridade.

### 5. `techassist_explain_prediction`
Inspeciona os n-gramas extraídos no vocabulário vetorial e seus pesos TF-IDF (Explainable AI - XAI).

## Exemplo de Uso no Agente

```python
# 1. Classificar o chamado
result = call_tool("techassist_classify_intent", {"query": "esqueci minha senha do windows"})

# 2. Se a confiança for aceita, obter o procedimento
if not result["is_fallback"]:
    solution = call_tool("techassist_get_solution", {"intent": result["intencao"]})
else:
    # 3. Caso contrário, criar ticket N2
    ticket = call_tool("techassist_create_ticket", {
        "description": "Usuário necessita de suporte presencial",
        "priority": "ALTA"
    })
```
