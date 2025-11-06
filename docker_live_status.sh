#!/bin/bash
# Script para verificar status do container Docker

echo "📊 STATUS DO CONTAINER DOCKER"
echo "=============================="
echo ""

# Verifica se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando!"
    exit 1
fi

# Verifica se o container existe
if docker ps -a | grep -q lofi-live-bot; then
    echo "📋 Status do container:"
    docker ps -a | grep lofi-live-bot
    echo ""
    
    if docker ps | grep -q lofi-live-bot; then
        echo "✅ Container está RODANDO"
        echo ""
        echo "📋 Últimas linhas do log:"
        docker logs --tail 20 lofi-live-bot
    else
        echo "⚠️  Container está PARADO"
        echo ""
        echo "💡 Para iniciar: ./docker_live_start.sh"
    fi
else
    echo "⚠️  Container não encontrado!"
    echo ""
    echo "💡 Para criar e iniciar: ./docker_live_start.sh"
fi

echo ""

