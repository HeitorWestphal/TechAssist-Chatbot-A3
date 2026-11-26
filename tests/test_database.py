"""Testes unitários para a camada de persistência relacional SQLite (src/database.py).
Valida criação de tickets, consulta por protocolo, listagem por status e atualização.
"""

import pytest
import sqlite3
from src import database

import uuid

def test_database_initialization():
    database.init_db()
    with database.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tickets'")
        assert cursor.fetchone() is not None

def test_create_and_get_ticket():
    proto = f"TK-TEST-{uuid.uuid4().hex[:6]}"
    created = database.create_ticket(
        protocolo=proto,
        descricao="Teste automatizado de integridade SQLite",
        intencao="redefinicao_senha",
        confianca=0.95,
        solicitante="Robo de Testes PyTest",
        departamento="Engenharia de Qualidade",
        prioridade="ALTA"
    )
    assert created is not None
    assert created["protocolo"] == proto
    assert created["status"] == "ABERTO"
    assert created["prioridade"] == "ALTA"

    fetched = database.get_ticket_by_protocol(proto)
    assert fetched is not None
    assert fetched["descricao"] == "Teste automatizado de integridade SQLite"
    assert fetched["confianca_ia"] == pytest.approx(0.95)

def test_update_ticket_status():
    proto = f"TK-TEST-{uuid.uuid4().hex[:6]}"
    database.create_ticket(
        protocolo=proto,
        descricao="Ticket para teste de transicao de status",
        intencao="problema_vpn_acesso",
        confianca=0.88
    )

    # Atualiza para RESOLVIDO
    updated = database.update_ticket_status(proto, "RESOLVIDO")
    assert updated is True

    row = database.get_ticket_by_protocol(proto)
    assert row["status"] == "RESOLVIDO"
    assert row["data_resolucao"] is not None

def test_list_tickets():
    tickets = database.list_tickets()
    assert isinstance(tickets, list)
    assert len(tickets) >= 1

    # Filtra por status
    resolved = database.list_tickets(status="RESOLVIDO")
    for t in resolved:
        assert t["status"] == "RESOLVIDO"

def test_list_tickets_filter_priority():
    proto = f"TK-CRITICO-{uuid.uuid4().hex[:6]}"
    database.create_ticket(
        protocolo=proto,
        descricao="Servidor principal inoperante",
        intencao="lentidao_sistema",
        confianca=0.99,
        prioridade="CRITICA"
    )
    criticos = database.list_tickets(prioridade="CRITICA")
    assert any(t["protocolo"] == proto for t in criticos)
