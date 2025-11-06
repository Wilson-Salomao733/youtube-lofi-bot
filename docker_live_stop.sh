#!/bin/bash
# Script para parar o container Docker do bot de live

echo "🛑 PARANDO CONTAINER DOCKER - BOT DE LIVE"
echo "========================================="
echo ""

# Verifica se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando!"
    exit 1
fi

# Verifica se o container existe
if ! docker ps -a | grep -q lofi-live-bot; then
    echo "⚠️  Container não encontrado!"
    exit 0
fi

# Para o container
echo "🛑 Parando container..."
docker compose -f docker-compose.live.yml down

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Container parado com sucesso!"
    echo ""
    echo "💡 Para iniciar novamente: ./docker_live_start.sh"
else
    echo "❌ Erro ao parar container!"
    exit 1
fi

