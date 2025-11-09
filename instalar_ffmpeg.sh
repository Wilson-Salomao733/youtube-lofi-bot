#!/bin/bash
# Script para instalar ffmpeg automaticamente

echo "=========================================="
echo "📦 Instalando ffmpeg"
echo "=========================================="

# Detecta o sistema operacional
if [ -f /etc/debian_version ]; then
    # Debian/Ubuntu
    echo "🔍 Detectado: Debian/Ubuntu"
    echo "📥 Atualizando pacotes..."
    sudo apt-get update
    echo "📦 Instalando ffmpeg..."
    sudo apt-get install -y ffmpeg
elif [ -f /etc/redhat-release ]; then
    # RedHat/CentOS/Fedora
    echo "🔍 Detectado: RedHat/CentOS/Fedora"
    echo "📦 Instalando ffmpeg..."
    sudo yum install -y ffmpeg || sudo dnf install -y ffmpeg
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "🔍 Detectado: macOS"
    echo "📦 Instalando ffmpeg via Homebrew..."
    brew install ffmpeg
else
    echo "❌ Sistema operacional não suportado automaticamente"
    echo "💡 Instale ffmpeg manualmente:"
    echo "   - Linux: sudo apt-get install ffmpeg"
    echo "   - macOS: brew install ffmpeg"
    exit 1
fi

# Verifica instalação
if command -v ffmpeg &> /dev/null; then
    echo ""
    echo "✅ ffmpeg instalado com sucesso!"
    ffmpeg -version | head -1
    echo ""
    echo "🎉 Agora você pode usar streaming direto via ffmpeg!"
else
    echo ""
    echo "❌ Erro ao instalar ffmpeg"
    exit 1
fi

