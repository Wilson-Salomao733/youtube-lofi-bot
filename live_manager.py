"""
Módulo centralizado para gerenciamento de lives no YouTube
Gerencia criação, streaming e encerramento de lives
"""
import os
import sys
import time
import subprocess
import logging
from datetime import datetime, timedelta, timezone
from youtube_uploader import YouTubeUploader
from youtube_automation import YouTubeAutomation


class LiveManager:
    """Gerenciador de lives no YouTube"""
    
    def __init__(self):
        self.uploader = None
        self.current_broadcast_id = None
        self.current_stream_key = None
        self.current_rtmp_url = None
        self.ffmpeg_process = None
        self.automation = None  # Referência para automação web
        self.logger = logging.getLogger(__name__)
    
    def initialize_uploader(self, max_retries=3, retry_delay=30):
        """Inicializa o uploader do YouTube com retry"""
        for attempt in range(max_retries):
            try:
                if not self.uploader:
                    self.uploader = YouTubeUploader()
                return True
            except Exception as e:
                error_str = str(e).lower()
                if 'name resolution' in error_str or 'failed to resolve' in error_str or 'no address associated' in error_str:
                    if attempt < max_retries - 1:
                        self.logger.warning(f"⚠️  Erro de rede ao conectar ao YouTube (tentativa {attempt + 1}/{max_retries}): {e}")
                        self.logger.info(f"⏳ Aguardando {retry_delay} segundos antes de tentar novamente...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        self.logger.error(f"❌ Erro de rede após {max_retries} tentativas: {e}")
                        self.logger.error("💡 Verifique sua conexão com a internet e DNS")
                        return False
                else:
                    raise
        
        return False
    
    def create_live(self, title, description, scheduled_minutes=3, privacy_status="public"):
        """
        Cria uma live no YouTube
        
        Args:
            title: Título da live
            description: Descrição da live
            scheduled_minutes: Minutos no futuro para agendar (mínimo 3)
            privacy_status: Status de privacidade
        
        Returns:
            (broadcast_id, stream_id, stream_key, rtmp_url) ou (None, None, None, None)
        """
        if not self.initialize_uploader():
            return None, None, None, None
        
        try:
            now_utc = datetime.now(timezone.utc)
            scheduled_time = now_utc + timedelta(minutes=max(scheduled_minutes, 3))
            
            self.logger.info(f"⏰ Criando live agendada para: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
            self.logger.info(f"💡 Iniciando streaming IMEDIATAMENTE - YouTube publica quando detectar stream")
            
            broadcast_id, stream_id, stream_key, rtmp_url = self.uploader.create_live_broadcast(
                title=title,
                scheduled_start_time=scheduled_time,
                description=description,
                privacy_status=privacy_status,
                use_permanent_stream=True
            )
            
            if not broadcast_id:
                self.logger.error("❌ Falha ao criar live")
                return None, None, None, None
            
            self.current_broadcast_id = broadcast_id
            self.current_stream_key = stream_key
            self.current_rtmp_url = rtmp_url
            
            self.logger.info(f"✅ Live criada: {broadcast_id}")
            self.logger.info(f"🔗 Link: https://www.youtube.com/watch?v={broadcast_id}")
            self.logger.info(f"🔑 Stream Key: {stream_key[:10] + '...' if stream_key else '❌ Não disponível'}")
            self.logger.info(f"📍 RTMP URL: {rtmp_url if rtmp_url else '❌ Não disponível'}")
            self.logger.info(f"♻️  Usando stream permanente: mesma chave para todas as lives")
            
            if not stream_key or not rtmp_url:
                self.logger.error("❌ Stream Key ou RTMP URL não disponíveis")
                self.logger.error("💡 O YouTube pode levar alguns minutos para disponibilizar o stream_key")
                self.logger.error(f"💡 Você pode obter manualmente em: https://studio.youtube.com/video/{broadcast_id}/edit")
                return broadcast_id, stream_id, None, None
            
            return broadcast_id, stream_id, stream_key, rtmp_url
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao criar live: {e}")
            import traceback
            traceback.print_exc()
            return None, None, None, None
    
    def start_streaming(self, video_path, stream_key=None, rtmp_url=None, use_automation_fallback=False):
        """
        Inicia transmissão do vídeo em loop usando ffmpeg
        Se ffmpeg não estiver disponível, usa automação web como fallback
        
        Args:
            video_path: Caminho do vídeo
            stream_key: Stream key (usa self.current_stream_key se None)
            rtmp_url: RTMP URL (usa self.current_rtmp_url se None)
            use_automation_fallback: Se True, usa automação web se ffmpeg falhar
        
        Returns:
            True se sucesso, False caso contrário
        """
        stream_key = stream_key or self.current_stream_key
        rtmp_url = rtmp_url or self.current_rtmp_url
        
        if not stream_key or not rtmp_url:
            self.logger.error("❌ Stream Key ou RTMP URL não disponíveis")
            return False
        
        if not os.path.exists(video_path):
            self.logger.error(f"❌ Arquivo de vídeo não encontrado: {video_path}")
            return False
        
        # Verifica conectividade de rede antes de tentar streaming
        try:
            import socket
            rtmp_host = rtmp_url.replace('rtmp://', '').split('/')[0]
            self.logger.info(f"🔍 Verificando conectividade com {rtmp_host}...")
            socket.gethostbyname(rtmp_host)
            self.logger.info("✅ DNS resolvido com sucesso")
        except Exception as e:
            self.logger.warning(f"⚠️  Aviso ao verificar DNS: {e}")
            self.logger.info("💡 Continuando mesmo assim...")
        
        # Tenta usar ffmpeg primeiro
        try:
            rtmp_full_url = f"{rtmp_url}/{stream_key}"
            
            self.logger.info(f"📍 RTMP URL: {rtmp_url}")
            self.logger.info(f"🔑 Stream Key: {stream_key[:10]}...")
            
            # Comando ffmpeg otimizado para streaming RTMP
            # Configurações baseadas nas recomendações oficiais do YouTube:
            # - Codec: H.264 (libx264) para vídeo, AAC para áudio
            # - Resolução: 1920x1080 (1080p) - detectada automaticamente do vídeo
            # - Frame rate: 30fps - detectado automaticamente do vídeo
            # - Bitrate vídeo: 4000k (recomendado: 3000-6000k para 1080p)
            # - Bitrate áudio: 128k (recomendado: 128k)
            # - Sample rate: 44100 Hz (recomendado: 44.1kHz ou 48kHz)
            # - Formato: FLV (RTMP requer FLV)
            ffmpeg_cmd = [
                'ffmpeg',
                '-re',  # Lê na taxa de reprodução (tempo real)
                '-stream_loop', '-1',  # Loop infinito do vídeo
                '-i', video_path,
                '-c:v', 'libx264',  # Codec de vídeo H.264 (recomendado pelo YouTube)
                '-preset', 'veryfast',  # Preset rápido para baixa latência
                '-tune', 'zerolatency',  # Otimização para baixa latência
                '-profile:v', 'high',  # Perfil High (recomendado para 1080p)
                '-level', '4.0',  # Nível H.264 4.0 (compatível com YouTube)
                '-maxrate', '4000k',  # Bitrate máximo: 4000k (dentro da faixa recomendada)
                '-bufsize', '8000k',  # Buffer size: 2x o bitrate (recomendado)
                '-g', '60',  # GOP size: 60 frames (2 segundos a 30fps - recomendado)
                '-keyint_min', '60',  # Keyframe mínimo: igual ao GOP
                '-sc_threshold', '0',  # Desabilita scene change detection (melhor para loop)
                '-c:a', 'aac',  # Codec de áudio AAC (recomendado pelo YouTube)
                '-b:a', '128k',  # Bitrate de áudio: 128k (recomendado)
                '-ar', '44100',  # Sample rate: 44.1kHz (recomendado)
                '-ac', '2',  # Canais de áudio: stereo (recomendado)
                '-f', 'flv',  # Formato de saída: FLV (RTMP requer FLV)
                '-flvflags', 'no_duration_filesize',  # Flag para FLV (otimização)
                '-loglevel', 'warning',  # Nível de log: warning (reduz spam)
                rtmp_full_url
            ]
            
            self.logger.info("🎥 Tentando iniciar streaming com ffmpeg...")
            self.logger.info(f"📝 Comando: {' '.join(ffmpeg_cmd[:5])}... [video em loop]")
            
            # Captura stderr separadamente para debug
            self.ffmpeg_process = subprocess.Popen(
                ffmpeg_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,  # Captura stderr separadamente
                text=True,
                bufsize=1
            )
            
            # Aguarda um pouco para verificar se iniciou corretamente
            # ffmpeg pode demorar alguns segundos para conectar ao RTMP
            time.sleep(5)  # Aguarda 5 segundos inicialmente
            
            # Verifica se ainda está rodando
            if self.ffmpeg_process.poll() is not None:
                # Processo terminou - captura stderr (onde ficam os erros do ffmpeg)
                exit_code = self.ffmpeg_process.returncode
                stderr_output = ""
                
                try:
                    # Lê stderr (onde ficam os erros e informações do ffmpeg)
                    # Usa communicate() para garantir que captura tudo
                    _, stderr_output = self.ffmpeg_process.communicate(timeout=1)
                    if stderr_output and isinstance(stderr_output, bytes):
                        stderr_output = stderr_output.decode('utf-8', errors='ignore')
                    elif not stderr_output:
                        stderr_output = ""
                except subprocess.TimeoutExpired:
                    # Se ainda está rodando, tenta ler o que já foi escrito
                    try:
                        stderr_output = self.ffmpeg_process.stderr.read()
                        if stderr_output and isinstance(stderr_output, bytes):
                            stderr_output = stderr_output.decode('utf-8', errors='ignore')
                        else:
                            stderr_output = ""
                    except:
                        stderr_output = ""
                except Exception as e:
                    self.logger.warning(f"⚠️  Não foi possível ler stderr: {e}")
                    stderr_output = ""
                
                # Log completo do stderr para debug
                if stderr_output:
                    self.logger.error(f"❌ ffmpeg terminou com código {exit_code}")
                    self.logger.error(f"📋 Saída completa do ffmpeg:")
                    
                    # Mostra últimas 30 linhas (onde geralmente está o erro)
                    stderr_lines = stderr_output.strip().split('\n')
                    last_lines = stderr_lines[-30:] if len(stderr_lines) > 30 else stderr_lines
                    
                    for line in last_lines:
                        if line.strip():
                            # Destaque linhas de erro
                            if any(word in line.lower() for word in ['error', 'failed', 'cannot', 'invalid', 'connection']):
                                self.logger.error(f"   ❌ {line.strip()}")
                            else:
                                self.logger.info(f"   ℹ️  {line.strip()}")
                
                # Verifica erros específicos
                stderr_lower = stderr_output.lower()
                error_found = False
                
                if 'failed to resolve hostname' in stderr_lower or 'no address associated with hostname' in stderr_lower:
                    self.logger.error("❌ Erro de DNS - não foi possível resolver o hostname")
                    self.logger.info("💡 Verificando DNS e tentando novamente em 10 segundos...")
                    time.sleep(10)
                    # Tenta novamente uma vez
                    self.logger.info("🔄 Tentando novamente após erro de DNS...")
                    return self.start_streaming(video_path, stream_key, rtmp_url, use_automation_fallback)
                elif 'connection refused' in stderr_lower or 'connection reset' in stderr_lower:
                    self.logger.error("❌ Erro de conexão RTMP - servidor recusou conexão")
                    self.logger.info("💡 Verifique se a stream key e RTMP URL estão corretas")
                    error_found = True
                elif 'authentication' in stderr_lower or 'unauthorized' in stderr_lower:
                    self.logger.error("❌ Erro de autenticação - stream key inválida")
                    error_found = True
                elif 'network' in stderr_lower or 'unreachable' in stderr_lower:
                    self.logger.error("❌ Erro de rede - não foi possível conectar ao servidor RTMP")
                    self.logger.info("💡 Verificando conectividade e tentando novamente em 10 segundos...")
                    time.sleep(10)
                    # Tenta novamente uma vez
                    self.logger.info("🔄 Tentando novamente após erro de rede...")
                    return self.start_streaming(video_path, stream_key, rtmp_url, use_automation_fallback)
                elif 'invalid' in stderr_lower or 'cannot' in stderr_lower:
                    self.logger.error("❌ Erro de formato ou parâmetros inválidos")
                    self.logger.info("💡 Verifique o formato do vídeo ou os parâmetros do ffmpeg")
                    error_found = True
                elif exit_code != 0:
                    self.logger.error(f"❌ ffmpeg terminou com código de erro: {exit_code}")
                    error_found = True
                
                if error_found:
                    self.logger.error("❌ Falha ao iniciar streaming com ffmpeg")
                    if use_automation_fallback:
                        self.logger.info("🔄 Tentando automação web como fallback...")
                        return self._start_streaming_with_automation()
                    return False
                else:
                    # Processo terminou mas sem erros claros
                    self.logger.warning("⚠️  ffmpeg terminou inesperadamente (sem erros claros)")
                    self.logger.info("💡 Verifique os logs acima para mais detalhes")
                    if use_automation_fallback:
                        self.logger.info("🔄 Tentando automação web como fallback...")
                        return self._start_streaming_with_automation()
                    return False
            
            self.logger.info("✅ Streaming iniciado com sucesso via ffmpeg!")
            self.logger.info(f"🔄 Vídeo rodando em loop infinito")
            
            return True
            
        except FileNotFoundError:
            self.logger.warning("⚠️  ffmpeg não encontrado!")
            self.logger.info("🔄 Tentando usar automação web como fallback...")
            
            if use_automation_fallback:
                return self._start_streaming_with_automation()
            else:
                self.logger.error("❌ ffmpeg não encontrado e automação web desabilitada!")
                self.logger.info("💡 Instale ffmpeg:")
                self.logger.info("   sudo apt-get install ffmpeg  # Linux")
                self.logger.info("   brew install ffmpeg           # macOS")
                return False
        except Exception as e:
            self.logger.error(f"❌ Erro ao iniciar streaming: {e}")
            if use_automation_fallback:
                self.logger.info("🔄 Tentando usar automação web como fallback...")
                return self._start_streaming_with_automation()
            import traceback
            traceback.print_exc()
            return False
    
    def _start_streaming_with_automation(self):
        """
        Inicia streaming usando automação web (clica no botão "Transmitir ao vivo")
        
        Returns:
            True se sucesso, False caso contrário
        """
        if not self.current_broadcast_id:
            self.logger.error("❌ Broadcast ID não disponível para automação web")
            return False
        
        self.logger.info("🤖 Iniciando automação web para clicar em 'Transmitir ao vivo'...")
        self.logger.info("💡 Isso abrirá um navegador automaticamente")
        
        try:
            # No Docker, usa headless=True
            import os
            is_docker = os.getenv('DOCKER_CONTAINER', 'false').lower() == 'true'
            headless_mode = is_docker or os.getenv('HEADLESS', 'false').lower() == 'true'
            
            automation = YouTubeAutomation(headless=headless_mode)
            
            success = automation.start_live_automation(
                broadcast_id=self.current_broadcast_id,
                enable_auto_start=True,
                wait_for_login=not is_docker  # No Docker, não espera login (usa cookies)
            )
            
            if success:
                self.logger.info("✅ Live iniciada via automação web!")
                self.logger.info("💡 O navegador permanecerá aberto. Você pode fechá-lo manualmente.")
                # Mantém referência para poder fechar depois
                self.automation = automation
                return True
            else:
                self.logger.error("❌ Falha na automação web")
                automation.close()
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erro na automação web: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def publish_live(self, broadcast_id=None, max_retries=10, retry_delay=30):
        """
        Publica a live (transiciona para 'live')
        
        Args:
            broadcast_id: ID do broadcast (usa self.current_broadcast_id se None)
            max_retries: Número máximo de tentativas (aumentado para 10)
            retry_delay: Segundos entre tentativas (aumentado para 30)
        
        Returns:
            True se sucesso, False caso contrário
        """
        broadcast_id = broadcast_id or self.current_broadcast_id
        
        if not broadcast_id or not self.uploader:
            return False
        
        self.logger.info("⏳ Aguardando YouTube detectar stream e publicar automaticamente...")
        self.logger.info("💡 Isso pode levar 3-5 minutos. O YouTube precisa detectar o stream ativo.")
        
        # Aguarda mais tempo para o YouTube detectar o stream
        # O YouTube geralmente precisa de 3-5 minutos para detectar um stream RTMP ativo
        self.logger.info("⏱️  Aguardando 3 minutos para o YouTube processar o stream...")
        for i in range(6):  # 6 x 30 segundos = 3 minutos
            time.sleep(30)
            remaining = 6 - i - 1
            if remaining > 0:
                self.logger.info(f"⏳ Aguardando... {remaining * 30}s restantes")
        
        self.logger.info("🔄 Tentando publicar live...")
        self.logger.info(f"🔄 Tentando até {max_retries} vezes com intervalo de {retry_delay}s...")
        
        if self.uploader.transition_broadcast_to_live(broadcast_id, max_retries=max_retries, retry_delay=retry_delay):
            self.logger.info("✅ Live publicada automaticamente!")
            return True
        else:
            # Se a API falhar, tenta usar automação web como último recurso
            self.logger.warning("⚠️  API não conseguiu publicar. Tentando automação web...")
            if self._publish_live_with_automation(broadcast_id):
                self.logger.info("✅ Live publicada via automação web!")
                return True
            else:
                self.logger.info("💡 YouTube pode publicar automaticamente quando detectar stream ativo")
                self.logger.info(f"💡 Verifique: https://www.youtube.com/watch?v={broadcast_id}")
                return False
    
    def _publish_live_with_automation(self, broadcast_id):
        """
        Publica a live usando automação web (clica no botão "Transmitir ao vivo")
        
        Args:
            broadcast_id: ID do broadcast
        
        Returns:
            True se sucesso, False caso contrário
        """
        if not broadcast_id:
            self.logger.error("❌ Broadcast ID não disponível para automação web")
            return False
        
        self.logger.info("🤖 Usando automação web para publicar live...")
        
        try:
            # No Docker, usa headless=True
            import os
            is_docker = os.getenv('DOCKER_CONTAINER', 'false').lower() == 'true'
            headless_mode = is_docker or os.getenv('HEADLESS', 'false').lower() == 'true'
            
            automation = YouTubeAutomation(headless=headless_mode)
            
            # Faz login
            if not automation.login_youtube():
                self.logger.error("❌ Falha ao fazer login no YouTube")
                automation.close()
                return False
            
            # Navega para a página da live
            if not automation.go_to_live_stream(broadcast_id):
                self.logger.error("❌ Falha ao navegar para a página da live")
                automation.close()
                return False
            
            # Clica no botão "Transmitir ao vivo"
            if automation.click_go_live_button():
                self.logger.info("✅ Botão 'Transmitir ao vivo' clicado com sucesso!")
                # Mantém referência para poder fechar depois
                self.automation = automation
                return True
            else:
                self.logger.error("❌ Falha ao clicar no botão 'Transmitir ao vivo'")
                automation.close()
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Erro na automação web: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def is_streaming_active(self):
        """Verifica se o streaming está ativo"""
        if not self.ffmpeg_process:
            return False
        
        # Verifica se o processo ainda está rodando
        poll_result = self.ffmpeg_process.poll()
        
        # poll() retorna None se o processo ainda está rodando
        # Retorna código de saída (0 ou outro número) se terminou
        if poll_result is None:
            return True  # Processo está ativo
        
        # Processo terminou - verifica se foi erro ou término normal
        # Código 0 geralmente significa sucesso, mas ffmpeg em loop não deveria terminar
        if poll_result != 0:
            self.logger.warning(f"⚠️  ffmpeg terminou com código de saída: {poll_result}")
        
        return False  # Processo não está mais ativo
    
    def stop_streaming(self):
        """Para o streaming e encerra a live"""
        self.logger.info("🛑 Parando streaming...")
        
        # Para ffmpeg
        if self.ffmpeg_process:
            try:
                self.ffmpeg_process.terminate()
                try:
                    self.ffmpeg_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.logger.warning("⚠️  Forçando encerramento do ffmpeg...")
                    self.ffmpeg_process.kill()
                
                self.logger.info("✅ Streaming parado")
            except Exception as e:
                self.logger.error(f"❌ Erro ao parar streaming: {e}")
            finally:
                self.ffmpeg_process = None
        
        # Fecha automação web se estiver ativa
        if self.automation:
            try:
                self.automation.close()
                self.logger.info("✅ Navegador de automação fechado")
            except Exception as e:
                self.logger.warning(f"⚠️  Erro ao fechar automação: {e}")
            finally:
                self.automation = None
        
        # Encerra live no YouTube
        if self.current_broadcast_id and self.uploader:
            try:
                if hasattr(self.uploader, 'end_broadcast'):
                    self.uploader.end_broadcast(self.current_broadcast_id)
                    self.logger.info("✅ Live encerrada no YouTube")
            except Exception as e:
                self.logger.error(f"❌ Erro ao encerrar live: {e}")

