#!/usr/bin/env python3
"""
Script para executar o workflow completo AGORA mesmo
Cria vídeo e inicia live imediatamente
"""
import os
import sys
from automated_live_bot import AutomatedLiveBot
import logging

# Configura logging
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'automated_live.log')
# Remove se for diretório (erro anterior)
if os.path.exists(log_file) and os.path.isdir(log_file):
    import shutil
    shutil.rmtree(log_file)
# Garante que é um arquivo
if not os.path.exists(log_file) or os.path.isdir(log_file):
    open(log_file, 'a').close()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Executa workflow completo agora"""
    logger.info("=" * 60)
    logger.info("🚀 EXECUTANDO WORKFLOW AGORA MESMO")
    logger.info("=" * 60)
    
    try:
        bot = AutomatedLiveBot()
        
        # Executa workflow completo
        bot.daily_workflow()
        
    except KeyboardInterrupt:
        logger.info("\n⚠️  Processo interrompido pelo usuário")
        if 'bot' in locals():
            bot.stop_streaming()
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

