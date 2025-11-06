#!/usr/bin/env python3
"""
Script para executar workflow AGORA dentro do container
"""
import sys
import os
sys.path.insert(0, '/app')

from automated_live_bot import AutomatedLiveBot
import threading

def main():
    """Executa workflow completo agora"""
    print("=" * 60)
    print("🚀 EXECUTANDO WORKFLOW AGORA MESMO")
    print("=" * 60)
    
    bot = AutomatedLiveBot()
    
    # Executa workflow em thread separada
    thread = threading.Thread(target=bot.daily_workflow, daemon=True)
    thread.start()
    
    print("✅ Workflow iniciado em background")
    print("📋 Ver logs: docker logs -f lofi-live-bot")

if __name__ == "__main__":
    main()

