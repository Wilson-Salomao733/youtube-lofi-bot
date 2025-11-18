#!/bin/bash
# Script para limpar arquivos desnecessários do projeto

cd /home/wilsonsalomo/Documentos/YOUTUBE

echo "🧹 Limpando projeto..."

# Arquivos de teste antigos
echo "Removendo arquivos de teste antigos..."
rm -f testar_fluxo.py
rm -f testar_fluxo_automatico.py
rm -f testar_streaming_rapido.py
rm -f testar_streaming_rapido_v2.py
rm -f test_fluxo_completo.py

# Scripts duplicados/antigos
echo "Removendo scripts duplicados..."
rm -f rodar_docker_agora.sh
rm -f executar_agora_docker.sh
rm -f testar_docker_agora.sh
rm -f testar_docker.sh
rm -f iniciar_bots_automatico.sh

# Documentação duplicada/antiga
echo "Removendo documentação duplicada..."
rm -f ESTRUTURA_NOVA.md
rm -f RESUMO_AUTOMACAO.md
rm -f RESUMO_CORRECOES.md
rm -f EXECUTAR_DOCKER_AGORA.md
rm -f DOCKER_SETUP.md
rm -f INSTALAR_DEPENDENCIAS.md
rm -f COMANDO_DOCKER.txt
rm -f RODAR_DOCKER.txt

# Arquivos temporários
echo "Removendo arquivos temporários..."
rm -f docker_execution.log
rm -f cleanup_old_files.py

# Limpar __pycache__
echo "Limpando __pycache__..."
find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true

echo "✅ Limpeza concluída!"


