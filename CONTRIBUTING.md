# Guia de Contribuição e Engenharia Colaborativa — TechAssist AI

Este documento estabelece as diretrizes de desenvolvimento, governança de código, divisão formal de responsabilidades e fluxo de trabalho com Git, Branches e Pull Requests para a equipe do **TechAssist AI**.

---

## 👥 1. Integrantes da Equipe

| Nome Completo | RA | Papel no Projeto | GitHub |
| :--- | :---: | :--- | :--- |
| **Heitor Della Barba Westphal** | 1072410915 | Líder de Equipe / Engenharia de PLN e Arquitetura de IA | [@HeitorWestphal](https://github.com/HeitorWestphal) |
| **Bruno Hudson Siebert Costa** | 1072419878 | Engenharia de Dados, Persistência Relacional SQLite e DevOps | [@BHSC1](https://github.com/BHSC1) |
| **Ian Santiago Silveira** | 1072410937 | Motor de Diálogo Conversacional e Gestão de Sessões Multi-Turnos | [@SantiagoIanS](https://github.com/SantiagoIanS) |
| **João Víctor Muniz da Silva** | 1072413992 | API RESTful Corporativa, Swagger UI e Validação Experimental | [@Muniz2504](https://github.com/Muniz2504) |

> **Nota de Integridade:** Todos os integrantes são programadores e desenvolvem ativamente funcionalidades de código-fonte (`src/`) e testes automatizados (`tests/`).

---

## 📋 2. Divisão de Funcionalidades, Módulos e Testes Unitários

Cada integrante é o responsável técnico principal por uma frente do sistema, desenvolvendo o código e os respectivos testes automatizados:

| Integrante | Funcionalidade / Escopo | Código-Fonte Implementado | Testes Automatizados (PyTest) | Branch Dedicada |
| :--- | :--- | :--- | :--- | :--- |
| **Heitor Westphal** | **Arquitetura de IA e PLN:** Vetorizador TF-IDF n-grams (1,2), Regressão Logística, Cosseno, Calibração de Fallback ($\theta = 0.38$), Corretor de Levenshtein, Projeção PCA e Benchmark comparativo de 4 modelos. | `src/intent_classifier.py`<br>`src/nlp_preprocessor.py`<br>`src/benchmark.py`<br>`src/generate_advanced_charts.py` | `tests/test_nlp_preprocessor.py`<br>`tests/test_intent_classifier.py` | `main` |
| **Bruno Hudson Siebert Costa** | **Persistência Relacional e Governança ITIL/LGPD:** Estruturação do banco SQLite, tabela de tickets de suporte N2, CRUD de incidentes, transição de status (ABERTO $\rightarrow$ EM_ATENDIMENTO $\rightarrow$ RESOLVIDO) e auditoria. | `src/database.py`<br>`data/techassist.db` | `tests/test_database.py` | `feat/database-sqlite-itil` |
| **Ian Santiago Silveira** | **Motor de Diálogo e Gestão de Sessão Multi-Turnos:** Máquina de estados finitos conversacional, orquestração de fluxo, fluxo guiado para abertura de chamado N2 (`#TK-XXXXX`), curadoria da base de 8 intenções e regras de fallback seguro. | `src/bot_engine.py`<br>`data/knowledge_base.json`<br>`data/training_dataset.csv` | `tests/test_bot_engine.py` | `feat/dialogue-engine-multiturn` |
| **João Víctor Muniz da Silva** | **API RESTful Corporativa, Swagger UI e Live Test Runner:** Endpoints JSON (`/api/chat`, `/api/explain`, `/api/tickets`), especificação formal OpenAPI 3.0, interface Swagger UI (`/docs`), runner dos 25 testes em tempo real e front-end com Chart.js. | `src/app_web.py`<br>`docs/openapi.yaml`<br>`src/templates/index.html`<br>`src/evaluate.py` | `tests/test_api_endpoints.py` | `feat/api-rest-swagger-runner` |

---

## 🔄 3. Fluxo de Trabalho com Branches e Pull Requests (GitHub Flow)

Para garantir rastreabilidade perante os professores e demonstrar o trabalho colaborativo real da equipe:

### Passo 1: Aceitar o convite de Colaborador
O líder Heitor Westphal convidou todos os integrantes como colaboradores no repositório GitHub. Aceite o convite no seu e-mail ou diretamente na notificação do GitHub.

### Passo 2: Clonar o Repositório e Atualizar a `main`
```bash
git clone https://github.com/HeitorWestphal/TechAssist-Chatbot-A3.git
cd TechAssist-Chatbot-A3
git checkout main
git pull origin main
```

### Passo 3: Acessar a sua Branch de Trabalho
As branches já foram criadas no repositório remoto. Para trabalhar na sua frente:

* **Bruno Hudson:**
  ```bash
  git checkout feat/database-sqlite-itil
  git pull origin feat/database-sqlite-itil
  ```
* **Ian Santiago:**
  ```bash
  git checkout feat/dialogue-engine-multiturn
  git pull origin feat/dialogue-engine-multiturn
  ```
* **João Víctor Muniz:**
  ```bash
  git checkout feat/api-rest-swagger-runner
  git pull origin feat/api-rest-swagger-runner
  ```

### Passo 4: Executar os Testes Unitários Localmente
Antes de fazer qualquer commit, valide que 100% dos testes da sua frente e do sistema continuam passando:
```bash
PYTHONPATH=. pytest -v --cov=src tests/
```

### Passo 5: Fazer Commits com a Própria Conta do GitHub
Utilize a convenção [Conventional Commits](https://www.conventionalcommits.org/pt-br/):
```bash
git add .
git commit -m "feat(database): adiciona auditoria de datas para fechamento de chamados N2"
```

### Passo 6: Enviar para o GitHub e Abrir o Pull Request
```bash
git push origin <sua-branch>
```
1. Acesse o repositório no GitHub: `https://github.com/HeitorWestphal/TechAssist-Chatbot-A3`.
2. Clique no botão verde **"Compare & pull request"**.
3. Preencha o template do PR descrevendo o que foi implementado e os testes executados.
4. O pipeline do **GitHub Actions (CI)** rodará automaticamente todos os testes para aprovação do merge na `main`.

---

## 🏷️ 4. Padrão de Mensagens de Commit

| Tipo | Finalidade | Exemplo de Commit |
| :---: | :--- | :--- |
| `feat` | Nova funcionalidade de código | `feat(dialogue): adiciona maquina de estados para abertura de chamados N2` |
| `test` | Adição ou aprimoramento de testes | `test(database): adiciona teste unitario para integridade de protocolo unico` |
| `fix` | Correção de defeito | `fix(nlp): ajusta tolerancia do corretor de Levenshtein para termos curtos` |
| `docs` | Alteração em documentação ou OpenAPI | `docs(swagger): detalha esquemas de entrada e saida da rota /api/tickets` |
| `ci` | Ajustes no pipeline do GitHub Actions | `ci: adiciona matrix de testes no Python 3.11` |
