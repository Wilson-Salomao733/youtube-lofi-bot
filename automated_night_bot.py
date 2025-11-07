"""
Bot Automatizado para Criar Vídeo Noturno e Live Diariamente
Cria vídeo às 20h e inicia live até 3h da manhã com loop infinito
Sons da Natureza: Chuva, Fogueira, Fazenda, Praia, Som de pessoas
"""
import os
import sys
import time
import schedule
import subprocess
import threading
from datetime import datetime, timedelta, timezone
from create_night_video import create_night_video
from youtube_uploader import YouTubeUploader
import signal
import logging

# Configura logging
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'automated_night.log')
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


class AutomatedNightBot:
    """Bot que automatiza criação de vídeo noturno e live diariamente"""
    
    def __init__(self):
        self.uploader = None
        self.current_video_path = None
        self.current_broadcast_id = None
        self.current_stream_key = None
        self.current_rtmp_url = None
        self.ffmpeg_process = None
        self.workflow_running = False  # Evita múltiplas execuções simultâneas
        self.setup_signal_handlers()
    
    def setup_signal_handlers(self):
        """Configura handlers para parar streaming graciosamente"""
        def signal_handler(sig, frame):
            logger.info("Recebido sinal de interrupção, parando streaming...")
            self.stop_streaming()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def create_daily_video(self):
        """Cria vídeo noturno de 30 segundos às 20h"""
        logger.info("🌙 Iniciando criação de vídeo noturno diário...")
        
        try:
            # Garante que a pasta output existe
            output_folder = "output"
            os.makedirs(output_folder, exist_ok=True)
            
            # Cria vídeo de 30 segundos (já salva na pasta output/)
            video_path = create_night_video(
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
            if not self.uploader:
                self.uploader = YouTubeUploader()
            
            # Calcula horário de término (3h da manhã do dia seguinte)
            now = datetime.now()
            # Se já passou das 3h, agenda para 3h do dia seguinte
            end_time = now.replace(hour=3, minute=0, second=0, microsecond=0)
            if end_time <= now:
                end_time += timedelta(days=1)
            
            # Título com data e categoria
            category_name = "Sons da Natureza"
            if video_path:
                # Tenta extrair categoria do nome do arquivo
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
            
            description = f"""
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
            
            # Agenda para começar (YouTube requer pelo menos 10 minutos no futuro)
            # IMPORTANTE: Calcular o horário DEPOIS que o vídeo é criado
            # e usar UTC + margem de segurança de 20 minutos (vídeo demora ~13min)
            now_utc = datetime.now(timezone.utc)
            scheduled_time = now_utc + timedelta(minutes=20)
            
            logger.info(f"📅 Agendando live para: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            
            # Cria live no YouTube
            broadcast_id, stream_id, stream_key, rtmp_url = self.uploader.create_live_broadcast(
                title=title,
                scheduled_start_time=scheduled_time,
                description=description,
                privacy_status="public",
                use_permanent_stream=True  # ♻️ Usa o mesmo stream_key para todas as lives
            )
            
            if not broadcast_id or not stream_key or not rtmp_url:
                logger.error("❌ Falha ao criar live ou obter stream_key")
                return False
            
            self.current_broadcast_id = broadcast_id
            self.current_stream_key = stream_key
            self.current_rtmp_url = rtmp_url
            
            logger.info(f"✅ Live criada: {broadcast_id}")
            logger.info(f"🔑 Stream Key: {stream_key[:10]}...")
            logger.info(f"📡 RTMP URL: {rtmp_url}")
            
            # Aguarda alguns segundos antes de iniciar streaming
            logger.info("⏳ Aguardando 15 segundos antes de iniciar streaming...")
            time.sleep(15)
            
            # Inicia streaming
            if self.start_streaming(video_path, stream_key, rtmp_url):
                logger.info("✅ Streaming iniciado!")
                return True
            else:
                logger.error("❌ Falha ao iniciar streaming")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro ao criar live: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def start_streaming(self, video_path, stream_key, rtmp_url):
        """Inicia streaming com ffmpeg em loop infinito"""
        try:
            logger.info("🎥 Iniciando streaming com FFmpeg...")
            
            # Comando ffmpeg para streaming em loop
            # Loop infinito do vídeo
            ffmpeg_cmd = [
                'ffmpeg',
                '-re',  # Lê na velocidade natural
                '-stream_loop', '-1',  # Loop infinito
                '-i', video_path,  # Arquivo de vídeo
                '-c:v', 'libx264',  # Codec de vídeo
                '-preset', 'veryfast',  # Preset rápido
                '-maxrate', '3000k',  # Bitrate máximo
                '-bufsize', '6000k',  # Buffer size
                '-pix_fmt', 'yuv420p',  # Formato de pixel
                '-g', '50',  # GOP size
                '-c:a', 'aac',  # Codec de áudio
                '-b:a', '160k',  # Bitrate de áudio
                '-ar', '44100',  # Sample rate
                '-f', 'flv',  # Formato de saída
                rtmp_url + '/' + stream_key  # URL RTMP completa
            ]
            
            logger.info(f"📡 Conectando a: {rtmp_url}")
            logger.info(f"🔑 Stream Key: {stream_key[:10]}...")
            
            # Inicia processo ffmpeg
            self.ffmpeg_process = subprocess.Popen(
                ffmpeg_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            logger.info("✅ FFmpeg iniciado (PID: {})".format(self.ffmpeg_process.pid))
            
            # Aguarda um pouco para verificar se iniciou corretamente
            time.sleep(5)
            
            if self.ffmpeg_process.poll() is not None:
                # Processo já terminou (erro)
                stderr = self.ffmpeg_process.stderr.read() if self.ffmpeg_process.stderr else "Sem erro disponível"
                logger.error(f"❌ FFmpeg terminou imediatamente. Erro: {stderr}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar streaming: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def stop_streaming(self):
        """Para o streaming e encerra a live"""
        logger.info("🛑 Parando streaming...")
        
        # Para ffmpeg
        if self.ffmpeg_process:
            try:
                self.ffmpeg_process.terminate()
                self.ffmpeg_process.wait(timeout=10)
                logger.info("✅ FFmpeg parado")
            except subprocess.TimeoutExpired:
                logger.warning("⚠️  FFmpeg não parou, forçando...")
                self.ffmpeg_process.kill()
            except Exception as e:
                logger.error(f"❌ Erro ao parar FFmpeg: {e}")
            finally:
                self.ffmpeg_process = None
        
        # Encerra live no YouTube
        if self.current_broadcast_id and self.uploader:
            try:
                self.uploader.end_broadcast(self.current_broadcast_id)
                logger.info("✅ Live encerrada no YouTube")
            except Exception as e:
                logger.error(f"❌ Erro ao encerrar live: {e}")
    
    def check_and_stop_at_3am(self):
        """Verifica se é 3h da manhã e para a live"""
        now = datetime.now()
        # Para às 3h da manhã
        if now.hour == 3 and now.minute == 0:
            logger.info("🕐 É 3h da manhã, encerrando live...")
            self.stop_streaming()
            return True
        return False
    
    def is_streaming_active(self):
        """Verifica se o streaming está ativo"""
        if not self.ffmpeg_process:
            return False
        return self.ffmpeg_process.poll() is None
    
    def nightly_workflow(self):
        """Fluxo noturno completo: criar vídeo e iniciar live"""
        # Evita múltiplas execuções simultâneas
        if self.workflow_running:
            logger.warning("⚠️  Workflow já em execução, ignorando...")
            return
        
        self.workflow_running = True
        
        try:
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
                
                # Monitora até 3h da manhã
                retry_count = 0
                max_retries = 3
                
                while True:
                    time.sleep(60)  # Verifica a cada minuto
                    
                    # Verifica se é 3h para parar
                    if self.check_and_stop_at_3am():
                        logger.info("✅ Live encerrada às 3h da manhã conforme agendado")
                        break
                    
                    # Verifica se ffmpeg ainda está rodando
                    if not self.is_streaming_active():
                        if retry_count < max_retries:
                            retry_count += 1
                            logger.warning(f"⚠️  Streaming parou! Tentando reiniciar ({retry_count}/{max_retries})...")
                            time.sleep(10)  # Aguarda antes de reiniciar
                            
                            if self.current_stream_key and self.current_rtmp_url and self.current_video_path:
                                if self.start_streaming(
                                    self.current_video_path,
                                    self.current_stream_key,
                                    self.current_rtmp_url
                                ):
                                    retry_count = 0  # Reset contador se reiniciou com sucesso
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
                    if datetime.now().minute == 0:
                        logger.info(f"📊 Live noturna ativa - {datetime.now().strftime('%H:%M')} - Até 3h da manhã")
            else:
                logger.error("❌ Falha ao iniciar live")
        except Exception as e:
            logger.error(f"❌ Erro no workflow noturno: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.workflow_running = False
    
    def run(self, execute_now=False):
        """Inicia o bot e agenda tarefas"""
        logger.info("🌙 Bot Automatizado de Live Noturna (Sons da Natureza) iniciado")
        logger.info("📅 Agendado para criar vídeo e live todo dia às 20h")
        logger.info("⏰ Live ficará no ar até 3h da manhã")
        
        # Se execute_now=True, executa workflow imediatamente
        if execute_now:
            logger.info("🚀 Executando workflow AGORA mesmo...")
            workflow_thread = threading.Thread(target=self.nightly_workflow, daemon=True)
            workflow_thread.start()
        
        # Agenda criação diária às 20h (horário local - container configurado com TZ=America/Sao_Paulo)
        schedule.every().day.at("20:00").do(lambda: threading.Thread(target=self.nightly_workflow, daemon=True).start())
        
        # Loop principal
        logger.info("🔄 Bot rodando... (Ctrl+C para parar)")
        if execute_now:
            logger.info("⏰ Workflow executando agora + agendado para amanhã às 20:00")
        else:
            logger.info("⏰ Próxima execução: Hoje às 20:00 (ou amanhã se já passou)")
        logger.info("⏱️  Verificando horário a cada 1 hora")
        
        while True:
            schedule.run_pending()
            time.sleep(3600)  # Verifica a cada 1 hora (3600 segundos)


if __name__ == "__main__":
    import os
    try:
        bot = AutomatedNightBot()
        # Se variável de ambiente EXECUTE_NOW estiver definida, executa workflow imediatamente
        execute_now = os.getenv('EXECUTE_NOW', 'false').lower() == 'true'
        bot.run(execute_now=execute_now)
    except KeyboardInterrupt:
        logger.info("\n⚠️  Bot interrompido pelo usuário")
        if bot:
            bot.stop_streaming()
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

