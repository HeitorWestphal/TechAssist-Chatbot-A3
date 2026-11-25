"""Testes unitários e de integração para o IntentClassifier.
Verifica treinamento, previsões, cálculo de probabilidades, similaridade por cossenos,
mecanismo de limiar de confiança (threshold) e fallback.
"""

import os
import pytest
from src.intent_classifier import IntentClassifier

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "training_dataset.csv")

@pytest.fixture(scope="module")
def trained_classifier():
    clf = IntentClassifier(confidence_threshold=0.38)
    clf.train(DATA_PATH)
    return clf

def test_classifier_is_trained(trained_classifier):
    assert trained_classifier.is_trained is True
    assert len(trained_classifier.classes_) >= 7
    assert "redefinicao_senha" in trained_classifier.classes_
    assert "problema_vpn_acesso" in trained_classifier.classes_
    assert "abertura_chamado" in trained_classifier.classes_

def test_predict_reset_senha(trained_classifier):
    res = trained_classifier.predict("Como faco para redefinir a minha senha?")
    assert res["intencao"] == "redefinicao_senha"
    assert res["is_fallback"] is False
    assert res["confianca"] >= 0.38
    assert "latencia_ms" in res
    assert res["latencia_ms"] < 50.0  # Inferência em sub-milissegundos

def test_predict_problema_vpn(trained_classifier):
    res = trained_classifier.predict("Minha VPN do FortiClient nao conecta e da erro de timeout")
    assert res["intencao"] == "problema_vpn_acesso"
    assert res["is_fallback"] is False

def test_predict_abrir_chamado(trained_classifier):
    res = trained_classifier.predict("Quero abrir um chamado com um tecnico humano urgente")
    assert res["intencao"] == "abertura_chamado"
    assert res["is_fallback"] is False

def test_fallback_out_of_domain(trained_classifier):
    # Frase completamente fora do domínio
    res = trained_classifier.predict("Receita de bolo de cenoura com cobertura de chocolate")
    assert res["intencao"] == "fora_escopo"
    assert res["is_fallback"] is True

def test_fallback_empty_or_stopwords(trained_classifier):
    res = trained_classifier.predict("e de que para com")
    assert res["intencao"] == "fora_escopo"
    assert res["is_fallback"] is True
    assert res["confianca"] == 0.0

def test_explain_tokens(trained_classifier):
    explanation = trained_classifier.explain("minha conexao vpn caiu")
    assert "termos_tfidf_encontrados" in explanation
    assert any("vpn" in term or "conexao" in term for term in explanation["termos_tfidf_encontrados"].keys())
    assert explanation["diagnostico_predicao"]["intencao"] == "problema_vpn_acesso"
