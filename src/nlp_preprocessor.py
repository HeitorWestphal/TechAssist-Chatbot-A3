"""
Módulo de Pré-Processamento de Linguagem Natural (PLN) para o TechAssist.
Implementa normalização textual, remoção de caracteres especiais,
tratamento de acentuação, filtragem de ruído e corretor ortográfico por Levenshtein.
"""

import re
import unicodedata
from typing import List, Set, Dict

# Lista de stopwords em português filtrada para reter tokens com valor semântico
STOPWORDS_PT = {
    "a", "ao", "aos", "aquela", "aquelas", "aquele", "aqueles", "aquilo", "as", "ate",
    "com", "da", "das", "de", "dela", "delas", "dele", "deles", "depois", "do", "dos",
    "e", "ela", "elas", "ele", "eles", "em", "entre", "era", "eram", "eramos", "essa",
    "essas", "esse", "esses", "esta", "estamos", "estao", "estas", "estava", "estavam",
    "este", "estes", "estou", "eu", "foi", "fomos", "foram", "isso", "isto", "ja", "lhe",
    "lhes", "me", "mesmo", "meu", "meus", "minha", "minhas", "muito", "na", "nas", "no",
    "nos", "nossa", "nossas", "nosso", "nossos", "num", "numa", "os", "ou", "para",
    "pela", "pelas", "pelo", "pelos", "por", "que", "se", "seja", "sejam", "sejamos",
    "sem", "sendo", "sera", "serao", "seu", "seus", "so", "sua", "suas", "tambem", "te",
    "tem", "temos", "tenham", "tenho", "um", "uma", "voces"
}

# Vocabulário canônico do domínio de TI corporativo para correção de digitação
CANONICAL_IT_VOCAB = {
    "senha", "senhas", "redefinir", "resetar", "trocar", "bloqueada", "bloqueado", "usuario", "login",
    "vpn", "conexao", "conectar", "conecta", "caiu", "caindo", "forticlient", "anyconnect", "gateway", "token", "mfa",
    "computador", "notebook", "maquina", "pc", "lento", "lerdo", "travando", "trava", "congelando",
    "memoria", "ram", "disco", "cpu", "gerenciador", "tarefas", "processos", "reiniciar",
    "instalar", "instalacao", "baixar", "software", "programa", "aplicativo", "vscode", "office", "teams", "slack", "docker",
    "chamado", "ticket", "protocolo", "atendente", "humano", "suporte", "tecnico", "ajuda", "orientacao",
    "horario", "plantao", "atendimento", "sabado", "domingo", "expediente", "ola", "bom", "dia", "tarde", "noite"
}

def remove_accents(text: str) -> str:
    """Remove marcas diacríticas e acentos mantendo caracteres ASCII base."""
    nfkd = unicodedata.normalize('NFKD', text)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

def levenshtein_distance(s1: str, s2: str) -> int:
    """Calcula a distância mínima de edição de Levenshtein entre duas palavras."""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def correct_word(word: str, max_dist: int = 2) -> str:
    """Corrige palavras com erros tipográficos buscando o termo mais próximo no vocabulário."""
    if word in CANONICAL_IT_VOCAB or len(word) <= 3 or word in STOPWORDS_PT:
        return word
    
    # Calibra a tolerância de edição de acordo com a extensão da palavra
    allowed_dist = 1 if len(word) <= 5 else max_dist
    
    best_match = word
    min_d = allowed_dist + 1
    for term in CANONICAL_IT_VOCAB:
        if abs(len(term) - len(word)) <= allowed_dist:
            d = levenshtein_distance(word, term)
            if d < min_d:
                min_d = d
                best_match = term
    return best_match if min_d <= allowed_dist else word

def clean_text(text: str, remove_stops: bool = True, apply_spellcheck: bool = False) -> str:
    """
    Normaliza a cadeia de caracteres para classificação PLN:
    1. Converte para minúsculas.
    2. Remove acentuação (NFKD).
    3. Remove pontuação e caracteres não alfanuméricos via Regex.
    4. Opcionalmente remove stopwords mantendo o núcleo semântico.
    5. Opcionalmente corrige erros de digitação via distância de Levenshtein.
    """
    if not text or not isinstance(text, str):
        return ""

    text = text.lower().strip()
    text = remove_accents(text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    tokens = text.split()

    if remove_stops:
        tokens = [t for t in tokens if t not in STOPWORDS_PT and len(t) > 1]

    if apply_spellcheck:
        tokens = [correct_word(t) for t in tokens]
        
    return " ".join(tokens)

def tokenize(text: str) -> List[str]:
    """Retorna lista de tokens normalizados."""
    return clean_text(text, remove_stops=False).split()
