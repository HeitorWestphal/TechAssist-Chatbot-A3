"""
Servidor Web Flask para a interface interativa do TechAssist (Requisito R1 e R7).
Fornece rotas de renderização de interface, endpoints de API RESTful,
execução de testes em tempo real, painel de tickets SQLite e telemetria analítica.
"""

import os
import csv
import json
import time
from flask import Flask, render_template, request, jsonify, send_from_directory, Response
from src.bot_engine import BotEngine
from src.database import list_tickets, get_ticket_by_protocol, update_ticket_status, create_ticket
from src.security_guardrails import security_guard
from src.statistical_validation import inject_typo_noise

app = Flask(__name__, template_folder="templates", static_folder="static")

# Métricas Prometheus em memória
METRICS = {
    "requests_total": 0,
    "predictions_total": {},
    "fallbacks_total": 0,
    "latencies": []
}

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
    """Processa a mensagem do usuário e retorna a resposta com distribuição de probabilidades e auditoria LGPD."""
    t_start = time.perf_counter()
    METRICS["requests_total"] += 1

    data = request.get_json() or {}
    message = data.get("message", "").strip()
    session_id = data.get("session_id", "web_default")
    apply_spellcheck = bool(data.get("apply_spellcheck", False))

    if not message:
        return jsonify({"error": "Mensagem vazia."}), 400

    # 1. Auditoria e Proteção de Segurança Corporativa / LGPD
    sanitized_text, sec_report = security_guard.inspect_and_sanitize(message)

    if not sec_report["is_safe"]:
        # Bloqueio preventivo contra SQLi ou Prompt Injection
        return jsonify({
            "response": f"⚠️ [ALERTA DE SEGURANÇA CORPORATIVA] A mensagem continha padrões proibidos ({', '.join(sec_report['violations'])}) e foi bloqueada pela camada de proteção do Helpdesk.",
            "intent": "seguranca_bloqueio",
            "confidence": 1.0,
            "is_fallback": True,
            "security_report": sec_report,
            "probabilities": {},
            "latency_ms": 0.1
        })

    # 2. Processamento da Mensagem Sanitizada
    result = engine.process_message(sanitized_text, session_id=session_id, apply_spellcheck=apply_spellcheck)
    result["security_report"] = sec_report
    if sec_report["pii_masked"]:
        result["mensagem_sanitizada_lgpd"] = sanitized_text

    # Métricas Prometheus
    pred_intent = result.get("intent", "desconhecido")
    METRICS["predictions_total"][pred_intent] = METRICS["predictions_total"].get(pred_intent, 0) + 1
    if result.get("is_fallback"):
        METRICS["fallbacks_total"] += 1
    
    elapsed = (time.perf_counter() - t_start) * 1000
    METRICS["latencies"].append(elapsed)
    if len(METRICS["latencies"]) > 500:
        METRICS["latencies"].pop(0)

    return jsonify(result)

@app.route("/api/adversarial-simulate", methods=["POST"])
def adversarial_simulate():
    """Simula injeção de ruído ortográfico adversarial e compara predição com e sem Levenshtein."""
    data = request.get_json() or {}
    text = data.get("text", "como faco para resetar minha senha de rede")
    noise_rate = float(data.get("noise_rate", 0.15))
    
    noisy_text = inject_typo_noise(text, noise_rate)
    
    pred_with = engine.classifier.predict(noisy_text, apply_spellcheck=True)
    pred_without = engine.classifier.predict(noisy_text, apply_spellcheck=False)
    
    return jsonify({
        "texto_original": text,
        "taxa_ruido": noise_rate,
        "texto_perturbado": noisy_text,
        "com_levenshtein": {
            "intencao": pred_with["intencao"],
            "confianca": round(pred_with["confianca"] * 100, 1),
            "is_fallback": pred_with["is_fallback"]
        },
        "sem_levenshtein": {
            "intencao": pred_without["intencao"],
            "confianca": round(pred_without["confianca"] * 100, 1),
            "is_fallback": pred_without["is_fallback"]
        }
    })

@app.route("/health", methods=["GET"])
def health():
    """Health check corporativo para monitoramento e orquestração Docker/Kubernetes."""
    return jsonify({
        "status": "healthy",
        "service": "techassist-ai",
        "version": "1.2.0",
        "classifier_loaded": engine.classifier.is_trained,
        "security_guardrails": "active"
    })

@app.route("/metrics", methods=["GET"])
def prometheus_metrics():
    """Endpoint oficial de métricas para ingestão no Prometheus / Grafana."""
    avg_latency = (sum(METRICS["latencies"]) / len(METRICS["latencies"])) if METRICS["latencies"] else 0.5
    sec_stats = security_guard.stats
    
    lines = [
        "# HELP techassist_requests_total Total de requisicoes recebidas pela API",
        "# TYPE techassist_requests_total counter",
        f"techassist_requests_total {METRICS['requests_total']}",
        "",
        "# HELP techassist_fallbacks_total Total de requisicoes que acionaram o Fallback seguro",
        "# TYPE techassist_fallbacks_total counter",
        f"techassist_fallbacks_total {METRICS['fallbacks_total']}",
        "",
        "# HELP techassist_latency_milliseconds Latencia media de inferencia em milissegundos",
        "# TYPE techassist_latency_milliseconds gauge",
        f"techassist_latency_milliseconds {avg_latency:.3f}",
        "",
        "# HELP techassist_pii_masked_total Total de dados pessoais LGPD mascarados",
        "# TYPE techassist_pii_masked_total counter",
        f"techassist_pii_masked_total {sec_stats['pii_masked_count']}",
        "",
        "# HELP techassist_sqli_blocked_total Total de tentativas de SQL Injection bloqueadas",
        "# TYPE techassist_sqli_blocked_total counter",
        f"techassist_sqli_blocked_total {sec_stats['sqli_blocked_count']}",
        "",
        "# HELP techassist_prompt_injection_blocked_total Total de tentativas de Jailbreak bloqueadas",
        "# TYPE techassist_prompt_injection_blocked_total counter",
        f"techassist_prompt_injection_blocked_total {sec_stats['prompt_injection_blocked_count']}",
        ""
    ]
    
    for intent, count in METRICS["predictions_total"].items():
        lines.append(f'techassist_intent_predictions_total{{intent="{intent}"}} {count}')
        
    return Response("\n".join(lines), mimetype="text/plain")

@app.route("/api/reset", methods=["POST"])
def reset():
    """Reinicia o estado da sessão conversacional."""
    data = request.get_json() or {}
    session_id = data.get("session_id", "web_default")
    engine.reset_session(session_id)
    return jsonify({"status": "reset_ok"})

@app.route("/api/history", methods=["GET"])
def history():
    """Retorna o histórico de mensagens registradas em uma sessão."""
    session_id = request.args.get("session_id", "web_default")
    session = engine.get_or_create_session(session_id)
    return jsonify({"session_id": session_id, "history": session.get("history", [])})

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

