"""Módulo de Recuperação de Informação Lexical e Probabilística: Okapi BM25 vs TF-IDF.
Implementa o algoritmo probabilístico Okapi BM25 em Python puro (zero dependências pesadas)
e compara empiricamente métricas de Precision@1, Precision@3 e Mean Reciprocal Rank (MRR)
contra o modelo vetorial TF-IDF clássico sobre o corpus de helpdesk corporativo.
"""
import os
import sys
import math
import json
import csv
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.nlp_preprocessor import clean_text, tokenize

DATA_DIR = os.path.join(BASE_DIR, "data")
RESULTS_DIR = os.path.join(BASE_DIR, "results")

class OkapiBM25:
    """Implementação canônica do algoritmo Okapi BM25 para recuperação de procedimentos de TI."""
    def __init__(self, corpus: list, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = len(corpus)
        self.doc_lengths = [len(doc) for doc in corpus]
        self.avg_doc_len = sum(self.doc_lengths) / self.corpus_size if self.corpus_size > 0 else 1.0
        self.corpus = corpus
        self.doc_freqs = Counter()
        self.idf = {}
        self._initialize()

    def _initialize(self):
        for doc in self.corpus:
            unique_terms = set(doc)
            for term in unique_terms:
                self.doc_freqs[term] += 1

        for term, freq in self.doc_freqs.items():
            # Fórmula de IDF com suavização Robertson-Spärck Jones
            self.idf[term] = math.log((self.corpus_size - freq + 0.5) / (freq + 0.5) + 1.0)

    def score(self, query: list) -> np.ndarray:
        scores = np.zeros(self.corpus_size)
        for term in query:
            if term not in self.idf:
                continue
            idf_val = self.idf[term]
            for i, doc in enumerate(self.corpus):
                term_count = doc.count(term)
                if term_count == 0:
                    continue
                num = term_count * (self.k1 + 1.0)
                denom = term_count + self.k1 * (1.0 - self.b + self.b * (self.doc_lengths[i] / self.avg_doc_len))
                scores[i] += idf_val * (num / denom)
        return scores

def run_bm25_vs_tfidf_benchmark():
    # Carregar base de treino e teste
    train_texts, train_intents = [], []
    with open(os.path.join(DATA_DIR, "training_dataset.csv"), mode="r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            train_texts.append(r["texto"].strip())
            train_intents.append(r["intencao"].strip())

    test_queries, test_expected = [], []
    with open(os.path.join(DATA_DIR, "test_dataset.csv"), mode="r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            test_queries.append(r["pergunta"].strip())
            test_expected.append(r["intencao_esperada"].strip())

    tokenized_corpus = [tokenize(clean_text(t)) for t in train_texts]
    bm25 = OkapiBM25(tokenized_corpus)

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    tfidf_vec = TfidfVectorizer(preprocessor=clean_text, ngram_range=(1, 2))
    X_train_tfidf = tfidf_vec.fit_transform(train_texts)

    # Avaliar P@1, P@3 e MRR
    p1_bm25, p3_bm25, mrr_bm25 = 0, 0, 0.0
    p1_tfidf, p3_tfidf, mrr_tfidf = 0, 0, 0.0
    p1_hybrid, p3_hybrid, mrr_hybrid = 0, 0, 0.0

    total_valid = 0

    for q, exp in zip(test_queries, test_expected):
        if exp == "fora_escopo":
            continue
        total_valid += 1

        # BM25
        q_tokens = tokenize(clean_text(q))
        scores_bm = bm25.score(q_tokens)
        ranked_bm_idx = np.argsort(scores_bm)[::-1]
        ranked_bm_intents = [train_intents[i] for i in ranked_bm_idx]

        # TF-IDF Cosine
        q_vec = tfidf_vec.transform([clean_text(q)])
        sims_tfidf = cosine_similarity(q_vec, X_train_tfidf)[0]
        ranked_tf_idx = np.argsort(sims_tfidf)[::-1]
        ranked_tf_intents = [train_intents[i] for i in ranked_tf_idx]

        # Híbrido Ponderado (Normalizado 0-1)
        norm_bm = scores_bm / (np.max(scores_bm) + 1e-6) if np.max(scores_bm) > 0 else scores_bm
        norm_tf = sims_tfidf / (np.max(sims_tfidf) + 1e-6) if np.max(sims_tfidf) > 0 else sims_tfidf
        hybrid_scores = 0.5 * norm_bm + 0.5 * norm_tf
        ranked_hy_idx = np.argsort(hybrid_scores)[::-1]
        ranked_hy_intents = [train_intents[i] for i in ranked_hy_idx]

        # Métricas BM25
        if ranked_bm_intents[0] == exp:
            p1_bm25 += 1
        if exp in ranked_bm_intents[:3]:
            p3_bm25 += 1
        rank_bm = (ranked_bm_intents.index(exp) + 1) if exp in ranked_bm_intents else 99
        mrr_bm25 += (1.0 / rank_bm)

        # Métricas TF-IDF
        if ranked_tf_intents[0] == exp:
            p1_tfidf += 1
        if exp in ranked_tf_intents[:3]:
            p3_tfidf += 1
        rank_tf = (ranked_tf_intents.index(exp) + 1) if exp in ranked_tf_intents else 99
        mrr_tfidf += (1.0 / rank_tf)

        # Métricas Híbrido
        if ranked_hy_intents[0] == exp:
            p1_hybrid += 1
        if exp in ranked_hy_intents[:3]:
            p3_hybrid += 1
        rank_hy = (ranked_hy_intents.index(exp) + 1) if exp in ranked_hy_intents else 99
        mrr_hybrid += (1.0 / rank_hy)

    results = {
        "TF-IDF Vetorial (Cosseno)": {
            "p_at_1": round(p1_tfidf / total_valid * 100, 2),
            "p_at_3": round(p3_tfidf / total_valid * 100, 2),
            "mrr": round(mrr_tfidf / total_valid, 3)
        },
        "Okapi BM25 Probabilístico": {
            "p_at_1": round(p1_bm25 / total_valid * 100, 2),
            "p_at_3": round(p3_bm25 / total_valid * 100, 2),
            "mrr": round(mrr_bm25 / total_valid, 3)
        },
        "Híbrido (TF-IDF + Okapi BM25)": {
            "p_at_1": round(p1_hybrid / total_valid * 100, 2),
            "p_at_3": round(p3_hybrid / total_valid * 100, 2),
            "mrr": round(mrr_hybrid / total_valid, 3)
        }
    }

    json_path = os.path.join(RESULTS_DIR, "benchmark_bm25_vs_tfidf.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Plot Figura 18 com layout limpo e sem sobreposição
    fig, ax = plt.subplots(figsize=(9.5, 5.2), dpi=300)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#f8fafc")

    x = np.arange(len(results))
    width = 0.25

    p1_vals = [results[m]["p_at_1"] for m in results]
    p3_vals = [results[m]["p_at_3"] for m in results]
    mrr_vals = [results[m]["mrr"] * 100 for m in results]

    b1 = ax.bar(x - width, p1_vals, width, label="Precision@1 (%)", color="#2563eb", edgecolor="#1e293b", linewidth=1.1)
    b2 = ax.bar(x, p3_vals, width, label="Precision@3 (%)", color="#10b981", edgecolor="#1e293b", linewidth=1.1)
    b3 = ax.bar(x + width, mrr_vals, width, label="MRR Normalizado (x100)", color="#f59e0b", edgecolor="#1e293b", linewidth=1.1)

    for bars in [b1, b2, b3]:
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., h + 1.2, f"{h:.1f}", ha="center", va="bottom",
                    fontsize=8.5, fontweight="bold", color="#0f172a")

    ax.set_xticks(x)
    ax.set_xticklabels(list(results.keys()), fontsize=10, fontweight="bold", color="#0f172a")
    ax.set_ylabel("Métrica de Recuperação (%)", fontsize=11, fontweight="bold", color="#0f172a", labelpad=8)
    ax.set_ylim(0, 118)
    ax.grid(True, axis="y", linestyle=":", alpha=0.6, color="#94a3b8")
    ax.legend(loc="upper left", frameon=True, facecolor="#ffffff", edgecolor="#cbd5e1", fontsize=9.5)

    plt.title("Figura 18 — Benchmark de Recuperação de Informação: Okapi BM25 vs TF-IDF Vetorial\n"
              "Avaliação de Precisão Semântica (P@1, P@3) e Mean Reciprocal Rank (MRR)",
              fontsize=11.5, fontweight="bold", pad=16, color="#0f172a")

    plt.tight_layout()
    out_path = os.path.join(RESULTS_DIR, "grafico_benchmark_bm25_vs_tfidf.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"[OK] Gráfico BM25 vs TF-IDF salvo em: {out_path}")
    return results

if __name__ == "__main__":
    run_bm25_vs_tfidf_benchmark()
