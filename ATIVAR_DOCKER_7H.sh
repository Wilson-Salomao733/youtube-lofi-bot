#!/bin/bash
# Script para atualizar e ativar o Docker para rodar às 7h

echo "🐳 ATUALIZANDO E ATIVANDO DOCKER PARA 7H"
echo "=========================================="
echo ""

# Verifica se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando!"
    echo "💡 Inicie o Docker primeiro"
    exit 1
fi

echo "1️⃣  Parando container antigo (se existir)..."
docker compose -f docker-compose.live.yml down 2>/dev/null || true

echo ""
echo "2️⃣  Reconstruindo imagem com as novas alterações..."
docker compose -f docker-compose.live.yml build --no-cache

if [ $? -ne 0 ]; then
    echo "❌ Erro ao construir imagem!"
    exit 1
fi

echo ""
echo "3️⃣  Subindo container..."
docker compose -f docker-compose.live.yml up -d

if [ $? -ne 0 ]; then
    echo "❌ Erro ao subir container!"
    exit 1
fi

echo ""
echo "4️⃣  Verificando status..."
sleep 2
docker ps | grep lofi-live-bot || echo "⚠️  Container não encontrado"

echo ""
echo "5️⃣  Verificando logs..."
echo "   (Aguardando 5 segundos para ver inicialização...)"
sleep 5
docker logs --tail 20 lofi-live-bot

echo ""
echo "=========================================="
echo "✅ DOCKER ATIVADO E RODANDO!"
echo "=========================================="
echo ""
echo "📋 Próximos passos:"
echo "   • Container vai rodar 24/7"
echo "   • Todo dia às 7h cria vídeo e inicia live"
echo "   • Live fica no ar até 19h (7 da noite)"
echo ""
echo "🔍 Comandos úteis:"
echo "   • Ver logs: docker logs -f lofi-live-bot"
echo "   • Parar: docker compose -f docker-compose.live.yml down"
echo "   • Reiniciar: docker compose -f docker-compose.live.yml restart"
echo ""
echo "⏰ Próxima execução: Amanhã às 07:00"
echo ""

