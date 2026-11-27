"""Testes unitários para Aprendizado Ativo (RLHF), BM25, Data Augmentation e Exportação CSV."""
import pytest
from src.database import add_feedback, list_feedback, approve_feedback_for_training, get_feedback_stats
from src.bm25_retriever import OkapiBM25
from src.data_augmenter import augment_sentence
from src.app_web import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_database_feedback_lifecycle():
    fb_id = add_feedback(
        session_id="test_session_123",
        pergunta="meu teclado nao funciona",
        intencao_predita="lentidao_sistema",
        confianca_ia=0.42,
        avaliacao=-1,
        comentario="Era problema de hardware/driver",
        intencao_corrigida="abertura_chamado"
    )
    assert fb_id > 0

    pending = list_feedback(status="PENDENTE_REVISAO")
    assert any(f["id"] == fb_id for f in pending)

    # Aprovar para retreinamento
    success = approve_feedback_for_training(fb_id, "abertura_chamado")
    assert success is True

    stats = get_feedback_stats()
    assert stats["total_feedbacks"] > 0
    assert stats["aprovados_treino"] > 0

def test_api_feedback_and_retrain_endpoints(client):
    # Enviar feedback
    res = client.post("/api/feedback", json={
        "session_id": "web_test",
        "pergunta": "esqueci minha credencial corporativa",
        "intencao_predita": "redefinicao_senha",
        "confianca": 0.85,
        "avaliacao": 1
    })
    assert res.status_code == 200
    fb_id = res.get_json()["id"]

    # Fila de curadoria
    res_queue = client.get("/api/active-learning/queue")
    assert res_queue.status_code == 200
    assert "queue" in res_queue.get_json()

    # Aprovação
    res_appr = client.post("/api/active-learning/approve", json={
        "id": fb_id,
        "intencao_corrigida": "redefinicao_senha"
    })
    assert res_appr.status_code == 200

    # Retreinamento ativo com 1 clique
    res_retrain = client.post("/api/active-learning/retrain")
    assert res_retrain.status_code == 200
    data = res_retrain.get_json()
    assert data["status"] == "retrained_successfully"
    assert data["total_amostras_treinadas"] > 100

def test_export_tickets_csv(client):
    res = client.get("/api/tickets/export/csv")
    assert res.status_code == 200
    assert res.content_type == "text/csv; charset=utf-8"
    assert "protocolo" in res.get_data(as_text=True)

def test_okapi_bm25_retriever():
    corpus = [
        ["como", "resetar", "minha", "senha"],
        ["minha", "vpn", "nao", "conecta"],
        ["computador", "esta", "muito", "lento"]
    ]
    bm25 = OkapiBM25(corpus)
    scores = bm25.score(["resetar", "senha"])
    assert len(scores) == 3
    # O primeiro documento deve ter a maior pontuação
    assert scores[0] > scores[1]
    assert scores[0] > scores[2]

def test_data_augmentation_eda():
    orig = "como faco para resetar minha senha bloqueada"
    aug = augment_sentence(orig)
    assert isinstance(aug, str)
    assert len(aug.split()) > 0
