"""Testes unitários e de integração para o motor de diálogo BotEngine.
Verifica sessões, contexto multi-turnos, geração e persistência de chamados e fallback.
"""

import os
import pytest
from src.bot_engine import BotEngine

KB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge_base.json")
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "training_dataset.csv")

@pytest.fixture(scope="module")
def bot():
    return BotEngine(kb_path=KB_PATH, dataset_path=DATA_PATH, threshold=0.38)

def test_bot_session_lifecycle(bot):
    session_id = "test-session-123"
    sess = bot.get_or_create_session(session_id)
    assert sess["state"] == "IDLE"
    assert len(sess["history"]) == 0

    bot.process_message("Olá", session_id=session_id)
    assert len(bot.sessions[session_id]["history"]) == 1
    assert len(bot.get_session_history(session_id)) == 1

    bot.reset_session(session_id)
    assert len(bot.sessions[session_id]["history"]) == 0
    assert len(bot.get_session_history(session_id)) == 0
    assert bot.sessions[session_id]["state"] == "IDLE"

def test_bot_saudacao(bot):
    res = bot.process_message("Ola, bom dia!", session_id="test-saudacao")
    assert res["intencao"] == "saudacao"
    assert "TechAssist" in res["resposta"]
    assert res["is_fallback"] is False

def test_bot_multi_turn_ticket_creation(bot):
    sess_id = "test-multi-turn-ticket"
    bot.reset_session(sess_id)

    # 1. Usuário expressa intenção de abrir chamado
    res1 = bot.process_message("Preciso falar com um atendente humano e abrir chamado", session_id=sess_id)
    assert bot.sessions[sess_id]["state"] == "AWAITING_TICKET_DETAILS"
    assert "descreva" in res1["resposta"].lower() or "detalhes" in res1["resposta"].lower()

    # 2. Usuário fornece os detalhes do incidente
    res2 = bot.process_message("Meu monitor Dell 4K nao liga mesmo conectado na tomada", session_id=sess_id)
    assert res2["intencao"] == "abertura_chamado_confirmada"
    assert "protocolo" in res2
    assert res2["protocolo"].startswith("TK-")
    assert bot.sessions[sess_id]["state"] == "IDLE"

def test_bot_fallback_behavior(bot):
    res = bot.process_message("Quanto custa um quilo de acucar no mercado?", session_id="test-fallback")
    assert res["is_fallback"] is True
    assert res["intencao"] == "fora_escopo"
    assert "não compreendi" in res["resposta"].lower() or "desculpe" in res["resposta"].lower() or "humano" in res["resposta"].lower()
