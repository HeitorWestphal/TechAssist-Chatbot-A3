"""
Script de Avaliação e Testes Automatizados (Requisitos R5 e R6 da A3).
Executa o conjunto formal de 25 testes, calcula métricas de desempenho
(Acurácia, Precisão, Recall, F1-Score, Matriz de Confusão e Taxa de Fallback)
e exporta os resultados para relatório e CSV.
"""

import os
import csv
import json
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from src.bot_engine import BotEngine

def run_evaluation(
    kb_path="data/knowledge_base.json",
    train_path="data/training_dataset.csv",
    test_path="data/test_dataset.csv",
    output_csv="results/test_execution_results.csv"
):
    print("=" * 70)
    print("  INICIANDO AVALIAÇÃO AUTOMATIZADA DO TECHASSIST (A3 - PLN/IA)")
    print("=" * 70)

    engine = BotEngine(kb_path, train_path, threshold=0.38)
    
    test_cases = []
    with open(test_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_cases.append(row)

    print(f"Total de casos de teste carregados: {len(test_cases)}")
    
    y_true = []
    y_pred = []
    results_rows = []
    
    correct_count = 0
    fallback_count = 0
    
    for case in test_cases:
        t_id = case["id"]
        cat = case["categoria_teste"]
        question = case["pergunta"]
        expected = case["intencao_esperada"]
        obs = case.get("observacao", "")

        pred_result = engine.classifier.predict(question)
        obtained = pred_result["intencao"]
        confidence = pred_result["confianca"]
        is_fallback = pred_result["is_fallback"]

        is_correct = (obtained == expected)
        if is_correct:
            correct_count += 1
        if is_fallback:
            fallback_count += 1

        y_true.append(expected)
        y_pred.append(obtained)

        results_rows.append({
            "id": t_id,
            "categoria_teste": cat,
            "pergunta": question,
            "intencao_esperada": expected,
            "intencao_obtida": obtained,
            "confianca": confidence,
            "acertou": "SIM" if is_correct else "NÃO",
            "is_fallback": "SIM" if is_fallback else "NÃO",
            "observacao": obs
        })

    # Salva resultados detalhados em CSV
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    fieldnames = [
        "id", "categoria_teste", "pergunta", "intencao_esperada",
        "intencao_obtida", "confianca", "acertou", "is_fallback", "observacao"
    ]
    with open(output_csv, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results_rows)

    print(f"\nResultados detalhados gravados em: {output_csv}")

    # Cálculo das métricas
    accuracy = accuracy_score(y_true, y_pred)
    all_classes = sorted(list(set(y_true + y_pred)))
    
    print("\n" + "=" * 70)
    print("                     MÉTRICAS GLOBAIS DE DESEMPENHO")
    print("=" * 70)
    print(f"• Acurácia Global (Taxa de Acerto): {accuracy * 100:.2f}% ({correct_count}/{len(test_cases)})")
    print(f"• Taxa de Fallback Acionado:        {(fallback_count / len(test_cases)) * 100:.2f}% ({fallback_count}/{len(test_cases)})")

    # Desempenho por Categoria de Teste
    print("\n" + "-" * 70)
    print("            DESEMPENHO POR CATEGORIA DE TESTE (R5)")
    print("-" * 70)
    categories = sorted(list(set(c["categoria_teste"] for c in test_cases)))
    for cat in categories:
        cat_cases = [r for r in results_rows if r["categoria_teste"] == cat]
        cat_correct = sum(1 for r in cat_cases if r["acertou"] == "SIM")
        cat_acc = (cat_correct / len(cat_cases)) * 100
        print(f"• {cat.ljust(18)}: {cat_acc:6.2f}% ({cat_correct}/{len(cat_cases)} acertos)")

    # Relatório de Classificação Detalhado
    print("\n" + "-" * 70)
    print("            RELATÓRIO DE CLASSIFICAÇÃO (PRECISÃO / RECALL / F1)")
    print("-" * 70)
    report_dict = classification_report(y_true, y_pred, labels=all_classes, zero_division=0, output_dict=True)
    print(classification_report(y_true, y_pred, labels=all_classes, zero_division=0))

    # Matriz de Confusão
    print("-" * 70)
    print("                        MATRIZ DE CONFUSÃO")
    print("-" * 70)
    cm = confusion_matrix(y_true, y_pred, labels=all_classes)
    
    # Imprime matriz legível
    header = "True \\ Pred".ljust(22) + " ".join([c[:7].center(8) for c in all_classes])
    print(header)
    for i, row in enumerate(cm):
        row_str = all_classes[i][:20].ljust(22) + " ".join([str(val).center(8) for val in row])
        print(row_str)

    # Gera resumo em formato JSON para documentação e relatórios
    metrics_summary = {
        "total_testes": len(test_cases),
        "acertos": correct_count,
        "acuracia_global": round(accuracy, 4),
        "taxa_fallback": round(fallback_count / len(test_cases), 4),
        "classes": all_classes,
        "matriz_confusao": cm.tolist(),
        "relatorio_por_classe": report_dict
    }

    with open("results/metrics_summary.json", "w", encoding="utf-8") as f:
        json.dump(metrics_summary, f, indent=2, ensure_ascii=False)

    print("\nResumo numérico salvo em: results/metrics_summary.json")
    print("=" * 70)

    return results_rows, metrics_summary

if __name__ == "__main__":
    run_evaluation()
