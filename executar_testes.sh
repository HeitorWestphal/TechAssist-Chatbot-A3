#!/usr/bin/env bash
# Script para executar a suite automatizada de testes e metricas (R5 e R6)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

if [ -d "venv" ]; then
    source venv/bin/activate
fi

python3 -m src.evaluate
