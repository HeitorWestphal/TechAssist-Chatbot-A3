"""Testes unitários para o módulo nlp_preprocessor.
Verifica normalização de acentos, filtragem de stopwords, tokenização e corretor por Levenshtein.
"""

import pytest
from src.nlp_preprocessor import (
    remove_accents,
    levenshtein_distance,
    correct_word,
    clean_text,
    tokenize,
    STOPWORDS_PT,
    CANONICAL_IT_VOCAB
)

def test_remove_accents():
    assert remove_accents("olá, você está aí?") == "ola, voce esta ai?"
    assert remove_accents("configuração de rede e atenção") == "configuracao de rede e atencao"
    assert remove_accents("COMPUTAÇÃO") == "COMPUTACAO"
    assert remove_accents("") == ""

def test_levenshtein_distance():
    # Palavras idênticas -> distância 0
    assert levenshtein_distance("senha", "senha") == 0
    # Inserção
    assert levenshtein_distance("vpn", "vpna") == 1
    # Remoção
    assert levenshtein_distance("login", "logi") == 1
    # Substituição
    assert levenshtein_distance("rede", "rodo") == 2
    # Caso vazio
    assert levenshtein_distance("", "teste") == 5
    assert levenshtein_distance("teste", "") == 5

def test_correct_word_canonical_match():
    # Palavra perfeita não deve mudar
    assert correct_word("senha") == "senha"
    assert correct_word("vpn") == "vpn"

    # Erro de digitação com distância 1
    assert correct_word("ssnha") == "senha"
    assert correct_word("computado") == "computador"
    assert correct_word("reinicia") == "reiniciar"

    # Palavras muito curtas (<= 3 chars) ou fora de alcance não devem ser forçadas
    assert correct_word("xyz") == "xyz"

def test_clean_text_basic():
    raw = "Olá! Gostaria de redefinir a minha senha do Windows, por favor."
    cleaned = clean_text(raw, remove_stops=True, apply_spellcheck=False)
    # Deve conter termos chave sem acento e sem pontuação
    assert "redefinir" in cleaned
    assert "senha" in cleaned
    assert "windows" in cleaned
    # Stopwords comuns devem ter sido filtradas
    assert "minha" not in cleaned.split()
    assert "do" not in cleaned.split()

def test_clean_text_with_spellcheck():
    raw = "esquessi a ssnha do meu usuario"
    cleaned = clean_text(raw, remove_stops=True, apply_spellcheck=True)
    # ssnha -> senha
    assert "senha" in cleaned
    assert "usuario" in cleaned

def test_clean_text_edge_cases():
    assert clean_text("") == ""
    assert clean_text(None) == ""
    assert clean_text("!@#$%^&*()") == ""

def test_tokenize():
    tokens = tokenize("preciso de suporte urgente")
    assert isinstance(tokens, list)
    assert "suporte" in tokens
    assert "urgente" in tokens
