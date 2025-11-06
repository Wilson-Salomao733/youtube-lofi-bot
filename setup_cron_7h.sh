#!/bin/bash
# Script para configurar cron para executar às 7h (alternativa ao bot 24/7)

echo "⏰ CONFIGURANDO CRON PARA 7H DA MANHÃ"
echo "====================================="
echo ""

# Verifica se está no diretório correto
if [ ! -f "run_workflow_now.py" ]; then
    echo "❌ Execute este script no diretório do projeto!"
    exit 1
fi

# Caminho completo do script
SCRIPT_DIR=$(pwd)
PYTHON_PATH=$(which python3)

echo "📋 Configuração:"
echo "   • Horário: Todo dia às 07:00"
echo "   • Script: $SCRIPT_DIR/run_workflow_now.py"
echo "   • Python: $PYTHON_PATH"
echo ""

# Verifica se já existe entrada no cron
if crontab -l 2>/dev/null | grep -q "run_workflow_now.py"; then
    echo "⚠️  Já existe uma entrada no cron para este script!"
    echo ""
    echo "Entrada atual:"
    crontab -l | grep "run_workflow_now.py"
    echo ""
    read -p "Deseja substituir? (s/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "❌ Cancelado"
        exit 0
    fi
    # Remove entrada antiga
    crontab -l 2>/dev/null | grep -v "run_workflow_now.py" | crontab -
fi

# Adiciona nova entrada no cron
CRON_LINE="0 7 * * * cd $SCRIPT_DIR && $PYTHON_PATH run_workflow_now.py >> $SCRIPT_DIR/automated_live.log 2>&1"

(crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -

if [ $? -eq 0 ]; then
    echo "✅ Cron configurado com sucesso!"
    echo ""
    echo "📋 Entrada adicionada:"
    crontab -l | grep "run_workflow_now.py"
    echo ""
    echo "🔍 Verificar cron:"
    echo "   crontab -l"
    echo ""
    echo "📋 Ver logs:"
    echo "   tail -f automated_live.log"
    echo ""
    echo "⏰ Próxima execução: Amanhã às 07:00"
    echo ""
    echo "⚠️  ATENÇÃO:"
    echo "   • O bot 24/7 (start_bot_7h.sh) NÃO é necessário com cron"
    echo "   • Se você tem o bot rodando, pare-o: kill \$(cat automated_live.pid)"
    echo "   • O cron executa o script e ele fica rodando até 19h"
else
    echo "❌ Erro ao configurar cron!"
    exit 1
fi

