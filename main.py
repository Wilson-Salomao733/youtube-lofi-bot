"""
Script principal para executar os bots de live (manhã e noite)
"""
import os
import sys
import time
import threading
import signal
from morning_bot import MorningBot
from night_bot import NightBot
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


class LiveBotManager:
    """Gerencia ambos os bots (manhã e noite)"""
    
    def __init__(self):
        self.morning_bot = None
        self.night_bot = None
        self.setup_signal_handlers()
    
    def setup_signal_handlers(self):
        """Configura handlers para parar bots graciosamente"""
        def signal_handler(sig, frame):
            logger.info("Recebido sinal de interrupção, parando bots...")
            self.stop_all()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def start_morning_bot(self, execute_now=False):
        """Inicia bot da manhã"""
        logger.info("🌅 Iniciando bot da manhã...")
        self.morning_bot = MorningBot()
        # execute_now=False porque o bot detecta automaticamente o horário
        morning_thread = threading.Thread(
            target=self.morning_bot.run,
            args=(False,),  # Bot detecta horário automaticamente
            daemon=True
        )
        morning_thread.start()
        return morning_thread
    
    def start_night_bot(self, execute_now=False):
        """Inicia bot da noite"""
        logger.info("🌙 Iniciando bot da noite...")
        self.night_bot = NightBot()
        # execute_now=False porque o bot detecta automaticamente o horário
        night_thread = threading.Thread(
            target=self.night_bot.run,
            args=(False,),  # Bot detecta horário automaticamente
            daemon=True
        )
        night_thread.start()
        return night_thread
    
    def stop_all(self):
        """Para todos os bots"""
        logger.info("🛑 Parando todos os bots...")
        if self.morning_bot:
            self.morning_bot.live_manager.stop_streaming()
        if self.night_bot:
            self.night_bot.live_manager.stop_streaming()
        logger.info("✅ Todos os bots parados")
    
    def run(self, morning_execute_now=False, night_execute_now=False):
        """Executa ambos os bots"""
        from datetime import datetime
        current_hour = datetime.now().hour
        
        logger.info("=" * 60)
        logger.info("🚀 Iniciando Sistema de Live Bots")
        logger.info("=" * 60)
        logger.info(f"🕐 Horário atual: {current_hour}h")
        logger.info("🌅 Bot da Manhã: 7h - 19h (LOFI)")
        logger.info("🌙 Bot da Noite: 20h - 3h (Sons da Natureza)")
        logger.info("=" * 60)
        logger.info("💡 Os bots detectam automaticamente o horário e executam o fluxo apropriado")
        logger.info("=" * 60)
        
        # Inicia ambos os bots (eles detectam o horário automaticamente)
        morning_thread = self.start_morning_bot(execute_now=False)
        night_thread = self.start_night_bot(execute_now=False)
        
        logger.info("✅ Ambos os bots iniciados")
        logger.info("🔄 Sistema rodando... (Ctrl+C para parar)")
        
        # Mantém o processo vivo
        try:
            while True:
                time.sleep(3600)  # Verifica a cada hora
        except KeyboardInterrupt:
            logger.info("\n⚠️  Sistema interrompido pelo usuário")
            self.stop_all()
            sys.exit(0)


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Sistema de Live Bots para YouTube")
    parser.add_argument(
        '--morning-now',
        action='store_true',
        help='Executa workflow da manhã imediatamente'
    )
    parser.add_argument(
        '--night-now',
        action='store_true',
        help='Executa workflow da noite imediatamente'
    )
    parser.add_argument(
        '--morning-only',
        action='store_true',
        help='Executa apenas o bot da manhã'
    )
    parser.add_argument(
        '--night-only',
        action='store_true',
        help='Executa apenas o bot da noite'
    )
    
    args = parser.parse_args()
    
    manager = LiveBotManager()
    
    try:
        if args.morning_only:
            logger.info("🌅 Executando apenas bot da manhã...")
            manager.start_morning_bot(execute_now=args.morning_now)
            while True:
                time.sleep(3600)
        elif args.night_only:
            logger.info("🌙 Executando apenas bot da noite...")
            manager.start_night_bot(execute_now=args.night_now)
            while True:
                time.sleep(3600)
        else:
            # Executa ambos
            manager.run(
                morning_execute_now=args.morning_now,
                night_execute_now=args.night_now
            )
    except KeyboardInterrupt:
        logger.info("\n⚠️  Sistema interrompido pelo usuário")
        manager.stop_all()
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        manager.stop_all()
        sys.exit(1)


if __name__ == "__main__":
    main()

