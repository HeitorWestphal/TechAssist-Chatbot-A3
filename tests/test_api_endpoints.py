"""Testes de integração para a API HTTP REST do TechAssist AI (src/app_web.py).
Valida rotas /api/chat, /api/reset, /api/explain, /api/tickets e /api/run-tests-live.
"""

import json
import pytest
from src.app_web import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"TechAssist" in response.data

def test_api_chat_success(client):
    payload = {
        "message": "Esqueci minha senha de rede, como faco?",
        "session_id": "pytest_session",
        "apply_spellcheck": False
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "resposta" in data
    assert data["intencao"] == "redefinicao_senha"
    assert "confianca" in data
    assert data["confianca"] >= 0.38
    assert "todas_probabilidades" in data

def test_api_chat_empty_message(client):
    response = client.post("/api/chat", json={"message": "   "})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_api_reset(client):
    response = client.post("/api/reset", json={"session_id": "pytest_session"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "reset_ok"

def test_api_history(client):
    client.post("/api/chat", json={"message": "Ola bom dia", "session_id": "test_history_sess"})
    res = client.get("/api/history?session_id=test_history_sess")
    assert res.status_code == 200
    data = res.get_json()
    assert "history" in data
    assert len(data["history"]) >= 1

def test_api_explain(client):
    response = client.get("/api/explain?text=vpn+caiu+e+nao+conecta")
    assert response.status_code == 200
    data = response.get_json()
    assert "termos_tfidf_encontrados" in data
    assert "diagnostico_predicao" in data
    assert data["diagnostico_predicao"]["intencao"] == "problema_vpn_acesso"

def test_api_tickets_get_and_status_update(client):
    # 1. Lista tickets
    response = client.get("/api/tickets")
    assert response.status_code == 200
    data = response.get_json()
    assert "tickets" in data
    assert "total" in data
    assert data["total"] >= 1

    primeiro_ticket = data["tickets"][0]["protocolo"]

    # 2. Atualiza status
    resp_update = client.post(f"/api/tickets/{primeiro_ticket}/status", json={"status": "EM_ATENDIMENTO"})
    assert resp_update.status_code == 200
    update_data = resp_update.get_json()
    assert update_data["new_status"] == "EM_ATENDIMENTO"

def test_api_run_tests_live(client):
    response = client.post("/api/run-tests-live", json={"apply_spellcheck": True})
    assert response.status_code == 200
    data = response.get_json()
    assert "total_testes" in data
    assert data["total_testes"] == 25
    assert "acuracia_global" in data
    assert data["acuracia_global"] >= 70.0
    assert "testes" in data
    assert len(data["testes"]) == 25

def test_swagger_and_openapi_endpoints(client):
    res_yaml = client.get("/openapi.yaml")
    assert res_yaml.status_code == 200
    assert b"openapi: 3.0.3" in res_yaml.data

    res_docs = client.get("/docs")
    assert res_docs.status_code == 200
    assert b"SwaggerUIBundle" in res_docs.data
