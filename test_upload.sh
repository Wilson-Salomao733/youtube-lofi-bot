#!/bin/bash

# Script de teste para upload automático

echo "🤖 Teste de Upload Automático"
echo "============================="
echo ""

# Verifica se tem credenciais
if [ ! -f "credentials/credentials.json" ]; then
    echo "❌ Credenciais não encontradas!"
    echo ""
    echo "📝 Configure primeiro:"
    echo "1. Acesse: https://console.cloud.google.com/"
    echo "2. Crie projeto e ative YouTube Data API v3"
    echo "3. Crie credenciais OAuth (aplicativo desktop)"
    echo "4. Baixe para: credentials/credentials.json"
    echo ""
    echo "Ou veja o guia completo:"
    echo "cat AUTOMATION_GUIDE.md"
    exit 1
fi

echo "✅ Credenciais encontradas!"
echo ""
read -p "Deseja criar e fazer upload de um vídeo de teste? [y/N]: " confirm

if [[ $confirm =~ ^[Yy]$ ]]; then
    echo ""
    echo "🎬 Criando vídeo de 1 minuto e fazendo upload..."
    python3 automated_youtube_bot.py --upload --duration 60
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Sucesso! Vídeo publicado no YouTube!"
        echo ""
        echo "Próximos passos:"
        echo "  • Criar vídeo de 1h: python3 automated_youtube_bot.py --upload --duration 3600"
        echo "  • Criar 5 vídeos: python3 automated_youtube_bot.py --upload --multiple 5"
        echo "  • Agendar: python3 automated_youtube_bot.py --upload --schedule '09:00'"
    fi
else
    echo "Cancelado."
fi

