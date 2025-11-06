#!/bin/bash

# Script para fazer push do projeto para o GitHub

echo "🚀 Preparando para fazer push para o GitHub..."
echo ""

# Verifica se já existe um remote
if git remote get-url origin 2>/dev/null; then
    echo "✅ Remote 'origin' já configurado:"
    git remote -v
    echo ""
    echo "📤 Fazendo push..."
    git push -u origin main
else
    echo "❌ Nenhum remote configurado ainda."
    echo ""
    echo "Para conectar ao GitHub, você precisa:"
    echo ""
    echo "1. Criar um novo repositório no GitHub:"
    echo "   - Acesse: https://github.com/new"
    echo "   - Nome sugerido: youtube-lofi-bot"
    echo "   - NÃO inicialize com README, .gitignore ou license"
    echo ""
    echo "2. Depois execute um destes comandos (substitua SEU_USUARIO):"
    echo ""
    echo "   git remote add origin https://github.com/SEU_USUARIO/youtube-lofi-bot.git"
    echo "   git push -u origin main"
    echo ""
    echo "   OU se preferir SSH:"
    echo ""
    echo "   git remote add origin git@github.com:SEU_USUARIO/youtube-lofi-bot.git"
    echo "   git push -u origin main"
    echo ""
    read -p "Digite seu nome de usuário do GitHub (ou pressione Enter para pular): " github_user
    
    if [ ! -z "$github_user" ]; then
        echo ""
        read -p "Nome do repositório (padrão: youtube-lofi-bot): " repo_name
        repo_name=${repo_name:-youtube-lofi-bot}
        
        echo ""
        read -p "Usar SSH? (s/N): " use_ssh
        
        if [[ "$use_ssh" =~ ^[Ss]$ ]]; then
            remote_url="git@github.com:${github_user}/${repo_name}.git"
        else
            remote_url="https://github.com/${github_user}/${repo_name}.git"
        fi
        
        echo ""
        echo "🔗 Adicionando remote: $remote_url"
        git remote add origin "$remote_url"
        
        echo ""
        echo "📤 Fazendo push..."
        git push -u origin main
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "✅ Push realizado com sucesso!"
            echo "🌐 Acesse: https://github.com/${github_user}/${repo_name}"
        else
            echo ""
            echo "❌ Erro ao fazer push. Verifique:"
            echo "   - Se o repositório foi criado no GitHub"
            echo "   - Se você tem permissão para fazer push"
            echo "   - Se suas credenciais estão configuradas"
        fi
    else
        echo ""
        echo "⚠️  Pulando configuração. Configure manualmente quando quiser."
    fi
fi

