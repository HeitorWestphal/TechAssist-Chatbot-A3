"""
Módulo de Pré-Processamento de Linguagem Natural (PLN) para o TechAssist.
Implementa normalização textual, remoção de caracteres especiais,
tratamento de acentuação e filtragem de ruído sem dependência externa pesada.
"""

import re
import unicodedata

# Lista de stopwords em português filtrada para reter tokens com valor semântico
# (ex: pronomes interrogativos e negações podem alterar a intenção).
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

def remove_accents(text: str) -> str:
    """Remove marcas diacríticas e acentos mantendo caracteres ASCII base."""
    nfkd = unicodedata.normalize('NFKD', text)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

def clean_text(text: str, remove_stops: bool = True) -> str:
    """
    Normaliza a cadeia de caracteres para classificação PLN:
    1. Converte para minúsculas.
    2. Remove acentuação.
    3. Remove pontuação e caracteres não alfanuméricos.
    4. Opcionalmente remove stopwords mantendo o núcleo semântico.
    5. Normaliza múltiplos espaços em branco.
    """
    if not text or not isinstance(text, str):
        return ""

    text = text.lower().strip()
    text = remove_accents(text)
    
    # Substitui caracteres não alfanuméricos por espaço
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    
    tokens = text.split()
    
    if remove_stops:
        tokens = [t for t in tokens if t not in STOPWORDS_PT and len(t) > 1]
        
    return " ".join(tokens)

def tokenize(text: str) -> list[str]:
    """Retorna lista de tokens normalizados."""
    return clean_text(text, remove_stops=False).split()
