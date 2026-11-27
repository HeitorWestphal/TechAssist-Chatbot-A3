"""
Servidor MCP (Model Context Protocol) para o TechAssist AI.
Permite que agentes autônomos (Claude Code, Cursor, Codex, Antigravity e Agensi.io)
invoquem diretamente as ferramentas de classificação, base de conhecimento e gestão de tickets N2.
"""

import sys
import json
import os
from typing import Dict, Any, List

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from src.bot_engine import BotEngine
from src.database import create_ticket, list_tickets, update_ticket_status, get_ticket_by_protocol

KB_PATH = os.path.join(BASE_DIR, "data", "knowledge_base.json")
DATASET_PATH = os.path.join(BASE_DIR, "data", "training_dataset.csv")

engine = BotEngine(kb_path=KB_PATH, dataset_path=DATASET_PATH, threshold=0.38)

TOOLS = [
    {
        "name": "techassist_classify_intent",
        "description": "Classifica a mensagem de suporte técnico usando TF-IDF calibrado e Regressão Logística (<1ms de latência), retornando confiança e probabilidades.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Mensagem ou dúvida do colaborador de TI."},
                "apply_spellcheck": {"type": "boolean", "default": False, "description": "Ativa o corretor dinâmico de Levenshtein (d <= 2)."}
            },
            "required": ["query"]
        }
    },
    {
        "name": "techassist_get_solution",
        "description": "Recupera o procedimento operacional homologado passo a passo para uma intenção identificada na base de conhecimento.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "intent": {"type": "string", "description": "Identificador da intenção (ex: redefinicao_senha, problema_vpn_acesso)."}
            },
            "required": ["intent"]
        }
    },
    {
        "name": "techassist_create_ticket",
        "description": "Registra e persiste formalmente um novo chamado técnico de N2 (#TK-XXXXX) no banco SQLite local com governança ITIL.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "description": {"type": "string", "description": "Descrição detalhada do incidente de TI."},
                "requester": {"type": "string", "default": "Colaborador Corporativo", "description": "Nome do colaborador solicitante."},
                "department": {"type": "string", "default": "Geral", "description": "Departamento do solicitante."},
                "priority": {"type": "string", "enum": ["BAIXA", "PADRAO", "ALTA", "CRITICA"], "default": "PADRAO"}
            },
            "required": ["description"]
        }
    },
    {
        "name": "techassist_list_tickets",
        "description": "Lista chamados técnicos persistidos no banco de dados SQLite, permitindo filtrar por status ou prioridade.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "status": {"type": "string", "enum": ["ABERTO", "EM_ATENDIMENTO", "RESOLVIDO"], "description": "Filtrar por status."},
                "priority": {"type": "string", "enum": ["BAIXA", "PADRAO", "ALTA", "CRITICA"], "description": "Filtrar por prioridade."}
            }
        }
    },
    {
        "name": "techassist_explain_prediction",
        "description": "Explicabilidade de IA (XAI): extrai os termos n-grams ativados no vocabulário vetorial e seus pesos TF-IDF.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Sentença para inspeção de features."}
            },
            "required": ["query"]
        }
    }
]

def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    if name == "techassist_classify_intent":
        q = arguments.get("query", "")
        spell = bool(arguments.get("apply_spellcheck", False))
        pred = engine.classifier.predict(q, apply_spellcheck=spell)
        return {"content": [{"type": "text", "text": json.dumps(pred, ensure_ascii=False, indent=2)}]}

    elif name == "techassist_get_solution":
        intent = arguments.get("intent", "")
        kb = engine.kb.get("intencoes", {})
        if intent in kb:
            sol = kb[intent]
        else:
            sol = kb.get("fallback", {"resposta": "Procedimento não encontrado na base de conhecimento."})
        return {"content": [{"type": "text", "text": json.dumps(sol, ensure_ascii=False, indent=2)}]}

    elif name == "techassist_create_ticket":
        import random
        desc = arguments.get("description", "")
        req = arguments.get("requester", "Colaborador Corporativo")
        dep = arguments.get("department", "Geral")
        prio = arguments.get("priority", "PADRAO")
        proto = f"TK-{random.randint(10000, 99999)}"
        ticket = create_ticket(protocolo=proto, descricao=desc, intencao="abertura_chamado",
                               confianca=1.0, solicitante=req, departamento=dep, prioridade=prio)
        return {"content": [{"type": "text", "text": json.dumps(ticket, ensure_ascii=False, indent=2)}]}

    elif name == "techassist_list_tickets":
        st = arguments.get("status")
        pr = arguments.get("priority")
        tickets = list_tickets(status=st, prioridade=pr)
        return {"content": [{"type": "text", "text": json.dumps({"total": len(tickets), "tickets": tickets}, ensure_ascii=False, indent=2)}]}

    elif name == "techassist_explain_prediction":
        q = arguments.get("query", "")
        exp = engine.classifier.explain(q)
        return {"content": [{"type": "text", "text": json.dumps(exp, ensure_ascii=False, indent=2)}]}

    else:
        return {"isError": True, "content": [{"type": "text", "text": f"Ferramenta desconhecida: {name}"}]}

def run_stdio_server():
    """Lê requisições JSON-RPC 2.0 da stdin e responde na stdout."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            req_id = req.get("id")
            method = req.get("method")

            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "techassist-mcp-server", "version": "1.0.0"}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"tools": TOOLS}
                }
            elif method == "tools/call":
                params = req.get("params", {})
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                res = handle_call_tool(tool_name, tool_args)
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": res
                }
            else:
                resp = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method {method} not found"}
                }
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(e)}
            }
            sys.stdout.write(json.dumps(err_resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    run_stdio_server()
