#!/bin/bash
# Script para iniciar o container Docker - TUDO roda dentro do container, nada na máquina

echo "🐳 INICIANDO CONTAINER DOCKER"
echo "=============================="
echo "TUDO roda dentro do container, NADA na sua máquina!"
echo ""

# Para qualquer processo Python rodando na máquina
echo "🛑 Parando processos Python na máquina (se houver)..."
pkill -f "run_workflow_now.py" 2>/dev/null && echo "   ✅ run_workflow_now.py parado" || true
pkill -f "automated_live_bot.py" 2>/dev/null && echo "   ✅ automated_live_bot.py parado" || true
pkill -f "automated_youtube_bot.py" 2>/dev/null && echo "   ✅ automated_youtube_bot.py parado" || true
sleep 1

# Verifica se Docker está rodando
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker não está rodando!"
    echo "💡 Inicie o Docker primeiro"
    exit 1
fi

# Verifica se está no diretório correto
if [ ! -f "docker-compose.live.yml" ]; then
    echo "❌ Execute este script no diretório do projeto!"
    exit 1
fi

# Verifica credenciais
if [ ! -f "credentials/credentials.json" ]; then
    echo "❌ credentials/credentials.json não encontrado!"
    echo "💡 Configure as credenciais do YouTube API primeiro"
    exit 1
fi

echo "📋 Configuração:"
echo "   • Container: lofi-live-bot"
echo "   • TUDO roda dentro do container"
echo "   • NADA roda na sua máquina"
echo "   • Verifica horário: A cada 1 hora"
echo "   • Execução: Todo dia às 07:00"
echo "   • Live encerra: Todo dia às 19:00"
echo ""

# Para container antigo se existir
if docker ps -a | grep -q lofi-live-bot; then
    echo "🛑 Parando container antigo..."
    docker compose -f docker-compose.live.yml down 2>/dev/null || true
    sleep 2
fi

# Constrói e inicia o container
echo "🔨 Construindo imagem Docker (pode demorar na primeira vez)..."
docker compose -f docker-compose.live.yml build

if [ $? -ne 0 ]; then
    echo "❌ Erro ao construir imagem!"
    exit 1
fi

echo ""
echo "🚀 Iniciando container..."
docker compose -f docker-compose.live.yml up -d

if [ $? -ne 0 ]; then
    echo "❌ Erro ao iniciar container!"
    exit 1
fi

echo ""
echo "✅ Container iniciado com sucesso!"
echo ""
echo "📋 Comandos úteis:"
echo "   • Ver logs: docker logs -f lofi-live-bot"
echo "   • Parar: ./docker_live_stop.sh"
echo "   • Status: ./docker_live_status.sh"
echo ""
echo "⏰ Próxima execução: Amanhã às 07:00"
echo "🔄 Container verifica horário a cada 1 hora"
echo ""
echo "✅ TUDO está rodando dentro do Docker, nada na sua máquina!"
echo ""
