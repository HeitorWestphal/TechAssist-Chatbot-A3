"""
Servidor Web Flask para a interface interativa do TechAssist (Requisito R1 e R7).
Fornece rotas de renderização de interface, endpoints de API JSON e telemetria analítica.
"""

import os
import json
from flask import Flask, render_template, request, jsonify, send_from_directory
from src.bot_engine import BotEngine

app = Flask(__name__, template_folder="templates", static_folder="static")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KB_PATH = os.path.join(BASE_DIR, "data", "knowledge_base.json")
DATASET_PATH = os.path.join(BASE_DIR, "data", "training_dataset.csv")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

engine = BotEngine(kb_path=KB_PATH, dataset_path=DATASET_PATH, threshold=0.38)

@app.route("/")
def index():
    """Renderiza a página principal com chat e telemetria analítica."""
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

@app.route("/api/explain", methods=["GET"])
def explain():
    """Endpoint de auditoria para a banca: inspeciona termos e pesos TF-IDF."""
    text = request.args.get("text", "")
    if not text:
        return jsonify({"error": "Parâmetro 'text' obrigatório."}), 400
    
    explanation = engine.classifier.explain(text)
    return jsonify(explanation)

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

if __name__ == "__main__":
    print("Iniciando TechAssist Web em http://localhost:5000 ...")
    app.run(host="0.0.0.0", port=5000, debug=True)
