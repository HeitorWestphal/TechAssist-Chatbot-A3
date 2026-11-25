#!/usr/bin/env bash
# Script para iniciar a Interface CLI no Terminal do TechAssist AI
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

if [ -d "venv" ]; then
    source venv/bin/activate
fi

python3 -m src.cli
