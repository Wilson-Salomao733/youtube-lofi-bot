#!/bin/bash
# Script para iniciar o bot noturno manualmente

echo "🌙 Iniciando Bot Noturno (Sons da Natureza)"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# Verifica se as pastas existem
if [ ! -d "imagens noite" ]; then
    echo "❌ Pasta 'imagens noite' não encontrada!"
    exit 1
fi

if [ ! -d "audio_noite" ]; then
    echo "❌ Pasta 'audio_noite' não encontrada!"
    exit 1
fi

echo "✅ Pastas encontradas"
echo ""

# Executa o bot
echo "🚀 Iniciando bot..."
python3 automated_night_bot.py

