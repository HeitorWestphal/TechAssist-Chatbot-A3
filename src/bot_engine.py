"""
Motor de Diálogo e Orquestração do TechAssist.
Coordena o fluxo completo (Entrada -> Pré-Processamento -> Classificação IA ->
Consulta à Base de Conhecimento -> Gestão de Estado/Contexto -> Resposta).
"""

import json
import random
import os
from typing import Dict, Any, List
from src.intent_classifier import IntentClassifier

class BotEngine:
    def __init__(self, kb_path: str, dataset_path: str, threshold: float = 0.38):
        self.kb_path = kb_path
        self.dataset_path = dataset_path
        self.classifier = IntentClassifier(confidence_threshold=threshold)
        
        # Carrega a base de conhecimento
        with open(kb_path, 'r', encoding='utf-8') as f:
            self.kb = json.load(f)
            
        # Treina o modelo com o dataset
        self.classifier.train(dataset_path)
        
        # Dicionário de sessões ativas para gerenciamento de contexto de conversa
        # (ex: estado de abertura de chamado)
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def get_or_create_session(self, session_id: str) -> Dict[str, Any]:
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "state": "IDLE", # IDLE, AWAITING_TICKET_DETAILS
                "ticket_data": {},
                "history": []
            }
        return self.sessions[session_id]

    def reset_session(self, session_id: str):
        self.sessions[session_id] = {
            "state": "IDLE",
            "ticket_data": {},
            "history": []
        }

    def process_message(self, user_message: str, session_id: str = "default") -> Dict[str, Any]:
        """
        Executa o pipeline conversacional completo:
        1. Verificação de estado/contexto de conversação ativo.
        2. Classificação de intenção via IA (TF-IDF + Modelo).
        3. Decisão de resposta ou acionamento de fallback.
        4. Geração de resposta estruturada com metadados.
        """
        session = self.get_or_create_session(session_id)
        msg_clean = user_message.strip()

        # Contexto: Se o usuário estiver no fluxo interativo de abertura de ticket
        if session["state"] == "AWAITING_TICKET_DETAILS":
            ticket_id = f"TK-{random.randint(10000, 99999)}"
            session["state"] = "IDLE"
            session["ticket_data"]["detalhes"] = msg_clean
            session["ticket_data"]["protocolo"] = ticket_id
            
            response_text = (
                f"✅ **Chamado Registrado com Sucesso!**\n\n"
                f"• **Protocolo:** `#{ticket_id}`\n"
                f"• **Descrição informada:** \"{msg_clean}\"\n"
                f"• **Fila:** Suporte Técnico N2 (Prioridade Padrão)\n"
                f"• **SLA de Atendimento:** até 4 horas úteis.\n\n"
                f"Nossa equipe técnica entrará em contato pelo seu e-mail institucional ou ramal. "
                f"Posso te ajudar com mais alguma dúvida?"
            )
            
            result = {
                "resposta": response_text,
                "intencao": "abertura_chamado_confirmada",
                "confianca": 1.0,
                "is_fallback": False,
                "protocolo": ticket_id,
                "acoes_sugeridas": ["Consultar status de chamado", "Tirar outra dúvida", "Encerrar conversa"]
            }
            session["history"].append({"user": user_message, "bot": response_text})
            return result

        # Classificação por PLN/IA
        pred = self.classifier.predict(msg_clean)
        intent = pred["intencao"]
        confidence = pred["confianca"]
        is_fallback = pred["is_fallback"]

        # Recuperação na Base de Conhecimento
        if is_fallback or intent == "fora_escopo":
            fallback_info = self.kb["intencoes"]["fallback"]
            response_text = fallback_info["resposta"]
            acoes = fallback_info["acoes_sugeridas"]
        elif intent in self.kb["intencoes"]:
            intent_info = self.kb["intencoes"][intent]
            response_text = intent_info["resposta"]
            acoes = intent_info.get("acoes_sugeridas", [])
            
            # Se a intenção for 'abertura_chamado', ativa o estado para a próxima mensagem
            if intent == "abertura_chamado":
                session["state"] = "AWAITING_TICKET_DETAILS"
        else:
            fallback_info = self.kb["intencoes"]["fallback"]
            response_text = fallback_info["resposta"]
            acoes = fallback_info["acoes_sugeridas"]

        result = {
            "resposta": response_text,
            "intencao": intent,
            "intencao_bruta": pred.get("intencao_bruta", intent),
            "confianca": confidence,
            "similaridade_cosseno": pred.get("similaridade_cosseno", 0.0),
            "probabilidade_modelo": pred.get("probabilidade_modelo", 0.0),
            "is_fallback": is_fallback,
            "limiar_aplicado": pred.get("limiar_aplicado", 0.38),
            "acoes_sugeridas": acoes
        }

        session["history"].append({"user": user_message, "bot": response_text})
        return result
