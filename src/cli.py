"""
Interface Interativa de Linha de Comando (CLI) para o TechAssist.
Permite testar e demonstrar o funcionamento do chatbot diretamente no terminal.
"""

import sys
from src.bot_engine import BotEngine

def main():
    print("=" * 65)
    print("      TECHASSIST AI - CENTRAL DE SUPORTE DE TI (CLI N1)")
    print("=" * 65)
    print("Carregando modelo de PLN e base de conhecimento...")
    
    engine = BotEngine(
        kb_path="data/knowledge_base.json",
        dataset_path="data/training_dataset.csv",
        threshold=0.38
    )
    
    print("\n✓ Modelo de IA carregado e pronto para atendimento!")
    print("Digite sua mensagem para iniciar ou 'sair' para encerrar.")
    print("Para inspecionar a IA, digite 'debug: <sua frase>'")
    print("-" * 65)

    session_id = "cli_user"
    
    # Mensagem inicial do bot
    initial_res = engine.process_message("olá", session_id=session_id)
    print(f"\n[TechAssist]: {initial_res['resposta']}\n")

    while True:
        try:
            user_input = input("[Você]: ").strip()
            if not user_input:
                continue

            if user_input.lower() in ["sair", "exit", "quit"]:
                print("\nEncerrando sessão de atendimento. Até logo!")
                break

            if user_input.startswith("debug:"):
                query = user_input.replace("debug:", "").strip()
                explanation = engine.classifier.explain(query)
                print("\n" + "=" * 50)
                print("         DIAGNÓSTICO TÉCNICO DE IA")
                print("=" * 50)
                print(f"Texto original:    {explanation['texto_original']}")
                print(f"Texto limpo:       {explanation['texto_normalizado']}")
                print(f"Termos TF-IDF:     {explanation['termos_tfidf_encontrados']}")
                diag = explanation["diagnostico_predicao"]
                print(f"Intenção prevista: {diag['intencao']}")
                print(f"Confiança:         {diag['confianca']} (Limiar: {diag['limiar_aplicado']})")
                print(f"Fallback acionado: {diag['is_fallback']}")
                print("=" * 50 + "\n")
                continue

            response = engine.process_message(user_input, session_id=session_id)
            
            print(f"\n[TechAssist]: {response['resposta']}")
            print(f"\n[Metadados IA] Intenção: {response['intencao']} | Confiança: {response['confianca'] * 100:.1f}% | Fallback: {response['is_fallback']}")
            
            if response.get("acoes_sugeridas"):
                print("Sugestões: " + " | ".join(response["acoes_sugeridas"]))
            print("-" * 65 + "\n")

        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando sessão...")
            break

if __name__ == "__main__":
    main()
