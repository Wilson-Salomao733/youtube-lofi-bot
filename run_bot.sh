#!/bin/bash

# Script para rodar o bot LOFI

echo "🎵 Bot LOFI para YouTube"
echo "========================"
echo ""

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verifica se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker não encontrado!${NC}"
    echo "Instale o Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Verifica se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose não encontrado!${NC}"
    echo "Instale o Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✅ Docker encontrado${NC}"
echo ""

# Menu de opções
echo "Escolha uma opção:"
echo ""
echo "1) Criar um vídeo de teste (1 minuto)"
echo "2) Criar vídeo de 1 hora"
echo "3) Criar múltiplos vídeos (ex: 5 vídeos de 1 hora)"
echo "4) Rodar em modo produção (automatizado)"
echo "5) Parar containers"
echo ""
read -p "Opção [1-5]: " option

case $option in
    1)
        echo "📹 Criando vídeo de teste..."
        docker-compose run --rm lofi-generator python3 create_lofi_video.py --duration 60
        ;;
    2)
        echo "📹 Criando vídeo de 1 hora..."
        docker-compose run --rm lofi-generator python3 create_lofi_video.py --duration 3600
        ;;
    3)
        read -p "Quantos vídeos? " count
        echo "📹 Criando $count vídeos..."
        docker-compose run --rm lofi-generator python3 automated_youtube_bot.py --multiple $count --duration 3600
        ;;
    4)
        echo "🚀 Iniciando modo produção..."
        echo "⚠️  Certifique-se de ter configurado as credenciais do YouTube!"
        read -p "Continuar? [y/N]: " confirm
        if [[ $confirm =~ ^[Yy]$ ]]; then
            docker-compose up -d
            echo "✅ Bot rodando em background!"
            echo "📝 Ver logs: docker-compose logs -f"
        fi
        ;;
    5)
        echo "🛑 Parando containers..."
        docker-compose down
        ;;
    *)
        echo "Opção inválida!"
        exit 1
        ;;
esac

