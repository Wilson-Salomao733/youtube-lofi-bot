#!/bin/bash
# Script para executar workflow completo AGORA mesmo

echo "🚀 EXECUTANDO WORKFLOW COMPLETO AGORA"
echo "======================================"
echo ""

# Verifica se está no diretório correto
if [ ! -f "automated_live_bot.py" ]; then
    echo "❌ Execute este script no diretório do projeto!"
    exit 1
fi

# Verifica credenciais
if [ ! -f "credentials/credentials.json" ]; then
    echo "❌ credentials/credentials.json não encontrado!"
    echo "💡 Configure as credenciais do YouTube API primeiro"
    exit 1
fi

# Verifica ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ ffmpeg não encontrado!"
    echo "💡 Instale: sudo apt-get install ffmpeg"
    exit 1
fi

echo "📹 Criando vídeo e iniciando live AGORA..."
echo ""

# Executa o workflow
python3 run_workflow_now.py

echo ""
echo "✅ Workflow executado!"
echo "📋 Ver logs: tail -f automated_live.log"

