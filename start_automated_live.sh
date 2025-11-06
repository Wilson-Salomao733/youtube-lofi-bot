#!/bin/bash
# Script para iniciar o bot automatizado de live

echo "🤖 Iniciando Bot Automatizado de Live LOFI"
echo "=========================================="

# Verifica se está usando Docker
if command -v docker &> /dev/null && [ -f "docker-compose.live.yml" ]; then
    echo "🐳 Usando Docker..."
    docker-compose -f docker-compose.live.yml up -d
    echo "✅ Bot iniciado em Docker!"
    echo "📋 Ver logs: docker-compose -f docker-compose.live.yml logs -f"
else
    echo "🐍 Executando diretamente com Python..."
    
    # Verifica se ffmpeg está instalado
    if ! command -v ffmpeg &> /dev/null; then
        echo "❌ ffmpeg não encontrado!"
        echo "💡 Instale: sudo apt-get install ffmpeg"
        exit 1
    fi
    
    # Verifica credenciais
    if [ ! -f "credentials/credentials.json" ]; then
        echo "❌ credentials/credentials.json não encontrado!"
        echo "💡 Configure as credenciais do YouTube API primeiro"
        exit 1
    fi
    
    # Inicia em background
    nohup python3 automated_live_bot.py > automated_live.log 2>&1 &
    PID=$!
    echo $PID > automated_live.pid
    echo "✅ Bot iniciado! PID: $PID"
    echo "📋 Ver logs: tail -f automated_live.log"
    echo "🛑 Parar bot: kill $PID"
fi

echo ""
echo "📅 Bot agendado para:"
echo "   🕐 07:00 - Criar vídeo e iniciar live"
echo "   🕐 18:00 - Encerrar live"
echo ""
echo "✅ Tudo automático, zero intervenção manual!"

