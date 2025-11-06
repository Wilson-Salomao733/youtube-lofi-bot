#!/bin/bash
# Para TUDO - processos Python na máquina E container Docker

echo "🛑 PARANDO TUDO"
echo "==============="
echo ""

# Para processos Python na máquina
echo "1️⃣  Parando processos Python na máquina..."
pkill -f "run_workflow_now.py" 2>/dev/null && echo "   ✅ run_workflow_now.py parado" || echo "   ℹ️  run_workflow_now.py não estava rodando"
pkill -f "automated_live_bot.py" 2>/dev/null && echo "   ✅ automated_live_bot.py parado" || echo "   ℹ️  automated_live_bot.py não estava rodando"
pkill -f "automated_youtube_bot.py" 2>/dev/null && echo "   ✅ automated_youtube_bot.py parado" || echo "   ℹ️  automated_youtube_bot.py não estava rodando"

# Para container Docker
echo ""
echo "2️⃣  Parando container Docker..."
if docker ps -a | grep -q lofi-live-bot; then
    docker compose -f docker-compose.live.yml down 2>/dev/null
    echo "   ✅ Container Docker parado"
else
    echo "   ℹ️  Container Docker não estava rodando"
fi

echo ""
echo "✅ TUDO PARADO!"
echo ""
echo "💡 Para iniciar apenas o Docker: ./docker_live_start.sh"
echo ""

