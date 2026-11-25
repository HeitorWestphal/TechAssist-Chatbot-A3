"""
Classificador de Intenções de PLN/IA para o TechAssist.
Utiliza vetorização TF-IDF (Term Frequency - Inverse Document Frequency)
combinada com Regressão Logística e similaridade de cossenos.
Possui mecanismo de limiar de confiança (threshold) para acionamento de fallback
e suporte a inspeção analítica de probabilidades para telemetria em tempo real.
"""

import os
import csv
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
from src.nlp_preprocessor import clean_text

class IntentClassifier:
    def __init__(self, confidence_threshold: float = 0.38):
        """
        :param confidence_threshold: Limiar mínimo de probabilidade/similaridade
        necessário para aceitar a intenção. Abaixo disso, aciona fallback.
        """
        self.confidence_threshold = confidence_threshold
        
        # Vetorizador TF-IDF com unigramas e bigramas
        self.vectorizer = TfidfVectorizer(
            preprocessor=clean_text,
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=1
        )
        
        # Classificador supervisionado com regularização L2 e pesos balanceados
        self.model = LogisticRegression(
            C=3.0,
            max_iter=1000,
            class_weight='balanced',
            random_state=42
        )
        
        self.classes_ = []
        self.is_trained = False
        self.train_texts = []
        self.train_labels = []
        self.tfidf_matrix = None

    def load_training_data(self, csv_path: str):
        """Carrega dataset de treinamento de um arquivo CSV (texto, intencao)."""
        texts = []
        labels = []
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                t = row['texto'].strip()
                lbl = row['intencao'].strip()
                if t and lbl:
                    texts.append(t)
                    labels.append(lbl)
        return texts, labels

    def train(self, csv_path: str):
        """Treina o vetorizador TF-IDF e o classificador supervisionado."""
        self.train_texts, self.train_labels = self.load_training_data(csv_path)
        
        if not self.train_texts:
            raise ValueError(f"Nenhum dado encontrado no arquivo {csv_path}")

        # 1. Ajusta o vocabulário e transforma sentenças em matriz TF-IDF
        self.tfidf_matrix = self.vectorizer.fit_transform(self.train_texts)
        
        # 2. Treina o classificador de Regressão Logística
        self.model.fit(self.tfidf_matrix, self.train_labels)
        self.classes_ = list(self.model.classes_)
        self.is_trained = True
        return self

    def predict(self, text: str, apply_spellcheck: bool = False) -> dict:
        """
        Recebe uma mensagem de texto do usuário e retorna a intenção detectada,
        o score de confiança (0.0 a 1.0), distribuição de probabilidades e telemetria.
        """
        start_time = time.perf_counter()

        if not self.is_trained:
            raise RuntimeError("O modelo ainda não foi treinado. Chame train() primeiro.")

        cleaned = clean_text(text, apply_spellcheck=apply_spellcheck)
        if not cleaned:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return {
                "intencao": "fora_escopo",
                "confianca": 0.0,
                "is_fallback": True,
                "motivo": "Texto vazio ou composto exclusivamente por stopwords/pontuação.",
                "todas_probabilidades": {c: 0.0 for c in self.classes_},
                "latencia_ms": round(elapsed_ms, 3)
            }

        # Vetoriza o texto de entrada
        query_vec = self.vectorizer.transform([cleaned])

        # Se todos os termos forem OOV (Out of Vocabulary), fallback imediato
        if query_vec.nnz == 0:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return {
                "intencao": "fora_escopo",
                "confianca": 0.0,
                "is_fallback": True,
                "motivo": "Termos completamente fora do vocabulário treinado.",
                "todas_probabilidades": {c: 0.0 for c in self.classes_},
                "latencia_ms": round(elapsed_ms, 3)
            }

        # Probabilidades do modelo supervisionado
        probabilities = self.model.predict_proba(query_vec)[0]
        max_idx = int(np.argmax(probabilities))
        predicted_class = self.classes_[max_idx]
        confidence = float(probabilities[max_idx])

        # Similaridade de cosseno máxima com os exemplos de treino
        cosine_sims = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        max_cosine_sim = float(np.max(cosine_sims))

        # Score híbrido de confiança calibrado
        hybrid_confidence = float(0.65 * confidence + 0.35 * max_cosine_sim)

        # Regra de Fallback determinístico
        is_fallback = False
        if predicted_class == "fora_escopo" or hybrid_confidence < self.confidence_threshold:
            is_fallback = True
            final_intent = "fora_escopo"
        else:
            final_intent = predicted_class

        # Dicionário com a probabilidade de todas as classes para o dashboard visual
        all_probs = {c: round(float(p) * 100, 2) for c, p in zip(self.classes_, probabilities)}

        elapsed_ms = (time.perf_counter() - start_time) * 1000

        return {
            "intencao": final_intent,
            "intencao_bruta": predicted_class,
            "confianca": round(hybrid_confidence, 4),
            "probabilidade_modelo": round(confidence, 4),
            "similaridade_cosseno": round(max_cosine_sim, 4),
            "is_fallback": is_fallback,
            "limiar_aplicado": self.confidence_threshold,
            "todas_probabilidades": all_probs,
            "latencia_ms": round(elapsed_ms, 3)
        }

    def explain(self, text: str) -> dict:
        """
        Retorna detalhes para a defesa técnica da A3:
        n-gramas identificados no vocabulário e pesos TF-IDF dos termos.
        """
        cleaned = clean_text(text)
        query_vec = self.vectorizer.transform([cleaned])
        feature_names = self.vectorizer.get_feature_names_out()
        
        terms_weights = {}
        cx = query_vec.tocoo()
        for i, j, v in zip(cx.row, cx.col, cx.data):
            terms_weights[feature_names[j]] = round(float(v), 4)

        pred = self.predict(text)
        return {
            "texto_original": text,
            "texto_normalizado": cleaned,
            "termos_tfidf_encontrados": terms_weights,
            "diagnostico_predicao": pred
        }
