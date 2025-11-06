#!/bin/bash
# Script para iniciar o bot que roda automaticamente às 7h

echo "🤖 INICIANDO BOT AUTOMATIZADO - 7H DA MANHÃ"
echo "============================================"
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

# Verifica se já está rodando
if [ -f "automated_live.pid" ]; then
    OLD_PID=$(cat automated_live.pid)
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "⚠️  Bot já está rodando (PID: $OLD_PID)"
        echo "💡 Para parar: kill $OLD_PID"
        echo "💡 Para forçar reinício: kill $OLD_PID && ./start_bot_7h.sh"
        exit 1
    else
        echo "🧹 Removendo PID antigo..."
        rm automated_live.pid
    fi
fi

echo "📅 Bot será executado automaticamente:"
echo "   🕐 07:00 - Criar vídeo e iniciar live"
echo "   🕐 19:00 - Encerrar live"
echo ""

# Inicia em background
echo "🚀 Iniciando bot em background..."
nohup python3 automated_live_bot.py > automated_live.log 2>&1 &
PID=$!
echo $PID > automated_live.pid

echo "✅ Bot iniciado! PID: $PID"
echo ""
echo "📋 Comandos úteis:"
echo "   • Ver logs: tail -f automated_live.log"
echo "   • Parar bot: kill $PID"
echo "   • Verificar status: ps -p $PID"
echo ""
echo "⏰ Próxima execução: Amanhã às 07:00"
echo "🔄 Bot rodando 24/7 até você parar manualmente"
echo ""

