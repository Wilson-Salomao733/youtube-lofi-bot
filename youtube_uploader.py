"""
Integração com YouTube API para upload de vídeos e criação de lives
"""
import os
import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import pickle


SCOPES = ['https://www.googleapis.com/auth/youtube.upload',
          'https://www.googleapis.com/auth/youtube.force-ssl']


class YouTubeUploader:
    """Gerencia upload e lives no YouTube"""
    
    def __init__(self, credentials_file='credentials/credentials.json',
                 token_file='credentials/token.pickle',
                 stream_config_file='credentials/stream_config.json'):
        """
        Inicializa o uploader do YouTube
        
        Args:
            credentials_file: Arquivo JSON com credenciais da API
            token_file: Arquivo para armazenar o token de autenticação
            stream_config_file: Arquivo para armazenar stream permanente
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.stream_config_file = stream_config_file
        self.youtube = None
        self._authenticate()
    
    def _authenticate(self):
        """Autentica com a API do YouTube"""
        creds = None
        
        # Tenta carregar token salvo
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # Se não há credenciais válidas, solicita autenticação
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    print(f"❌ Arquivo de credenciais não encontrado: {self.credentials_file}")
                    print("📝 Crie um arquivo credentials.json com suas credenciais do Google Cloud Console")
                    print("🔗 https://console.cloud.google.com/apis/credentials")
                    return False
                
                # Converte credenciais web para installed se necessário
                self._ensure_installed_credentials()
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            # Salva credenciais para próxima vez
            os.makedirs(os.path.dirname(self.token_file), exist_ok=True)
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.youtube = build('youtube', 'v3', credentials=creds)
        print("✅ Autenticado no YouTube com sucesso!")
        return True
    
    def _ensure_installed_credentials(self):
        """Converte credenciais web para installed se necessário"""
        try:
            with open(self.credentials_file, 'r') as f:
                creds_data = json.load(f)
            
            # Se tiver "web" mas não "installed", converte
            if 'web' in creds_data and 'installed' not in creds_data:
                print("📝 Convertendo credenciais web para desktop...")
                creds_data['installed'] = creds_data['web']
                
                # Salva o arquivo convertido
                with open(self.credentials_file, 'w') as f:
                    json.dump(creds_data, f, indent=2)
                print("✅ Credenciais convertidas com sucesso!")
        except Exception as e:
            print(f"⚠️  Aviso ao converter credenciais: {e}")
    
    def upload_video(self, video_file, title, description="", tags=[], 
                     category_id="22", privacy_status="private"):
        """
        Faz upload de um vídeo
        
        Args:
            video_file: Caminho do arquivo de vídeo
            title: Título do vídeo
            description: Descrição do vídeo
            tags: Lista de tags
            category_id: ID da categoria (22 = Pessoas e blogs)
            privacy_status: Status de privacidade (public, unlisted, private)
        
        Returns:
            ID do vídeo ou None em caso de erro
        """
        if not self.youtube:
            print("❌ Não autenticado no YouTube")
            return None
        
        if not os.path.exists(video_file):
            print(f"❌ Arquivo de vídeo não encontrado: {video_file}")
            return None
        
        print(f"📤 Fazendo upload do vídeo: {title}")
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': category_id
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False
            }
        }
        
        try:
            media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
            insert_request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = insert_request.next_chunk()
                if status:
                    print(f"📊 Progresso: {int(status.progress() * 100)}%")
            
            video_id = response['id']
            print(f"✅ Vídeo enviado com sucesso! ID: {video_id}")
            print(f"🔗 https://www.youtube.com/watch?v={video_id}")
            return video_id
            
        except HttpError as e:
            print(f"❌ Erro ao enviar vídeo: {e}")
            return None
    
    def get_or_create_permanent_stream(self):
        """
        Obtém ou cria um stream permanente que pode ser reutilizado para todas as lives
        
        Returns:
            (stream_id, stream_key, rtmp_url) ou (None, None, None) se falhar
        """
        if not self.youtube:
            print("❌ Não autenticado no YouTube")
            return None, None, None
        
        # Tenta carregar stream permanente salvo
        if os.path.exists(self.stream_config_file):
            try:
                with open(self.stream_config_file, 'r') as f:
                    config = json.load(f)
                    stream_id = config.get('stream_id')
                    stream_key = config.get('stream_key')
                    rtmp_url = config.get('rtmp_url')
                    
                    if stream_id and stream_key and rtmp_url:
                        # Verifica se o stream ainda é válido
                        try:
                            stream_info = self.youtube.liveStreams().list(
                                part='cdn,status,snippet',
                                id=stream_id
                            ).execute()
                            
                            if stream_info.get('items'):
                                item = stream_info['items'][0]
                                cdn_info = item.get('cdn', {})
                                ingestion_info = cdn_info.get('ingestionInfo', {})
                                current_key = ingestion_info.get('streamKey', '')
                                
                                if current_key:
                                    print(f"✅ Usando stream permanente existente: {stream_id}")
                                    # Atualiza com key da API se diferente
                                    if current_key != stream_key:
                                        config['stream_key'] = current_key
                                        config['rtmp_url'] = ingestion_info.get('ingestionAddress', rtmp_url)
                                        with open(self.stream_config_file, 'w') as f:
                                            json.dump(config, f, indent=2)
                                    return stream_id, current_key, ingestion_info.get('ingestionAddress', rtmp_url)
                                else:
                                    # Stream existe mas API não retorna key, usa a salva
                                    print(f"⚠️  API não retornou stream_key, usando o salvo no arquivo")
                                    print(f"✅ Usando stream permanente existente (key do arquivo): {stream_id}")
                                    return stream_id, stream_key, rtmp_url
                        except Exception as e:
                            print(f"⚠️  Erro ao verificar stream permanente: {e}")
                            # Se o stream existe mas deu erro, usa o key salvo mesmo assim
                            print(f"✅ Usando stream permanente existente (key do arquivo): {stream_id}")
                            return stream_id, stream_key, rtmp_url
            except Exception as e:
                print(f"⚠️  Erro ao carregar stream permanente: {e}")
        
        # Cria um novo stream permanente
        print("🆕 Criando novo stream permanente (será reutilizado para todas as lives)...")
        try:
            stream_body = {
                'snippet': {
                    'title': 'LOFI Live - Stream Permanente'
                },
                'cdn': {
                    'format': '1080p',
                    'ingestionType': 'rtmp',
                    'resolution': '1080p',
                    'frameRate': '30fps'
                }
            }
            
            stream_response = self.youtube.liveStreams().insert(
                part='snippet,cdn',
                body=stream_body
            ).execute()
            
            stream_id = stream_response['id']
            print(f"✅ Stream permanente criado: {stream_id}")
            
            # Tenta obter stream_key com retry mais agressivo
            import time
            stream_key = None
            rtmp_url = None
            max_retries = 15  # Aumentado para 15 tentativas
            retry_delay = 20  # Aumentado para 20 segundos entre tentativas
            
            print(f"🔍 Aguardando stream_key ficar disponível (pode levar até {max_retries * retry_delay / 60:.1f} minutos)...")
            
            for attempt in range(1, max_retries + 1):
                try:
                    stream_info = self.youtube.liveStreams().list(
                        part='cdn,status,snippet',
                        id=stream_id
                    ).execute()
                    
                    if stream_info.get('items'):
                        item = stream_info['items'][0]
                        cdn_info = item.get('cdn', {})
                        ingestion_info = cdn_info.get('ingestionInfo', {})
                        stream_key = ingestion_info.get('streamKey', '')
                        rtmp_url = ingestion_info.get('ingestionAddress', '')
                        
                        if stream_key and rtmp_url:
                            print(f"✅ Stream Key obtido na tentativa {attempt}/{max_retries}!")
                            break
                        else:
                            if attempt < max_retries:
                                print(f"⏳ Tentativa {attempt}/{max_retries}: Stream Key ainda não disponível, aguardando {retry_delay}s...")
                                time.sleep(retry_delay)
                except Exception as e:
                    if attempt < max_retries:
                        print(f"⚠️  Erro na tentativa {attempt}/{max_retries}: {e}")
                        time.sleep(retry_delay)
            
            if stream_key and rtmp_url:
                # Salva stream permanente
                config = {
                    'stream_id': stream_id,
                    'stream_key': stream_key,
                    'rtmp_url': rtmp_url,
                    'created_at': datetime.now().isoformat()
                }
                
                os.makedirs(os.path.dirname(self.stream_config_file), exist_ok=True)
                with open(self.stream_config_file, 'w') as f:
                    json.dump(config, f, indent=2)
                
                print(f"💾 Stream permanente salvo em: {self.stream_config_file}")
                print(f"🔑 Stream Key: {stream_key[:20]}... (será reutilizado para todas as lives)")
                return stream_id, stream_key, rtmp_url
            else:
                print("⚠️  Stream criado mas stream_key não disponível ainda")
                print("💡 Tente novamente em alguns minutos ou obtenha manualmente no YouTube Studio")
                return stream_id, None, None
                
        except Exception as e:
            print(f"❌ Erro ao criar stream permanente: {e}")
            import traceback
            traceback.print_exc()
            return None, None, None
    
    def create_live_broadcast(self, title, scheduled_start_time=None, 
                              description="", privacy_status="public", use_permanent_stream=True):
        """
        Cria um live streaming no YouTube
        
        Args:
            title: Título do live
            scheduled_start_time: Data e hora agendada (datetime)
            description: Descrição do live
            privacy_status: Status de privacidade
        
        Returns:
            ID do broadcast e stream_key
        """
        if not self.youtube:
            print("❌ Não autenticado no YouTube")
            return None, None
        
        # Se não especificado, cria para começar imediatamente (sem agendamento)
        scheduled_start_time_str = None
        if scheduled_start_time:
            # YouTube requer formato ISO 8601 em UTC com Z
            # Deve ser entre 10 minutos e 7 dias no futuro
            from datetime import timezone
            if scheduled_start_time.tzinfo is None:
                scheduled_start_time = scheduled_start_time.replace(tzinfo=timezone.utc)
            else:
                scheduled_start_time = scheduled_start_time.astimezone(timezone.utc)
            scheduled_start_time_str = scheduled_start_time.isoformat().replace('+00:00', 'Z')
        
        print(f"🎬 Criando live: {title}")
        print(f"⏰ Agendado para: {scheduled_start_time}")
        
        try:
            # Cria o broadcast
            broadcast_body = {
                'snippet': {
                    'title': title,
                    'description': description
                },
                'status': {
                    'privacyStatus': privacy_status,
                    'selfDeclaredMadeForKids': False
                }
            }
            
            # Adiciona scheduledStartTime apenas se fornecido
            if scheduled_start_time_str:
                broadcast_body['snippet']['scheduledStartTime'] = scheduled_start_time_str
                print(f"⏰ Agendado para: {scheduled_start_time_str}")
            else:
                print("⏰ Live será iniciada imediatamente quando você começar a transmitir")
            
            broadcast_response = self.youtube.liveBroadcasts().insert(
                part='snippet,contentDetails,status',
                body=broadcast_body
            ).execute()
            
            broadcast_id = broadcast_response['id']
            
            # Usa stream permanente se solicitado, senão cria um novo
            if use_permanent_stream:
                stream_id, stream_key, rtmp_url = self.get_or_create_permanent_stream()
                
                if not stream_id:
                    print("❌ Falha ao obter/criar stream permanente")
                    return None, None, None, None
                
                print(f"♻️  Usando stream permanente: {stream_id}")
                
                # Se stream_key não está disponível, tenta obter novamente com mais tentativas
                if not stream_key or not rtmp_url:
                    print("⚠️  Stream permanente criado mas stream_key não disponível ainda")
                    print("🔄 Tentando obter stream_key novamente (aguarde, pode levar alguns minutos)...")
                    import time
                    max_retries = 20  # Mais tentativas
                    retry_delay = 15  # 15 segundos entre tentativas
                    
                    for attempt in range(1, max_retries + 1):
                        time.sleep(retry_delay)
                        try:
                            stream_info = self.youtube.liveStreams().list(
                                part='cdn,status,snippet',
                                id=stream_id
                            ).execute()
                            
                            if stream_info.get('items'):
                                item = stream_info['items'][0]
                                cdn_info = item.get('cdn', {})
                                ingestion_info = cdn_info.get('ingestionInfo', {})
                                stream_key = ingestion_info.get('streamKey', '')
                                rtmp_url = ingestion_info.get('ingestionAddress', '')
                                
                                if stream_key and rtmp_url:
                                    print(f"✅ Stream Key obtido na tentativa {attempt}/{max_retries}!")
                                    # Atualiza arquivo de configuração
                                    config = {
                                        'stream_id': stream_id,
                                        'stream_key': stream_key,
                                        'rtmp_url': rtmp_url,
                                        'created_at': datetime.now().isoformat()
                                    }
                                    os.makedirs(os.path.dirname(self.stream_config_file), exist_ok=True)
                                    with open(self.stream_config_file, 'w') as f:
                                        json.dump(config, f, indent=2)
                                    print(f"💾 Stream permanente atualizado com stream_key")
                                    break
                                else:
                                    if attempt % 3 == 0:  # Mostra progresso a cada 3 tentativas
                                        print(f"⏳ Tentativa {attempt}/{max_retries}: Stream Key ainda não disponível... (aguardando {retry_delay}s)")
                        except Exception as e:
                            if attempt % 3 == 0:
                                print(f"⚠️  Erro na tentativa {attempt}/{max_retries}: {e}")
                    
                    if not stream_key or not rtmp_url:
                        print("⚠️  Stream Key ainda não disponível após múltiplas tentativas")
                        print("💡 O stream permanente foi criado, mas o stream_key precisa ser obtido manualmente")
                        print(f"💡 Acesse: https://studio.youtube.com/ e obtenha o stream_key")
                        print(f"💡 Depois salve em: {self.stream_config_file}")
                        print(f"💡 Ou aguarde alguns minutos e tente criar a live novamente")
            else:
                # Cria um novo stream (comportamento antigo)
                stream_body = {
                    'snippet': {
                        'title': f"Stream for {title}"
                    },
                    'cdn': {
                        'format': '1080p',
                        'ingestionType': 'rtmp',
                        'resolution': '1080p',
                        'frameRate': '30fps'
                    }
                }
                
                stream_response = self.youtube.liveStreams().insert(
                    part='snippet,cdn',
                    body=stream_body
                ).execute()
                
                stream_id = stream_response['id']
                stream_key = None
                rtmp_url = None
                
                # Tenta obter stream_key com retry
                import time
                max_retries = 5
                retry_delay = 10
                
                print(f"🔍 Buscando Stream Key (pode levar alguns segundos)...")
                
                for attempt in range(1, max_retries + 1):
                    try:
                        stream_info = self.youtube.liveStreams().list(
                            part='cdn,status,snippet',
                            id=stream_id
                        ).execute()
                        
                        if stream_info.get('items'):
                            item = stream_info['items'][0]
                            cdn_info = item.get('cdn', {})
                            ingestion_info = cdn_info.get('ingestionInfo', {})
                            stream_key = ingestion_info.get('streamKey', '')
                            rtmp_url = ingestion_info.get('ingestionAddress', '')
                            
                            if stream_key and rtmp_url:
                                print(f"✅ Stream Key obtido na tentativa {attempt}/{max_retries}")
                                break
                            else:
                                if attempt < max_retries:
                                    print(f"⏳ Tentativa {attempt}/{max_retries}: Stream Key ainda não disponível, aguardando {retry_delay}s...")
                                    time.sleep(retry_delay)
                                else:
                                    print(f"⚠️  Tentativa {attempt}/{max_retries}: Stream Key ainda não disponível após {max_retries} tentativas")
                    except Exception as e:
                        if attempt < max_retries:
                            print(f"⚠️  Erro na tentativa {attempt}/{max_retries}: {e}")
                            time.sleep(retry_delay)
            
            # Vincula broadcast e stream
            bind_response = self.youtube.liveBroadcasts().bind(
                part='id,contentDetails',
                id=broadcast_id,
                streamId=stream_id
            ).execute()
            
            print(f"✅ Broadcast vinculado ao stream!")
            
            # Se stream_key ainda não está disponível, tenta obter após vincular
            if not stream_key or not rtmp_url:
                print("🔄 Stream vinculado, aguardando stream_key ficar disponível...")
                import time
                max_retries = 20
                retry_delay = 15
                
                for attempt in range(1, max_retries + 1):
                    time.sleep(retry_delay)
                    try:
                        stream_info = self.youtube.liveStreams().list(
                            part='cdn,status,snippet',
                            id=stream_id
                        ).execute()
                        
                        if stream_info.get('items'):
                            item = stream_info['items'][0]
                            cdn_info = item.get('cdn', {})
                            ingestion_info = cdn_info.get('ingestionInfo', {})
                            stream_key = ingestion_info.get('streamKey', '')
                            rtmp_url = ingestion_info.get('ingestionAddress', '')
                            
                            if stream_key and rtmp_url:
                                print(f"✅ Stream Key obtido após vincular (tentativa {attempt}/{max_retries})!")
                                # Atualiza config se for stream permanente
                                if use_permanent_stream and os.path.exists(self.stream_config_file):
                                    try:
                                        with open(self.stream_config_file, 'r') as f:
                                            config = json.load(f)
                                        config['stream_key'] = stream_key
                                        config['rtmp_url'] = rtmp_url
                                        with open(self.stream_config_file, 'w') as f:
                                            json.dump(config, f, indent=2)
                                        print(f"💾 Stream permanente atualizado com stream_key")
                                    except:
                                        pass
                                break
                            else:
                                if attempt % 3 == 0:
                                    print(f"⏳ Tentativa {attempt}/{max_retries}: Stream Key ainda não disponível... (aguardando {retry_delay}s)")
                    except Exception as e:
                        if attempt % 3 == 0:
                            print(f"⚠️  Erro na tentativa {attempt}/{max_retries}: {e}")
            
            print(f"✅ Live criado com sucesso!")
            print(f"🎥 Broadcast ID: {broadcast_id}")
            print(f"📡 Stream ID: {stream_id}")
            print(f"🔗 Link: https://www.youtube.com/watch?v={broadcast_id}")
            if use_permanent_stream:
                print(f"♻️  Stream permanente reutilizado (mesmo stream_key para todas as lives)")
            print(f"🔑 Stream Key: {'✅ Disponível' if stream_key else '❌ Não disponível'}")
            print(f"📍 RTMP URL: {'✅ Disponível' if rtmp_url else '❌ Não disponível'}")
            
            if not stream_key or not rtmp_url:
                if use_permanent_stream:
                    print("⚠️  ATENÇÃO: Stream Key não disponível do stream permanente!")
                    print("💡 Verifique o arquivo: credentials/stream_config.json")
                    print("💡 Ou obtenha manualmente em: https://studio.youtube.com/")
                else:
                    print("⚠️  ATENÇÃO: Stream Key ou RTMP URL não foram retornados após múltiplas tentativas!")
                    print("💡 Isso pode acontecer se o stream ainda não estiver pronto.")
                    print("💡 O YouTube pode levar alguns minutos para disponibilizar o stream_key.")
                    print(f"💡 Você pode obter manualmente em: https://studio.youtube.com/video/{broadcast_id}/edit")
            
            return broadcast_id, stream_id, stream_key, rtmp_url
            
        except HttpError as e:
            error_details = e.error_details if hasattr(e, 'error_details') else []
            error_reason = None
            for detail in error_details:
                if isinstance(detail, dict) and 'reason' in detail:
                    error_reason = detail['reason']
                    break
            
            print(f"❌ Erro ao criar live: {e}")
            import traceback
            traceback.print_exc()
            
            if error_reason == 'liveStreamingNotEnabled':
                print("\n" + "=" * 60)
                print("⚠️  CANAL NÃO HABILITADO PARA LIVE STREAMING")
                print("=" * 60)
                print("\n📋 Requisitos do YouTube para Live Streaming:")
                print("   1. Canal precisa ter pelo menos 1,000 inscritos")
                print("   2. Ou canal verificado pelo YouTube")
                print("   3. Conta sem restrições de live streaming")
                print("\n💡 Como habilitar:")
                print("   1. Acesse: https://www.youtube.com/features")
                print("   2. Vá em 'Transmissões'")
                print("   3. Siga as instruções para habilitar")
                print("\n🔗 Ou acesse diretamente:")
                print("   https://studio.youtube.com/")
                print("   Vá em: Transmissões → Configurações")
                print("\n📌 Alternativas:")
                print("   - Fazer upload de vídeos normais (sem live)")
                print("   - Aguardar até ter 1,000 inscritos")
                print("   - Verificar seu canal no YouTube")
                print("=" * 60)
            elif error_reason == 'invalidScheduledStartTime':
                print("\n" + "=" * 60)
                print("⚠️  HORÁRIO AGENDADO INVÁLIDO")
                print("=" * 60)
                print("\n📋 Requisitos do YouTube:")
                print("   - Horário deve ser pelo menos 10 minutos no futuro")
                print("   - Horário deve ser no máximo 7 dias no futuro")
                print(f"\n💡 Horário tentado: {scheduled_start_time}")
                print("=" * 60)
            
            return None, None, None, None
    
    def upload_video_to_live(self, video_file, broadcast_id):
        """
        Faz upload de um vídeo para ser usado em uma live
        
        Args:
            video_file: Caminho do arquivo de vídeo
            broadcast_id: ID do broadcast
        
        Returns:
            True se sucesso
        """
        # Para lives com vídeo, precisamos de OBS ou similar
        # Este é um placeholder para integração futura
        print(f"📤 Upload de vídeo para live: {broadcast_id}")
        print("📝 Nota: Para lives com vídeo, use OBS com a stream_key")
        return True


# Função helper para configuração rápida
def setup_youtube_api():
    """Guia de configuração da API do YouTube"""
    print("🔧 Configuração da API do YouTube")
    print("=" * 50)
    print("\n1. Acesse: https://console.cloud.google.com/")
    print("2. Crie um novo projeto ou selecione um existente")
    print("3. Ative a YouTube Data API v3")
    print("4. Vá em 'Credenciais' -> 'Criar credenciais' -> 'ID do cliente OAuth'")
    print("5. Tipo: Aplicativo da área de trabalho")
    print("6. Baixe as credenciais JSON")
    print("7. Salve como: credentials/credentials.json")
    print("\n📁 Estrutura esperada:")
    print("credentials/")
    print("  ├── credentials.json  (baixado do Google Cloud)")
    print("  └── token.pickle       (gerado automaticamente)")
    print("\n")


if __name__ == "__main__":
    setup_youtube_api()

