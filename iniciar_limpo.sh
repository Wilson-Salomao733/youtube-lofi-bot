#!/bin/bash
# Script para parar tudo na máquina e iniciar apenas no Docker

set -e

cd /home/wilsonsalomo/Documentos/YOUTUBE

echo "=========================================="
echo "🧹 LIMPANDO TUDO E INICIANDO NO DOCKER"
echo "=========================================="
echo ""

# 1. Para todos os processos Python relacionados aos bots
echo "1️⃣ Parando processos Python na máquina..."
pkill -f "python.*morning_bot\|python.*night_bot\|python.*main.py" 2>/dev/null || true
sleep 2
echo "   ✅ Processos Python parados"
echo ""

# 2. Para containers Docker existentes
echo "2️⃣ Parando containers Docker..."
docker compose down 2>/dev/null || true
docker stop youtube-live-bots 2>/dev/null || true
docker rm youtube-live-bots 2>/dev/null || true
sleep 2
echo "   ✅ Containers Docker parados"
echo ""

# 3. Reconstrói a imagem (se necessário)
echo "3️⃣ Verificando imagem Docker..."
docker compose build --quiet 2>/dev/null || docker compose build
echo "   ✅ Imagem Docker pronta"
echo ""

# 4. Inicia os bots no Docker
echo "4️⃣ Iniciando bots no Docker..."
echo ""
echo "💡 Os bots vão:"
echo "   - Detectar o horário atual automaticamente"
echo "   - Se for entre 7h-19h: executar fluxo da MANHÃ"
echo "   - Se for fora desse horário: executar fluxo da NOITE"
echo "   - Continuar agendados para os próximos horários"
echo ""

docker compose up -d

echo ""
echo "✅ Bots iniciados no Docker!"
echo ""
echo "📋 Comandos úteis:"
echo "   Ver logs: docker compose logs -f"
echo "   Parar: docker compose down"
echo "   Status: docker compose ps"
echo ""
echo "=========================================="
echo "✅ TUDO PRONTO! Tudo rodando no Docker!"
echo "=========================================="
echo ""
echo "💡 Agora TUDO roda no Docker, nada na sua máquina!"
echo ""

