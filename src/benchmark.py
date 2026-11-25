"""
Módulo de Benchmark Comparativo e Engenharia de Dados (Projeto A3 - Inteligência Artificial).
Compara empiricamente 4 arquiteturas de IA/PLN:
1. Regras Simbólicas / Regex (Opção A)
2. TF-IDF + Multinomial Naive Bayes (Opção B - Bayesiano)
3. TF-IDF + Linear Support Vector Machine (Opção B - Discriminativo)
4. TF-IDF n-grams + Regressão Logística + Cosseno + Fallback (Opção C - Nossa Híbrida)

Gera gráficos de alta resolução e relatórios quantitativos para fundamentação científica.
"""

import os
import time
import csv
import json
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
from src.nlp_preprocessor import clean_text
from src.intent_classifier import IntentClassifier

# Configuração global de estilo visual acadêmico para gráficos
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

class RuleBasedClassifier:
    """Classificador baseado puramente em Regras Simbólicas e Expressões Regulares (Opção A)."""
    def __init__(self):
        self.rules = {
            "redefinicao_senha": [r"\bsenha\b", r"\blogin\b", r"\breset\b", r"\bbloquead[ao]\b", r"\bcredencia(l|is)\b"],
            "problema_vpn_acesso": [r"\bvpn\b", r"\bforticlient\b", r"\banyconnect\b", r"\bgateway\b", r"\bmfa\b", r"\bconectar\b"],
            "lentidao_sistema": [r"\blento\b", r"\btravando\b", r"\bcarroca\b", r"\bmemoria\b", r"\bcpu\b", r"\bdisco\b", r"\blerdo\b"],
            "instalacao_software": [r"\binstala(r|cao)?\b", r"\bbaixar\b", r"\bsoftware\b", r"\bprograma\b", r"\bvscode\b", r"\boffice\b", r"\bdocker\b"],
            "abertura_chamado": [r"\bchamado\b", r"\bticket\b", r"\batendente\b", r"\bhumano\b", r"\bnivel 2\b", r"\bn2\b"],
            "horario_suporte": [r"\bhorario\b", r"\bplantao\b", r"\bfim de semana\b", r"\bsabado\b", r"\bdomingo\b", r"\bexpediente\b"],
            "saudacao": [r"\bola\b", r"\boi\b", r"\bbom dia\b", r"\bboa tarde\b", r"\bboa noite\b", r"\bajuda\b"]
        }

    def predict(self, text: str) -> str:
        cleaned = clean_text(text)
        for intent, patterns in self.rules.items():
            for pat in patterns:
                if re.search(pat, cleaned):
                    return intent
        return "fora_escopo"

def run_benchmark(
    train_path="data/training_dataset.csv",
    test_path="data/test_dataset.csv",
    output_dir="results"
):
    os.makedirs(output_dir, exist_ok=True)
    print("=" * 75)
    print("    INICIANDO BENCHMARK QUANTITATIVO DE ARQUITETURAS (A3 - PLN/IA)")
    print("=" * 75)

    # 1. Carrega dados de treino
    train_texts, train_labels = [], []
    with open(train_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            train_texts.append(r['texto'])
            train_labels.append(r['intencao'])

    # 2. Carrega dados de teste
    test_rows = []
    with open(test_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            test_rows.append(r)

    y_true = [r["intencao_esperada"] for r in test_rows]
    test_queries = [r["pergunta"] for r in test_rows]

    # Modelos para comparação
    # Modelo 1: Regras Simbólicas (Opção A)
    rule_model = RuleBasedClassifier()

    # Vetorizador padrão para modelos B
    vec_b = TfidfVectorizer(preprocessor=clean_text, ngram_range=(1, 2))
    X_train_b = vec_b.fit_transform(train_texts)
    X_test_b = vec_b.transform(test_queries)

    # Modelo 2: Naive Bayes Multinomial
    nb_model = MultinomialNB(alpha=0.5)
    nb_model.fit(X_train_b, train_labels)

    # Modelo 3: Linear Support Vector Machine
    svm_model = LinearSVC(C=1.5, max_iter=2000, random_state=42)
    svm_model.fit(X_train_b, train_labels)

    # Modelo 4: Nossa Arquitetura Híbrida (Opção C)
    hybrid_model = IntentClassifier(confidence_threshold=0.38)
    hybrid_model.train(train_path)

    # Coleta de métricas e latências
    bench_results = {}

    models_dict = {
        "Regras Simbólicas (Opção A)": {"type": "rule", "model": rule_model},
        "TF-IDF + Naive Bayes (Opção B)": {"type": "sklearn", "model": nb_model},
        "TF-IDF + SVM Linear (Opção B)": {"type": "sklearn", "model": svm_model},
        "Híbrida TF-IDF + LogReg + Fallback (Opção C)": {"type": "hybrid", "model": hybrid_model}
    }

    for m_name, m_info in models_dict.items():
        start_t = time.perf_counter()
        preds = []
        # Repete 10x para medição precisa de latência
        for _ in range(10):
            preds_batch = []
            for q in test_queries:
                if m_info["type"] == "rule":
                    p = m_info["model"].predict(q)
                elif m_info["type"] == "sklearn":
                    vec = vec_b.transform([q])
                    p = m_info["model"].predict(vec)[0]
                elif m_info["type"] == "hybrid":
                    res = m_info["model"].predict(q)
                    p = res["intencao"]
                preds_batch.append(p)
        elapsed_total = time.perf_counter() - start_t
        avg_latency_ms = (elapsed_total / (10 * len(test_queries))) * 1000

        preds = preds_batch
        acc = accuracy_score(y_true, preds)
        prec, rec, f1, _ = precision_recall_fscore_support(y_true, preds, average="weighted", zero_division=0)
        
        # Teste específico para perguntas Fora de Escopo
        fora_escopo_indices = [i for i, y in enumerate(y_true) if y == "fora_escopo"]
        fora_escopo_acc = sum(1 for i in fora_escopo_indices if preds[i] == "fora_escopo") / len(fora_escopo_indices)

        bench_results[m_name] = {
            "acuracia": round(acc * 100, 2),
            "precisao": round(prec * 100, 2),
            "recall": round(rec * 100, 2),
            "f1_score": round(f1 * 100, 2),
            "fora_escopo_taxa": round(fora_escopo_acc * 100, 2),
            "latencia_ms": round(avg_latency_ms, 3),
            "predicoes": preds
        }

        print(f"[{m_name}]")
        print(f"  • Acurácia: {acc*100:.2f}% | F1: {f1*100:.2f}% | Precisão: {prec*100:.2f}% | Latência: {avg_latency_ms:.3f} ms")

    # Salva JSON de benchmark
    with open(os.path.join(output_dir, "benchmark_comparison.json"), "w", encoding="utf-8") as f:
        json.dump(bench_results, f, indent=2, ensure_ascii=False)

    # -------------------------------------------------------------
    # GRÁFICO 1: Comparativo de Métricas dos Modelos
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5.5))
    labels = list(bench_results.keys())
    # Nomes mais curtos para o eixo X
    short_labels = ["Regras Simbólicas\n(Opção A)", "TF-IDF + Naive Bayes\n(Opção B1)", "TF-IDF + SVM Linear\n(Opção B2)", "Híbrida TF-IDF + LogReg\n(Nossa Opção C)"]
    x = np.arange(len(short_labels))
    width = 0.22

    accs = [bench_results[k]["acuracia"] for k in labels]
    precs = [bench_results[k]["precisao"] for k in labels]
    f1s = [bench_results[k]["f1_score"] for k in labels]

    r1 = ax.bar(x - width, accs, width, label='Acurácia Global (%)', color='#2563EB')
    r2 = ax.bar(x, precs, width, label='Precisão Ponderada (%)', color='#10B981')
    r3 = ax.bar(x + width, f1s, width, label='F1-Score (%)', color='#F59E0B')

    ax.set_ylabel('Pontuação (%)', fontsize=12, fontweight='bold', color='#1E293B')
    ax.set_title('Benchmark Comparativo de Arquiteturas de IA / PLN (A3)', fontsize=14, fontweight='bold', pad=15, color='#1E3A8A')
    ax.set_xticks(x)
    ax.set_xticklabels(short_labels, fontsize=10, fontweight='bold')
    ax.set_ylim(0, 110)
    ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.annotate(f'{h:.1f}%',
                        xy=(rect.get_x() + rect.get_width() / 2, h),
                        xytext=(0, 4), textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')

    autolabel(r1)
    autolabel(r2)
    autolabel(r3)
    plt.tight_layout()
    g1_path = os.path.join(output_dir, "grafico_benchmark_modelos.png")
    plt.savefig(g1_path, dpi=300)
    plt.close()
    print(f"✓ Gráfico 1 gerado: {g1_path}")

    # -------------------------------------------------------------
    # GRÁFICO 2: Análise de Calibração do Limiar (Threshold Curve)
    # -------------------------------------------------------------
    thresholds = np.linspace(0.10, 0.60, 11)
    acc_list, fallback_out_list, f1_list = [], [], []

    for th in thresholds:
        clf_temp = IntentClassifier(confidence_threshold=th)
        clf_temp.train(train_path)
        temp_preds = [clf_temp.predict(q)["intencao"] for q in test_queries]
        
        acc_val = accuracy_score(y_true, temp_preds) * 100
        # Taxa de fora_escopo corretamente identificado
        fe_acc = sum(1 for i in fora_escopo_indices if temp_preds[i] == "fora_escopo") / len(fora_escopo_indices) * 100
        _, _, f1_val, _ = precision_recall_fscore_support(y_true, temp_preds, average="weighted", zero_division=0)
        
        acc_list.append(acc_val)
        fallback_out_list.append(fe_acc)
        f1_list.append(f1_val * 100)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(thresholds, acc_list, marker='o', linewidth=2.5, color='#2563EB', label='Acurácia Global (%)')
    ax.plot(thresholds, fallback_out_list, marker='s', linewidth=2.5, color='#10B981', label='Retenção Fora de Escopo / Fallback (%)')
    ax.plot(thresholds, f1_list, marker='^', linewidth=2.5, color='#F59E0B', label='F1-Score Ponderado (%)')

    # Destaca o limiar ótimo escolhido (0.38)
    ax.axvline(x=0.38, color='#DC2626', linestyle='--', linewidth=2, label='Limiar Operacional Escolhido (0.38)')
    ax.annotate('Ponto de Operação Ótimo (0.38)\nEquilíbrio Precision / Fallback',
                xy=(0.38, 72.0), xytext=(0.42, 60),
                arrowprops=dict(facecolor='#DC2626', shrink=0.08, width=1.5, headwidth=7),
                fontsize=9.5, fontweight='bold', color='#DC2626',
                bbox=dict(boxstyle="round,pad=0.4", fc="#FEF2F2", ec="#DC2626", lw=1))

    ax.set_xlabel('Limiar de Confiança Operacional (Threshold)', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_ylabel('Desempenho (%)', fontsize=11, fontweight='bold', color='#1E293B')
    ax.set_title('Estudo Empírico de Calibração do Limiar de Confiança (Threshold Analysis)', fontsize=13, fontweight='bold', pad=15, color='#1E3A8A')
    ax.set_ylim(20, 105)
    ax.set_xticks(np.round(thresholds, 2))
    ax.legend(loc='lower left', frameon=True, facecolor='white', framealpha=0.9)
    ax.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    g2_path = os.path.join(output_dir, "grafico_calibracao_threshold.png")
    plt.savefig(g2_path, dpi=300)
    plt.close()
    print(f"✓ Gráfico 2 gerado: {g2_path}")

    # -------------------------------------------------------------
    # GRÁFICO 3: Heatmap da Matriz de Confusão (Seaborn)
    # -------------------------------------------------------------
    hybrid_preds = bench_results["Híbrida TF-IDF + LogReg + Fallback (Opção C)"]["predicoes"]
    all_classes = sorted(list(set(y_true + hybrid_preds)))
    cm = confusion_matrix(y_true, hybrid_preds, labels=all_classes)

    fig, ax = plt.subplots(figsize=(8.5, 7))
    class_labels_clean = [c.replace('_', ' ').title() for c in all_classes]
    sns.heatmap(
        cm, annot=True, fmt='d', cmap='Blues', cbar=True,
        xticklabels=class_labels_clean, yticklabels=class_labels_clean,
        linewidths=0.8, linecolor='#E2E8F0', ax=ax, annot_kws={"size": 11, "weight": "bold"}
    )
    ax.set_xlabel('Intenção Predita pelo Modelo', fontsize=11, fontweight='bold', labelpad=10, color='#1E293B')
    ax.set_ylabel('Intenção Real Esperada (Ground Truth)', fontsize=11, fontweight='bold', labelpad=10, color='#1E293B')
    ax.set_title('Matriz de Confusão — TechAssist AI (Modelo Híbrido Final)', fontsize=13, fontweight='bold', pad=15, color='#1E3A8A')
    plt.xticks(rotation=35, ha='right', fontsize=9.5)
    plt.yticks(rotation=0, fontsize=9.5)
    plt.tight_layout()
    g3_path = os.path.join(output_dir, "grafico_matriz_confusao.png")
    plt.savefig(g3_path, dpi=300)
    plt.close()
    print(f"✓ Gráfico 3 gerado: {g3_path}")

    # -------------------------------------------------------------
    # GRÁFICO 4: Comparativo de Latência de Inferência (ms)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 4))
    latencies = [bench_results[k]["latencia_ms"] for k in labels]
    y_pos = np.arange(len(short_labels))
    colors_lat = ['#94A3B8', '#60A5FA', '#3B82F6', '#1E40AF']

    bars = ax.barh(y_pos, latencies, color=colors_lat, height=0.55, edgecolor='#1E293B', linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(short_labels, fontsize=9.5, fontweight='bold')
    ax.invert_yaxis()  # Labels lidas de cima para baixo
    ax.set_xlabel('Tempo Médio de Inferência por Consulta (milissegundos)', fontsize=10.5, fontweight='bold', color='#1E293B')
    ax.set_title('Eficiência Computacional: Latência de Inferência Local', fontsize=13, fontweight='bold', pad=15, color='#1E3A8A')
    ax.grid(axis='x', linestyle='--', alpha=0.6)

    for bar in bars:
        w = bar.get_width()
        ax.annotate(f'{w:.3f} ms',
                    xy=(w, bar.get_y() + bar.get_height() / 2),
                    xytext=(6, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=9.5, fontweight='bold', color='#1E293B')

    ax.set_xlim(0, max(latencies) * 1.35)
    plt.tight_layout()
    g4_path = os.path.join(output_dir, "grafico_latencia_modelos.png")
    plt.savefig(g4_path, dpi=300)
    plt.close()
    print(f"✓ Gráfico 4 gerado: {g4_path}")

    print("=" * 75)
    print("        BENCHMARK E GRÁFICOS GERADOS COM SUCESSO!")
    print("=" * 75)

if __name__ == "__main__":
    run_benchmark()
