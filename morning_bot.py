"""
Bot Automatizado para Criar Vídeo e Live Diariamente (Manhã)
Cria vídeo às 7h e inicia live até 19h com loop infinito
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
log_file = os.path.join(log_dir, 'morning_bot.log')

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


class MorningBot:
    """Bot que automatiza criação de vídeo e live diariamente (manhã)"""
    
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
        """Cria vídeo de 30 segundos às 7h"""
        logger.info("🎬 Iniciando criação de vídeo diário...")
        
        try:
            output_folder = "output"
            os.makedirs(output_folder, exist_ok=True)
            
            video_path = self.video_creator.create_morning_video(
                video_duration=30,
                images_dir="images",
                audios_dir="audios"
            )
            logger.info(f"✅ Vídeo criado: {video_path}")
            
            self.current_video_path = video_path
            return video_path
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar vídeo: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def create_live_and_start_streaming(self, video_path):
        """Cria live no YouTube e inicia transmissão automática"""
        logger.info("📺 Criando live no YouTube...")
        
        try:
            now = datetime.now()
            title = f"Músicas para Trabalhar e Estudar Concentrado LOFI 🎵 - {now.strftime('%d/%m/%Y')}"
            
            description = """
🎵 Músicas LOFI para Trabalhar e Estudar Concentrado

Perfeito para:
• Estudar e focar nos estudos 📚
• Trabalhar com produtividade 💼
• Relaxar e descontrair 🌙
• Meditar e praticar yoga 🧘
• Ler e se concentrar 📖

Esta transmissão ao vivo apresenta beats suaves e visuais relaxantes.

🎨 Todos os visuais e sons são gerados programaticamente.
Sem problemas de direitos autorais - sinta-se livre para usar esta música.

👉 Inscreva-se para mais conteúdo LOFI!
🔔 Ative as notificações para novos vídeos

Tags: #lofi #estudar #música #trabalhar #concentração #chill #beats #hiphop #foco #live #músicaparastudar
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
    
    def check_and_stop_at_19h(self):
        """Verifica se é 19h e para o streaming"""
        now = datetime.now()
        if now.hour == 19 and now.minute < 5:
            logger.info("🕐 19h - Parando live diária...")
            self.live_manager.stop_streaming()
            return True
        return False
    
    def daily_workflow(self):
        """Fluxo diário completo: criar vídeo e iniciar live"""
        # Usa lock para evitar execuções simultâneas
        if not self.workflow_lock.acquire(blocking=False):
            logger.warning("⚠️  Workflow já em execução, ignorando...")
            return
        
            self.workflow_running = True
            
            # Log de início com timestamp
            logger.info(f"🕐 Iniciando workflow às {datetime.now().strftime('%H:%M:%S')}")
            logger.info("=" * 60)
            logger.info("🌅 Iniciando fluxo diário - 7h da manhã")
            logger.info("=" * 60)
            
            # Cria vídeo
            video_path = self.create_daily_video()
            if not video_path:
                logger.error("❌ Falha ao criar vídeo")
                return
            
            # Cria live e inicia streaming
            if self.create_live_and_start_streaming(video_path):
                logger.info("✅ Live iniciada com sucesso!")
                logger.info("🔄 Monitorando streaming...")
                
                # Se executado via EXECUTE_NOW, monitora por tempo limitado (30 minutos para teste)
                # Se executado normalmente, monitora até 19h
                import os
                is_test_mode = os.getenv('EXECUTE_NOW', 'false').lower() == 'true'
                
                if is_test_mode:
                    logger.info("🧪 Modo teste: Monitorando por 30 minutos...")
                    test_duration = 30 * 60  # 30 minutos
                    start_time = time.time()
                    
                    retry_count = 0
                    max_retries = 3
                    
                    while time.time() - start_time < test_duration:
                        time.sleep(60)  # Verifica a cada minuto
                        
                        elapsed = int((time.time() - start_time) / 60)
                        remaining = test_duration / 60 - elapsed
                        logger.info(f"📊 Live ativa - {elapsed} minutos decorridos - {remaining:.0f} minutos restantes")
                        
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
                    
                    logger.info("⏰ Tempo de teste concluído (30 minutos)")
                    self.live_manager.stop_streaming()
                else:
                    logger.info("🔄 Monitorando até 19h...")
                    retry_count = 0
                    max_retries = 3
                    
                    while True:
                        time.sleep(60)  # Verifica a cada minuto
                        
                        # Verifica se é 19h para parar
                        if self.check_and_stop_at_19h():
                            logger.info("✅ Live encerrada às 19h conforme agendado")
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
                            logger.info(f"📊 Live ativa - {now.strftime('%H:%M')} - Até 19h")
            else:
                logger.error("❌ Falha ao iniciar live")
                
        except Exception as e:
            logger.error(f"❌ Erro no workflow diário: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.workflow_running = False
            self.workflow_lock.release()  # Libera o lock
    
    def run(self, execute_now=False):
        """Inicia o bot e agenda tarefas"""
        logger.info("🤖 Bot Automatizado de Live LOFI (Manhã) iniciado")
        logger.info("📅 Agendado para criar vídeo e live todo dia às 7h")
        logger.info("⏰ Live ficará no ar até 19h")
        
        # Verifica se deve executar agora baseado no horário
        current_hour = datetime.now().hour
        
        # Se estiver entre 7h e 19h, executa o fluxo da manhã
        should_execute_now = execute_now or (7 <= current_hour < 19)
        
        if should_execute_now:
            logger.info(f"🚀 Horário atual: {current_hour}h - Executando workflow da MANHÃ agora...")
            # Executa em thread para não bloquear o agendamento
            workflow_thread = threading.Thread(target=self.daily_workflow, daemon=True)
            workflow_thread.start()
            logger.info("✅ Workflow da manhã iniciado em background")
        else:
            logger.info(f"⏰ Horário atual: {current_hour}h - Fora do horário da manhã (7h-19h)")
            logger.info("💤 Aguardando próximo horário agendado...")
        
        # SEMPRE agenda criação diária às 7h
        schedule.every().day.at("07:00").do(
            lambda: threading.Thread(target=self.daily_workflow, daemon=True).start()
        )
        
        # Loop principal - SEMPRE roda para manter o agendamento ativo
        logger.info("🔄 Bot rodando... (Ctrl+C para parar)")
        logger.info("⏰ Próxima execução agendada: Amanhã às 07:00")
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
        bot = MorningBot()
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

