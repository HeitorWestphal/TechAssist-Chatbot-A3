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

        # Tabela de Feedback Humano e Curadoria (Active Learning / RLHF)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS active_learning_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT,
                pergunta TEXT NOT NULL,
                intencao_predita TEXT NOT NULL,
                confianca_ia REAL NOT NULL,
                avaliacao_usuario INTEGER NOT NULL, -- 1 (Positivo), -1 (Negativo)
                comentario_ou_correcao TEXT,
                intencao_corrigida TEXT,
                status TEXT DEFAULT 'PENDENTE_REVISAO', -- PENDENTE_REVISAO, APROVADO_TREINO, REJEITADO
                data_registro DATETIME DEFAULT CURRENT_TIMESTAMP
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
        # Previne colisões randômicas de protocolo
        cursor.execute("SELECT id FROM tickets WHERE protocolo = ?", (protocolo,))
        if cursor.fetchone():
            import random
            protocolo = f"{protocolo}_{random.randint(100, 9999)}"
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

def list_tickets(status: Optional[str] = None, prioridade: Optional[str] = None) -> List[Dict[str, Any]]:
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM tickets WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        if prioridade:
            query += " AND prioridade = ?"
            params.append(prioridade)
        query += " ORDER BY id DESC"
        cursor.execute(query, params)
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

# -------------------------------------------------------------
# FUNÇÕES DE APRENDIZADO ATIVO (ACTIVE LEARNING / RLHF)
# -------------------------------------------------------------
def add_feedback(session_id: str, pergunta: str, intencao_predita: str,
                 confianca_ia: float, avaliacao: int,
                 comentario: Optional[str] = None, intencao_corrigida: Optional[str] = None) -> int:
    """Registra feedback do usuário sobre uma resposta do chatbot."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO active_learning_feedback 
            (session_id, pergunta, intencao_predita, confianca_ia, avaliacao_usuario, comentario_ou_correcao, intencao_corrigida, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'PENDENTE_REVISAO')
        """, (session_id, pergunta, intencao_predita, float(confianca_ia), int(avaliacao), comentario, intencao_corrigida))
        conn.commit()
        return cursor.lastrowid

def list_feedback(status: Optional[str] = None) -> List[Dict[str, Any]]:
    """Lista os feedbacks de usuários para curadoria humana."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM active_learning_feedback WHERE 1=1"
        params = []
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY id DESC"
        cursor.execute(query, params)
        return [dict(r) for r in cursor.fetchall()]

def approve_feedback_for_training(feedback_id: int, intencao_corrigida: str) -> bool:
    """Aprova uma sentença com rótulo correto para enriquecimento do corpus de treino."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE active_learning_feedback
            SET status = 'APROVADO_TREINO', intencao_corrigida = ?
            WHERE id = ?
        """, (intencao_corrigida, feedback_id))
        conn.commit()
        return cursor.rowcount > 0

def get_feedback_stats() -> Dict[str, Any]:
    """Retorna estatísticas consolidadas de feedback e curadoria."""
    init_db()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM active_learning_feedback")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM active_learning_feedback WHERE avaliacao_usuario = 1")
        positivos = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM active_learning_feedback WHERE avaliacao_usuario = -1")
        negativos = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM active_learning_feedback WHERE status = 'APROVADO_TREINO'")
        aprovados = cursor.fetchone()[0]
        return {
            "total_feedbacks": total,
            "positivos": positivos,
            "negativos": negativos,
            "aprovados_treino": aprovados,
            "satisfacao_percent": round((positivos / total * 100), 1) if total > 0 else 100.0
        }

# Inicializa ao carregar módulo
init_db()
