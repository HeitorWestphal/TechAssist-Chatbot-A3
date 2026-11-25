"""
Servidor Web Flask para a interface interativa do TechAssist (Requisito R1 e R7).
Fornece rotas de renderização de interface, endpoints de API RESTful,
execução de testes em tempo real, painel de tickets SQLite e telemetria analítica.
"""

import os
import csv
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
from src.bot_engine import BotEngine
from src.database import list_tickets, get_ticket_by_protocol, update_ticket_status, create_ticket

app = Flask(__name__, template_folder="templates", static_folder="static")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KB_PATH = os.path.join(BASE_DIR, "data", "knowledge_base.json")
DATASET_PATH = os.path.join(BASE_DIR, "data", "training_dataset.csv")
TEST_DATASET_PATH = os.path.join(BASE_DIR, "data", "test_dataset.csv")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

engine = BotEngine(kb_path=KB_PATH, dataset_path=DATASET_PATH, threshold=0.38)

@app.route("/")
def index():
    """Renderiza a página principal com chat, telemetria analítica e painel N2."""
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    """Processa a mensagem do usuário e retorna a resposta com distribuição de probabilidades."""
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    session_id = data.get("session_id", "web_default")
    apply_spellcheck = bool(data.get("apply_spellcheck", False))

    if not message:
        return jsonify({"error": "Mensagem vazia."}), 400

    result = engine.process_message(message, session_id=session_id, apply_spellcheck=apply_spellcheck)
    return jsonify(result)

@app.route("/api/reset", methods=["POST"])
def reset():
    """Reinicia o estado da sessão conversacional."""
    data = request.get_json() or {}
    session_id = data.get("session_id", "web_default")
    engine.reset_session(session_id)
    return jsonify({"status": "reset_ok"})

@app.route("/api/explain", methods=["GET", "POST"])
def explain():
    """Endpoint de explicabilidade e atribuição de tokens TF-IDF (XAI)."""
    if request.method == "POST":
        data = request.get_json() or {}
        text = data.get("text", "")
    else:
        text = request.args.get("text", "")

    if not text:
        return jsonify({"error": "Texto obrigatório."}), 400
    
    explanation = engine.classifier.explain(text)
    return jsonify(explanation)

@app.route("/api/tickets", methods=["GET"])
def get_tickets():
    """Retorna os tickets persistidos no banco de dados SQLite."""
    status_filter = request.args.get("status")
    tickets = list_tickets(status_filter)
    return jsonify({"total": len(tickets), "tickets": tickets})

@app.route("/api/tickets/<protocolo>/status", methods=["POST"])
def change_ticket_status(protocolo):
    """Atualiza o status de um chamado (ABERTO, EM_ATENDIMENTO, RESOLVIDO)."""
    data = request.get_json() or {}
    new_status = data.get("status", "EM_ATENDIMENTO")
    success = update_ticket_status(protocolo, new_status)
    if success:
        return jsonify({"status": "updated", "protocolo": protocolo, "new_status": new_status})
    return jsonify({"error": "Ticket não encontrado."}), 404

@app.route("/api/run-tests-live", methods=["POST"])
def run_tests_live():
    """
    Executa a suite dos 25 testes do edital em tempo real e retorna
    o diagnóstico caso a caso para exibição visual no front-end.
    """
    data = request.get_json() or {}
    use_spellcheck = bool(data.get("apply_spellcheck", False))

    test_cases = []
    with open(TEST_DATASET_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_cases.append(row)

    results = []
    correct_count = 0
    fallback_count = 0

    for case in test_cases:
        q = case["pergunta"]
        expected = case["intencao_esperada"]
        pred = engine.classifier.predict(q, apply_spellcheck=use_spellcheck)

        obtained = pred["intencao"]
        conf = pred["confianca"]
        is_fallback = pred["is_fallback"]
        is_correct = (obtained == expected)

        if is_correct:
            correct_count += 1
        if is_fallback:
            fallback_count += 1

        results.append({
            "id": case["id"],
            "categoria": case["categoria_teste"],
            "pergunta": q,
            "esperado": expected,
            "obtido": obtained,
            "confianca": round(conf * 100, 1),
            "acertou": is_correct,
            "is_fallback": is_fallback,
            "latencia_ms": pred.get("latencia_ms", 0.5)
        })

    accuracy = round((correct_count / len(test_cases)) * 100, 2)
    return jsonify({
        "total_testes": len(test_cases),
        "acertos": correct_count,
        "acuracia_global": accuracy,
        "taxa_fallback": round((fallback_count / len(test_cases)) * 100, 2),
        "spellcheck_aplicado": use_spellcheck,
        "testes": results
    })

@app.route("/api/benchmark-data", methods=["GET"])
def benchmark_data():
    """Retorna os dados numéricos do benchmark de modelos."""
    bench_file = os.path.join(RESULTS_DIR, "benchmark_comparison.json")
    if os.path.exists(bench_file):
        with open(bench_file, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify({"error": "Benchmark não encontrado."}), 404

@app.route("/results/<path:filename>")
def serve_results(filename):
    """Serve imagens de gráficos e relatórios da pasta results."""
    return send_from_directory(RESULTS_DIR, filename)

DOCS_DIR = os.path.join(BASE_DIR, "docs")

@app.route("/openapi.yaml")
def openapi_spec():
    """Serve a especificação formal OpenAPI 3.0."""
    return send_from_directory(DOCS_DIR, "openapi.yaml", mimetype="text/yaml")

@app.route("/docs")
def swagger_ui():
    """Interface interativa Swagger UI para testes da API RESTful."""
    return """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>TechAssist AI — Documentação Swagger API</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
        <style>body { margin: 0; background: #0f172a; } .swagger-ui { background: #ffffff; padding: 20px; border-radius: 8px; max-width: 1200px; margin: 20px auto; }</style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
        <script>
            window.onload = () => {
                SwaggerUIBundle({
                    url: '/openapi.yaml',
                    dom_id: '#swagger-ui',
                    presets: [SwaggerUIBundle.presets.apis],
                    layout: "BaseLayout"
                });
            };
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    print("Iniciando TechAssist Web em http://localhost:5000 ...")
    app.run(host="0.0.0.0", port=5000, debug=True)

