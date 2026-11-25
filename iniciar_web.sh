#!/usr/bin/env bash
# Script para iniciar a Interface Web do TechAssist AI
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "=========================================================="
echo "    INICIANDO TECHASSIST AI — INTERFACE WEB DE HELPDESK"
echo "=========================================================="
echo "Acesse no navegador: http://localhost:5000"
echo "Pressione Ctrl+C para encerrar."
echo "=========================================================="

# Abre o navegador automaticamente no macOS se disponível
if [[ "$OSTYPE" == "darwin"* ]]; then
    (sleep 1.5 && open "http://localhost:5000") &
fi

python3 -m src.app_web
