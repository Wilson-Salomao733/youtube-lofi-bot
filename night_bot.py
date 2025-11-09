"""
Bot Automatizado para Criar Vídeo Noturno e Live Diariamente
Cria vídeo às 20h e inicia live até 3h da manhã com loop infinito
Sons da Natureza: Chuva, Fogueira, Fazenda, Praia, Som de pessoas
"""
import os
import sys
import time
import schedule
import threading
from datetime import datetime, timedelta
from video_creator import VideoCreator
from live_manager import LiveManager
import signal
import logging

# Configura logging
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'night_bot.log')

if os.path.exists(log_file) and os.path.isdir(log_file):
    import shutil
    shutil.rmtree(log_file)

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


class NightBot:
    """Bot que automatiza criação de vídeo noturno e live diariamente"""
    
    def __init__(self):
        self.video_creator = VideoCreator()
        self.live_manager = LiveManager()
        self.live_manager.logger = logger
        self.current_video_path = None
        self.workflow_running = False
        self.workflow_lock = threading.Lock()  # Lock thread-safe
        self.setup_signal_handlers()
    
    def setup_signal_handlers(self):
        """Configura handlers para parar streaming graciosamente"""
        def signal_handler(sig, frame):
            logger.info("Recebido sinal de interrupção, parando streaming...")
            self.live_manager.stop_streaming()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def create_daily_video(self):
        """Cria vídeo noturno de 30 segundos às 20h"""
        logger.info("🌙 Iniciando criação de vídeo noturno diário...")
        
        try:
            output_folder = "output"
            os.makedirs(output_folder, exist_ok=True)
            
            video_path = self.video_creator.create_night_video(
                video_duration=30,
                images_dir="imagens noite",
                audios_dir="audio_noite"
            )
            logger.info(f"✅ Vídeo noturno criado: {video_path}")
            
            self.current_video_path = video_path
            return video_path
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar vídeo noturno: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def create_live_and_start_streaming(self, video_path):
        """Cria live no YouTube e inicia transmissão automática"""
        logger.info("📺 Criando live noturna no YouTube...")
        
        try:
            now = datetime.now()
            
            # Tenta extrair categoria do nome do arquivo
            category_name = "Sons da Natureza"
            if video_path:
                filename = os.path.basename(video_path)
                if "chuva" in filename.lower():
                    category_name = "Chuva Relaxante"
                elif "fogueira" in filename.lower():
                    category_name = "Fogueira Aconchegante"
                elif "fazenda" in filename.lower():
                    category_name = "Sons da Fazenda"
                elif "praia" in filename.lower():
                    category_name = "Ondas do Mar"
                elif "pessoas" in filename.lower():
                    category_name = "Ambiente Tranquilo"
            
            title = f"Sons da Natureza para Dormir e Relaxar 🌙 {category_name} - {now.strftime('%d/%m/%Y')}"
            
            description = """
🌙 Sons da Natureza para Dormir e Relaxar

Perfeito para:
• Dormir profundamente 😴
• Relaxar e meditar 🧘
• Reduzir ansiedade e estresse 🌿
• Estudar com foco tranquilo 📚
• Trabalhar em paz 💼
• Praticar yoga e mindfulness 🧘‍♀️

Esta transmissão ao vivo apresenta sons naturais relaxantes e visuais calmos.

🎨 Todos os visuais e sons são gerados programaticamente.
Sem problemas de direitos autorais - sinta-se livre para usar este conteúdo.

👉 Inscreva-se para mais sons da natureza!
🔔 Ative as notificações para novos vídeos

Tags: #sonsdanatureza #chuva #relaxar #dormir #meditação #natureza #sleep #relax #asmr #peaceful #calm #sleepsounds #rainsounds
"""
            
            broadcast_id, stream_id, stream_key, rtmp_url = self.live_manager.create_live(
                title=title,
                description=description,
                scheduled_minutes=0,  # 0 = sem agendamento, início imediato
                privacy_status="public"
            )
            
            if not broadcast_id:
                logger.error("❌ Falha ao criar live")
                return False
            
            if not stream_key or not rtmp_url:
                logger.error("❌ Stream Key ou RTMP URL não disponíveis")
                return False
            
            # Inicia streaming IMEDIATAMENTE
            logger.info("📡 Iniciando streaming IMEDIATAMENTE...")
            
            if self.live_manager.start_streaming(video_path, stream_key, rtmp_url):
                logger.info("✅ Streaming iniciado!")
                
                # Tenta publicar após aguardar
                self.live_manager.publish_live(broadcast_id)
                
                return True
            else:
                logger.error("❌ Falha ao iniciar streaming")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao criar live: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def check_and_stop_at_3am(self):
        """Verifica se é 3h da manhã e para a live"""
        now = datetime.now()
        if now.hour == 3 and now.minute == 0:
            logger.info("🕐 É 3h da manhã, encerrando live...")
            self.live_manager.stop_streaming()
            return True
        return False
    
    def nightly_workflow(self):
        """Fluxo noturno completo: criar vídeo e iniciar live"""
        # Usa lock para evitar execuções simultâneas
        if not self.workflow_lock.acquire(blocking=False):
            logger.warning("⚠️  Workflow já em execução, ignorando...")
            return
        
            self.workflow_running = True
            
            # Log de início com timestamp
            logger.info(f"🕐 Iniciando workflow às {datetime.now().strftime('%H:%M:%S')}")
            logger.info("=" * 60)
            logger.info("🌙 Iniciando fluxo noturno - 20h da noite")
            logger.info("=" * 60)
            
            # Cria vídeo
            video_path = self.create_daily_video()
            if not video_path:
                logger.error("❌ Falha ao criar vídeo")
                return
            
            # Cria live e inicia streaming
            if self.create_live_and_start_streaming(video_path):
                logger.info("✅ Live noturna iniciada com sucesso!")
                logger.info("🔄 Monitorando até 3h da manhã...")
                
                retry_count = 0
                max_retries = 3
                
                while True:
                    time.sleep(60)  # Verifica a cada minuto
                    
                    # Verifica se é 3h para parar
                    if self.check_and_stop_at_3am():
                        logger.info("✅ Live encerrada às 3h da manhã conforme agendado")
                        break
                    
                    # Verifica se streaming ainda está ativo
                    if not self.live_manager.is_streaming_active():
                        if retry_count < max_retries:
                            retry_count += 1
                            logger.warning(f"⚠️  Streaming parou! Tentando reiniciar ({retry_count}/{max_retries})...")
                            time.sleep(10)
                            
                            if (self.live_manager.current_stream_key and 
                                self.live_manager.current_rtmp_url and 
                                self.current_video_path):
                                if self.live_manager.start_streaming(
                                    self.current_video_path,
                                    self.live_manager.current_stream_key,
                                    self.live_manager.current_rtmp_url
                                ):
                                    retry_count = 0
                                    logger.info("✅ Streaming reiniciado com sucesso!")
                                else:
                                    logger.error(f"❌ Falha ao reiniciar streaming (tentativa {retry_count})")
                            else:
                                logger.error("❌ Informações de streaming não disponíveis para reiniciar")
                                break
                        else:
                            logger.error("❌ Máximo de tentativas atingido. Encerrando live.")
                            break
                    
                    # Log de status a cada hora
                    now = datetime.now()
                    if now.minute == 0:
                        logger.info(f"📊 Live noturna ativa - {now.strftime('%H:%M')} - Até 3h da manhã")
            else:
                logger.error("❌ Falha ao iniciar live")
                
        except Exception as e:
            logger.error(f"❌ Erro no workflow noturno: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.workflow_running = False
            self.workflow_lock.release()  # Libera o lock
    
    def run(self, execute_now=False):
        """Inicia o bot e agenda tarefas"""
        logger.info("🌙 Bot Automatizado de Live Noturna (Sons da Natureza) iniciado")
        logger.info("📅 Agendado para criar vídeo e live todo dia às 20h")
        logger.info("⏰ Live ficará no ar até 3h da manhã")
        
        # Verifica se deve executar agora baseado no horário
        current_hour = datetime.now().hour
        
        # Se NÃO estiver entre 7h e 19h, executa o fluxo da noite
        # (ou seja, se for antes das 7h ou depois das 19h)
        should_execute_now = execute_now or (current_hour < 7 or current_hour >= 19)
        
        if should_execute_now:
            logger.info(f"🚀 Horário atual: {current_hour}h - Executando workflow da NOITE agora...")
            # Executa em thread para não bloquear o agendamento
            workflow_thread = threading.Thread(target=self.nightly_workflow, daemon=True)
            workflow_thread.start()
            logger.info("✅ Workflow da noite iniciado em background")
        else:
            logger.info(f"⏰ Horário atual: {current_hour}h - Dentro do horário da manhã (7h-19h)")
            logger.info("💤 Aguardando próximo horário agendado...")
        
        # SEMPRE agenda criação diária às 20h
        schedule.every().day.at("20:00").do(
            lambda: threading.Thread(target=self.nightly_workflow, daemon=True).start()
        )
        
        # Loop principal - SEMPRE roda para manter o agendamento ativo
        logger.info("🔄 Bot rodando... (Ctrl+C para parar)")
        logger.info("⏰ Próxima execução agendada: Hoje às 20:00 (ou amanhã se já passou)")
        logger.info("⏱️  Verificando horário a cada 1 minuto")
        
        # Verifica a cada minuto para ser mais preciso
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Verifica a cada 1 minuto (mais preciso)
            except Exception as e:
                logger.error(f"❌ Erro no loop do bot: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(60)  # Continua mesmo com erro


if __name__ == "__main__":
    import os
    try:
        bot = NightBot()
        execute_now = os.getenv('EXECUTE_NOW', 'false').lower() == 'true'
        bot.run(execute_now=execute_now)
    except KeyboardInterrupt:
        logger.info("\n⚠️  Bot interrompido pelo usuário")
        if bot:
            bot.live_manager.stop_streaming()
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

