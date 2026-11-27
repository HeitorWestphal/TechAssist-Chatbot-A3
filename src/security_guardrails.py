"""Módulo de Segurança Corporativa, Sanitização e Governança LGPD.
Responsável por:
1. Detecção e Mascaramento de Dados Sensíveis (PII: CPF, Cartões, Senhas, E-mails) em conformidade com a LGPD;
2. Bloqueio Preventivo de Injeção SQL (SQLi) e Injeção de Prompt / Jailbreaks;
3. Sanitização contra Cross-Site Scripting (XSS);
4. Auditoria de eventos de segurança.
"""
import re
from typing import Dict, Tuple

# Expressões Regulares de PII
REGEX_CPF = r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b'
REGEX_CREDIT_CARD = r'\b(?:\d{4}[ -]?){3}\d{4}\b'
REGEX_EMAIL = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
REGEX_PASSWORD_PATTERNS = r'(?i)\b(?:senha|password|passwd|pwd)\s*[:=]\s*([^\s,;]+)'

# Expressões de Injeção SQL
SQLI_PATTERNS = [
    r'(?i)\b(union\s+select)\b',
    r'(?i)\b(or\s+1\s*=\s*1)\b',
    r'(?i)\b(drop\s+table)\b',
    r'(?i)\b(insert\s+into)\b',
    r'(?i)\b(delete\s+from)\b',
    r'(?i)(--|\/\*|\*\/|;)'
]

# Expressões de Prompt Injection / Jailbreak
PROMPT_INJECTION_PATTERNS = [
    r'(?i)\b(ignore\s+(all\s+)?(previous|prior)\s+instructions?)\b',
    r'(?i)\b(system\s+prompt)\b',
    r'(?i)\b(voc[eê]\s+agora\s+[eé]\s+um(a)?\s+ia\s+sem\s+regras)\b',
    r'(?i)\b(dan\s+mode|jailbreak)\b'
]

class SecurityGuardrails:
    def __init__(self):
        self.stats = {
            "pii_masked_count": 0,
            "sqli_blocked_count": 0,
            "prompt_injection_blocked_count": 0,
            "xss_sanitized_count": 0
        }

    def inspect_and_sanitize(self, text: str) -> Tuple[str, Dict[str, any]]:
        """Analisa o texto, verifica ameaças, aplica mascaramento LGPD e sanitiza XSS."""
        if not text:
            return text, {"is_safe": True, "violations": []}

        violations = []
        is_safe = True

        # 1. Checagem de SQL Injection
        for pattern in SQLI_PATTERNS:
            if re.search(pattern, text):
                violations.append("SQL_INJECTION_DETECTED")
                is_safe = False
                self.stats["sqli_blocked_count"] += 1
                break

        # 2. Checagem de Prompt Injection
        for pattern in PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, text):
                violations.append("PROMPT_INJECTION_DETECTED")
                is_safe = False
                self.stats["prompt_injection_blocked_count"] += 1
                break

        # 3. Mascaramento LGPD de Dados Pessoais Identificáveis (PII)
        sanitized = text
        masked_pii = False

        if re.search(REGEX_CPF, sanitized):
            sanitized = re.sub(REGEX_CPF, "[CPF_PROTEGIDO_LGPD]", sanitized)
            masked_pii = True

        if re.search(REGEX_CREDIT_CARD, sanitized):
            sanitized = re.sub(REGEX_CREDIT_CARD, "[CARTAO_PROTEGIDO_LGPD]", sanitized)
            masked_pii = True

        if re.search(REGEX_EMAIL, sanitized):
            sanitized = re.sub(REGEX_EMAIL, "[EMAIL_PROTEGIDO_LGPD]", sanitized)
            masked_pii = True

        if re.search(REGEX_PASSWORD_PATTERNS, sanitized):
            sanitized = re.sub(REGEX_PASSWORD_PATTERNS, r"senha: [SENHA_OCULTADA_LGPD]", sanitized)
            masked_pii = True

        if masked_pii:
            self.stats["pii_masked_count"] += 1

        # 4. Sanitização contra tags HTML / XSS
        if "<" in sanitized and ">" in sanitized:
            old_san = sanitized
            sanitized = re.sub(r'<[^>]*>', '', sanitized)
            if sanitized != old_san:
                self.stats["xss_sanitized_count"] += 1

        security_report = {
            "is_safe": is_safe,
            "violations": violations,
            "pii_masked": masked_pii,
            "sanitized_text": sanitized
        }

        return sanitized, security_report

security_guard = SecurityGuardrails()
