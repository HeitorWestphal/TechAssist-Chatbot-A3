"""
Testes unitários para o servidor MCP do TechAssist AI (src/mcp_server.py).
Valida tools de classificação, recuperação de procedimentos, abertura e listagem de chamados.
"""

import json
import pytest
from src.mcp_server import handle_call_tool, TOOLS

def test_mcp_tools_list_schema():
    assert len(TOOLS) == 5
    tool_names = [t["name"] for t in TOOLS]
    assert "techassist_classify_intent" in tool_names
    assert "techassist_get_solution" in tool_names
    assert "techassist_create_ticket" in tool_names
    assert "techassist_list_tickets" in tool_names
    assert "techassist_explain_prediction" in tool_names

def test_mcp_classify_tool():
    res = handle_call_tool("techassist_classify_intent", {"query": "esqueci minha senha de rede"})
    assert "content" in res
    payload = json.loads(res["content"][0]["text"])
    assert payload["intencao"] == "redefinicao_senha"
    assert payload["confianca"] >= 0.38

def test_mcp_get_solution_tool():
    res = handle_call_tool("techassist_get_solution", {"intent": "problema_vpn_acesso"})
    assert "content" in res
    payload = json.loads(res["content"][0]["text"])
    assert "resposta" in payload
    assert "VPN" in payload["resposta"]

def test_mcp_create_and_list_ticket_tool():
    res_create = handle_call_tool("techassist_create_ticket", {
        "description": "Falha geral de rede na filial Sul",
        "requester": "Analista MCP",
        "department": "Operações",
        "priority": "CRITICA"
    })
    ticket = json.loads(res_create["content"][0]["text"])
    assert "protocolo" in ticket
    assert ticket["protocolo"].startswith("TK-")
    assert ticket["status"] == "ABERTO"

    res_list = handle_call_tool("techassist_list_tickets", {"priority": "CRITICA"})
    data = json.loads(res_list["content"][0]["text"])
    assert data["total"] >= 1
    assert any(t["protocolo"] == ticket["protocolo"] for t in data["tickets"])

def test_mcp_unknown_tool():
    res = handle_call_tool("ferramenta_inexistente", {})
    assert res.get("isError") is True
