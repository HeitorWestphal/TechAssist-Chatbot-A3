"""
Módulo de Banco de Dados Relacional SQLite para Persistência de Chamados de TI.
Implementa governança e rastreabilidade conforme ITIL v4 e LGPD.
"""

import os
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), "data", "techassist.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Cria a tabela de tickets se ela não existir e popula com dados iniciais de auditoria."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                protocolo TEXT UNIQUE NOT NULL,
                solicitante TEXT NOT NULL DEFAULT 'Colaborador Corporativo',
                departamento TEXT DEFAULT 'Geral',
                descricao TEXT NOT NULL,
                intencao_detectada TEXT NOT NULL,
                confianca_ia REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'ABERTO', -- ABERTO, EM_ATENDIMENTO, RESOLVIDO
                prioridade TEXT NOT NULL DEFAULT 'PADRAO', -- BAIXA, PADRAO, ALTA, CRITICA
                data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
                data_resolucao DATETIME
            )
        """)
        conn.commit()

        # Seed inicial se estiver vazio
        cursor.execute("SELECT COUNT(*) FROM tickets")
        if cursor.fetchone()[0] == 0:
            seed_data = [
                ("TK-10842", "Mariana Silva", "Controladoria", "Falha de autenticação ao tentar conectar VPN FortiClient", "problema_vpn_acesso", 0.78, "RESOLVIDO", "PADRAO", "2026-11-20 09:14:00", "2026-11-20 10:30:00"),
                ("TK-29451", "Carlos Eduardo", "Recursos Humanos", "Notebook travando após atualização de segurança do Windows 11", "lentidao_sistema", 0.65, "EM_ATENDIMENTO", "ALTA", "2026-11-23 14:22:00", None),
                ("TK-83920", "Ana Paula", "Comercial", "Conta bloqueada por excesso de tentativas no portal institucional", "redefinicao_senha", 0.82, "ABERTO", "CRITICA", "2026-11-24 08:05:00", None)
            ]
            cursor.executemany("""
                INSERT INTO tickets (protocolo, solicitante, departamento, descricao, intencao_detectada, confianca_ia, status, prioridade, data_criacao, data_resolucao)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, seed_data)
            conn.commit()

def create_ticket(protocolo: str, descricao: str, intencao: str, confianca: float,
                  solicitante: str = "Colaborador Corporativo", departamento: str = "Geral",
                  prioridade: str = "PADRAO") -> Dict[str, Any]:
    """Insere um novo ticket gerado pelo chatbot no banco de dados."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tickets (protocolo, solicitante, departamento, descricao, intencao_detectada, confianca_ia, status, prioridade)
            VALUES (?, ?, ?, ?, ?, ?, 'ABERTO', ?)
        """, (protocolo, solicitante, departamento, descricao, intencao, float(confianca), prioridade))
        conn.commit()
    return get_ticket_by_protocol(protocolo)

def get_ticket_by_protocol(protocolo: str) -> Optional[Dict[str, Any]]:
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tickets WHERE protocolo = ?", (protocolo,))
        row = cursor.fetchone()
        return dict(row) if row else None

def list_tickets(status: Optional[str] = None) -> List[Dict[str, Any]]:
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        if status:
            cursor.execute("SELECT * FROM tickets WHERE status = ? ORDER BY id DESC", (status,))
        else:
            cursor.execute("SELECT * FROM tickets ORDER BY id DESC")
        rows = cursor.fetchall()
        return [dict(r) for r in rows]

def update_ticket_status(protocolo: str, novo_status: str) -> bool:
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        data_res = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if novo_status == "RESOLVIDO" else None
        cursor.execute("""
            UPDATE tickets SET status = ?, data_resolucao = ? WHERE protocolo = ?
        """, (novo_status, data_res, protocolo))
        conn.commit()
        return cursor.rowcount > 0

# Inicializa ao carregar módulo
init_db()
