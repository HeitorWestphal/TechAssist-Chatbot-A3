"""
Servidor Web Flask para a interface interativa do TechAssist (Requisito R1 e R7).
Fornece rotas de renderização de interface e endpoints de API JSON.
"""

import os
from flask import Flask, render_template, request, jsonify
from src.bot_engine import BotEngine

app = Flask(__name__, template_folder="templates", static_folder="static")

# Inicializa o motor conversacional com IA
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KB_PATH = os.path.join(BASE_DIR, "data", "knowledge_base.json")
DATASET_PATH = os.path.join(BASE_DIR, "data", "training_dataset.csv")

engine = BotEngine(kb_path=KB_PATH, dataset_path=DATASET_PATH, threshold=0.38)

@app.route("/")
def index():
    """Renderiza a página principal do chat."""
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    """Processa a mensagem do usuário e retorna a resposta com metadados de IA."""
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    session_id = data.get("session_id", "web_default")

    if not message:
        return jsonify({"error": "Mensagem vazia."}), 400

    result = engine.process_message(message, session_id=session_id)
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
    """Endpoint de auditoria para a defesa: inspeciona pesos TF-IDF de um texto."""
    text = request.args.get("text", "")
    if not text:
        return jsonify({"error": "Parâmetro 'text' obrigatório."}), 400
    
    explanation = engine.classifier.explain(text)
    return jsonify(explanation)

if __name__ == "__main__":
    print("Iniciando TechAssist Web em http://localhost:5000 ...")
    app.run(host="0.0.0.0", port=5000, debug=True)
