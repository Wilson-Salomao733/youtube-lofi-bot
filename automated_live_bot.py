"""
Bot Automatizado para Criar Vídeo e Live Diariamente
Cria vídeo às 7h e inicia live até 18h com loop infinito
"""
import os
import sys
import time
import schedule
import subprocess
import threading
from datetime import datetime, timedelta
from create_lofi_video import create_lofi_video
from youtube_uploader import YouTubeUploader
import signal
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


class AutomatedLiveBot:
    """Bot que automatiza criação de vídeo e live diariamente"""
    
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
        """Cria vídeo de 30 segundos às 7h"""
        logger.info("🎬 Iniciando criação de vídeo diário...")
        
        try:
            # Garante que a pasta output existe
            output_folder = "output"
            os.makedirs(output_folder, exist_ok=True)
            
            # Cria vídeo de 30 segundos (já salva na pasta output/)
            video_path = create_lofi_video(video_duration=30, images_dir="images", audios_dir="audios")
            logger.info(f"✅ Vídeo criado: {video_path}")
            
            self.current_video_path = video_path
            return video_path
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar vídeo: {e}")
            return None
    
    def create_live_and_start_streaming(self, video_path):
        """Cria live no YouTube e inicia transmissão automática"""
        logger.info("📺 Criando live no YouTube...")
        
        try:
            if not self.uploader:
                self.uploader = YouTubeUploader()
            
            # Calcula horário de término (18h do mesmo dia)
            now = datetime.now()
            end_time = now.replace(hour=18, minute=0, second=0, microsecond=0)
            if end_time <= now:
                # Se já passou das 18h, agenda para 18h do dia seguinte
                end_time += timedelta(days=1)
            
            # Título com data
            title = f"Músicas para Trabalhar e Estudar Concentrado LOFI 🎵 - {now.strftime('%d/%m/%Y')}"
            
            description = f"""
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
            
            # Agenda para começar (YouTube requer pelo menos 10 minutos no futuro)
            # IMPORTANTE: Calcular o horário DEPOIS que o vídeo é criado
            # e usar UTC + margem de segurança de 20 minutos (vídeo demora ~13min)
            from datetime import timezone
            now_utc = datetime.now(timezone.utc)
            scheduled_time = now_utc + timedelta(minutes=20)
            
            logger.info(f"⏰ Agora (UTC): {now_utc}")
            logger.info(f"⏰ Agendando live para: {scheduled_time} (UTC)")
            logger.info(f"⏰ Diferença: {(scheduled_time - now_utc).total_seconds() / 60:.1f} minutos")
            
            broadcast_id, stream_id, stream_key, rtmp_url = self.uploader.create_live_broadcast(
                title=title,
                scheduled_start_time=scheduled_time,
                description=description,
                privacy_status="public",
                use_permanent_stream=True  # ♻️ Usa o mesmo stream_key para todas as lives
            )
            
            if not broadcast_id:
                logger.error("❌ Falha ao criar live")
                logger.error("💡 Verifique os logs acima para detalhes do erro")
                logger.error("💡 Possíveis causas:")
                logger.error("   - Canal não habilitado para live streaming")
                logger.error("   - Credenciais inválidas ou expiradas")
                logger.error("   - Horário agendado muito próximo (precisa ser 10+ minutos)")
                return False
            
            self.current_broadcast_id = broadcast_id
            self.current_stream_key = stream_key
            self.current_rtmp_url = rtmp_url
            
            logger.info(f"✅ Live criada: {broadcast_id}")
            logger.info(f"🔗 Link: https://www.youtube.com/watch?v={broadcast_id}")
            logger.info(f"🔑 Stream Key: {'✅ Disponível' if stream_key else '❌ Não disponível'}")
            logger.info(f"📍 RTMP URL: {'✅ Disponível' if rtmp_url else '❌ Não disponível'}")
            
            if not stream_key or not rtmp_url:
                logger.error("❌ Stream Key ou RTMP URL não disponíveis após múltiplas tentativas automáticas")
                logger.error("💡 O YouTube pode levar alguns minutos para disponibilizar o stream_key")
                logger.error(f"💡 Você pode obter manualmente em: https://studio.youtube.com/video/{broadcast_id}/edit")
                return False
            
            # Aguarda alguns segundos antes de iniciar streaming
            logger.info("⏳ Aguardando 30 segundos antes de iniciar streaming...")
            time.sleep(30)
            
            # Inicia streaming
            return self.start_streaming(video_path, stream_key, rtmp_url)
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar live: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def start_streaming(self, video_path, stream_key, rtmp_url):
        """Inicia transmissão do vídeo em loop usando ffmpeg"""
        logger.info("📡 Iniciando transmissão com ffmpeg...")
        
        if not stream_key or not rtmp_url:
            logger.error("❌ Stream Key ou RTMP URL não disponíveis")
            # Tenta obter do YouTube Studio
            logger.info("💡 Tente obter manualmente do YouTube Studio")
            return False
        
        try:
            # URL completa do RTMP
            rtmp_full_url = f"{rtmp_url}/{stream_key}"
            
            logger.info(f"📍 RTMP URL: {rtmp_url}")
            logger.info(f"🔑 Stream Key: {stream_key[:10]}...")
            
            # Comando ffmpeg para transmitir vídeo em loop
            # -stream_loop -1 = loop infinito
            # -re = ler em tempo real (mantém velocidade correta)
            # -c copy = copiar codecs sem re-encodar (mais eficiente)
            
            ffmpeg_cmd = [
                'ffmpeg',
                '-re',  # Lê em tempo real
                '-stream_loop', '-1',  # Loop infinito
                '-i', video_path,  # Input vídeo
                '-c:v', 'libx264',  # Codec de vídeo
                '-preset', 'veryfast',  # Preset rápido
                '-maxrate', '4000k',  # Bitrate máximo
                '-bufsize', '8000k',  # Buffer size
                '-c:a', 'aac',  # Codec de áudio
                '-b:a', '128k',  # Bitrate de áudio
                '-f', 'flv',  # Formato de saída (FLV para RTMP)
                '-flvflags', 'no_duration_filesize',
                rtmp_full_url
            ]
            
            logger.info("🎥 Iniciando ffmpeg...")
            logger.info(f"📝 Comando: {' '.join(ffmpeg_cmd[:5])}... [video em loop]")
            
            # Inicia processo ffmpeg
            self.ffmpeg_process = subprocess.Popen(
                ffmpeg_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Aguarda um pouco para verificar se iniciou corretamente
            time.sleep(5)
            
            if self.ffmpeg_process.poll() is not None:
                # Processo terminou (erro)
                stdout, stderr = self.ffmpeg_process.communicate()
                logger.error(f"❌ Erro ao iniciar ffmpeg: {stderr}")
                return False
            
            logger.info("✅ Streaming iniciado com sucesso!")
            logger.info(f"🔄 Vídeo rodando em loop infinito")
            logger.info(f"⏰ Live ficará no ar até 19h (7 da noite)")
            
            return True
            
        except FileNotFoundError:
            logger.error("❌ ffmpeg não encontrado!")
            logger.info("💡 Instale ffmpeg:")
            logger.info("   sudo apt-get install ffmpeg  # Linux")
            logger.info("   brew install ffmpeg           # macOS")
            return False
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar streaming: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def stop_streaming(self):
        """Para o streaming graciosamente"""
        if self.ffmpeg_process:
            logger.info("🛑 Parando streaming...")
            try:
                self.ffmpeg_process.terminate()
                # Aguarda até 10 segundos para terminar
                try:
                    self.ffmpeg_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    logger.warning("⚠️  Forçando encerramento do ffmpeg...")
                    self.ffmpeg_process.kill()
                
                logger.info("✅ Streaming parado")
            except Exception as e:
                logger.error(f"❌ Erro ao parar streaming: {e}")
    
    def check_and_stop_at_19h(self):
        """Verifica se é 19h (7 da noite) e para o streaming"""
        now = datetime.now()
        # Para entre 19:00 e 19:05 (para garantir que para mesmo)
        if now.hour == 19 and now.minute < 5:
            logger.info("🕐 19h (7 da noite) - Parando live diária...")
            self.stop_streaming()
            return True
        return False
    
    def is_streaming_active(self):
        """Verifica se o streaming está ativo"""
        if not self.ffmpeg_process:
            return False
        return self.ffmpeg_process.poll() is None
    
    def daily_workflow(self):
        """Fluxo diário completo: criar vídeo e iniciar live"""
        # Evita múltiplas execuções simultâneas
        if self.workflow_running:
            logger.warning("⚠️  Workflow já em execução, ignorando...")
            return
        
        self.workflow_running = True
        
        try:
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
                logger.info("🔄 Monitorando até 19h (7 da noite)...")
                
                # Monitora até 19h
                retry_count = 0
                max_retries = 3
                
                while True:
                    time.sleep(60)  # Verifica a cada minuto
                    
                    # Verifica se é 19h para parar
                    if self.check_and_stop_at_19h():
                        logger.info("✅ Live encerrada às 19h (7 da noite) conforme agendado")
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
                        logger.info(f"📊 Live ativa - {datetime.now().strftime('%H:%M')} - Até 19h")
            else:
                logger.error("❌ Falha ao iniciar live")
        except Exception as e:
            logger.error(f"❌ Erro no workflow diário: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.workflow_running = False
    
    def run(self, execute_now=False):
        """Inicia o bot e agenda tarefas"""
        logger.info("🤖 Bot Automatizado de Live LOFI iniciado")
        logger.info("📅 Agendado para criar vídeo e live todo dia às 7h")
        logger.info("⏰ Live ficará no ar até 19h (7 da noite)")
        
        # Se execute_now=True, executa workflow imediatamente
        if execute_now:
            logger.info("🚀 Executando workflow AGORA mesmo...")
            workflow_thread = threading.Thread(target=self.daily_workflow, daemon=True)
            workflow_thread.start()
        
        # Agenda criação diária às 7h (horário local - container configurado com TZ=America/Sao_Paulo)
        schedule.every().day.at("07:00").do(lambda: threading.Thread(target=self.daily_workflow, daemon=True).start())
        
        # Loop principal
        logger.info("🔄 Bot rodando... (Ctrl+C para parar)")
        if execute_now:
            logger.info("⏰ Workflow executando agora + agendado para amanhã às 07:00")
        else:
            logger.info("⏰ Próxima execução: Amanhã às 07:00")
        logger.info("⏱️  Verificando horário a cada 1 hora")
        
        while True:
            schedule.run_pending()
            time.sleep(3600)  # Verifica a cada 1 hora (3600 segundos)


if __name__ == "__main__":
    import os
    try:
        bot = AutomatedLiveBot()
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

