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
        Usa stream key fixa: 19cr-ehfp-pycp-m8yj-2m85
        
        Returns:
            (stream_id, stream_key, rtmp_url) ou (None, None, None) se falhar
        """
        # STREAM KEY FIXA (sempre a mesma)
        FIXED_STREAM_KEY = "19cr-ehfp-pycp-m8yj-2m85"
        FIXED_RTMP_URL = "rtmp://a.rtmp.youtube.com/live2"
        DEFAULT_STREAM_ID = "0bvegNwA2fGiIN-7wd633g1762446787467917"
        
        if not self.youtube:
            print("❌ Não autenticado no YouTube")
            # Mesmo sem autenticação, retorna a stream key fixa
            print(f"💡 Usando stream key fixa: {FIXED_STREAM_KEY[:10]}...")
            return DEFAULT_STREAM_ID, FIXED_STREAM_KEY, FIXED_RTMP_URL
        
        # Tenta carregar stream permanente salvo
        if os.path.exists(self.stream_config_file):
            try:
                with open(self.stream_config_file, 'r') as f:
                    config = json.load(f)
                    stream_id = config.get('stream_id', DEFAULT_STREAM_ID)
                    stream_key = config.get('stream_key', FIXED_STREAM_KEY)
                    rtmp_url = config.get('rtmp_url', FIXED_RTMP_URL)
                    
                    # SEMPRE usa a stream key fixa (mesmo se o arquivo tiver outra)
                    stream_key = FIXED_STREAM_KEY
                    rtmp_url = FIXED_RTMP_URL
                    
                    print(f"✅ Usando stream permanente do arquivo: {stream_id}")
                    print(f"🔑 Stream Key: {stream_key} (FIXA - sempre a mesma)")
                    print(f"📍 RTMP URL: {rtmp_url}")
                    print(f"💡 Esta chave é fixa e sempre será a mesma")
                    
                    # Verifica se o stream ainda existe (mas não atualiza a key)
                    try:
                        stream_info = self.youtube.liveStreams().list(
                            part='cdn,status,snippet',
                            id=stream_id
                        ).execute()
                        
                        if not stream_info.get('items'):
                            print(f"⚠️  Stream {stream_id} não encontrado na API, mas usando chave fixa mesmo assim")
                    except Exception as e:
                        print(f"⚠️  Erro ao verificar stream na API: {e}")
                        print(f"💡 Continuando com chave fixa mesmo assim")
                    
                    # SEMPRE retorna a chave fixa
                    return stream_id, stream_key, rtmp_url
            except Exception as e:
                print(f"⚠️  Erro ao carregar stream permanente: {e}")
                print(f"💡 Usando stream key fixa: {FIXED_STREAM_KEY}")
                return DEFAULT_STREAM_ID, FIXED_STREAM_KEY, FIXED_RTMP_URL
        
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
            
            # SEMPRE usa a stream key fixa (mesmo se a API retornar outra)
            FIXED_STREAM_KEY = "19cr-ehfp-pycp-m8yj-2m85"
            FIXED_RTMP_URL = "rtmp://a.rtmp.youtube.com/live2"
            
            # Usa stream_key da API se disponível, senão usa a fixa
            final_stream_key = stream_key if stream_key else FIXED_STREAM_KEY
            final_rtmp_url = rtmp_url if rtmp_url else FIXED_RTMP_URL
            
            # Salva stream permanente com chave fixa
            config = {
                'stream_id': stream_id,
                'stream_key': FIXED_STREAM_KEY,  # SEMPRE salva a chave fixa
                'rtmp_url': FIXED_RTMP_URL,
                'created_at': datetime.now().isoformat(),
                'is_fixed_key': True
            }
            
            os.makedirs(os.path.dirname(self.stream_config_file), exist_ok=True)
            with open(self.stream_config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"💾 Stream permanente salvo em: {self.stream_config_file}")
            print(f"🔑 Stream Key: {FIXED_STREAM_KEY} (FIXA - sempre a mesma)")
            print(f"📍 RTMP URL: {FIXED_RTMP_URL}")
            return stream_id, FIXED_STREAM_KEY, FIXED_RTMP_URL
                
        except Exception as e:
            print(f"⚠️  Erro ao criar stream permanente via API: {e}")
            print(f"💡 Usando stream key fixa como fallback")
            # Retorna stream key fixa mesmo se falhar
            FIXED_STREAM_KEY = "19cr-ehfp-pycp-m8yj-2m85"
            FIXED_RTMP_URL = "rtmp://a.rtmp.youtube.com/live2"
            DEFAULT_STREAM_ID = "0bvegNwA2fGiIN-7wd633g1762446787467917"
            return DEFAULT_STREAM_ID, FIXED_STREAM_KEY, FIXED_RTMP_URL
    
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
                print("⏰ Live SEM agendamento - será iniciada imediatamente quando você começar a transmitir")
            
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
                
                # SEMPRE usa a stream key fixa (não tenta obter da API)
                FIXED_STREAM_KEY = "19cr-ehfp-pycp-m8yj-2m85"
                FIXED_RTMP_URL = "rtmp://a.rtmp.youtube.com/live2"
                
                if not stream_key or not rtmp_url:
                    print("💡 Usando stream key fixa (sempre a mesma)")
                    stream_key = FIXED_STREAM_KEY
                    rtmp_url = FIXED_RTMP_URL
                else:
                    # Mesmo se a API retornar, usa a fixa
                    print("💡 Usando stream key fixa (sempre a mesma)")
                    stream_key = FIXED_STREAM_KEY
                    rtmp_url = FIXED_RTMP_URL
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
            
            # SEMPRE usa a stream key fixa (não precisa aguardar da API)
            FIXED_STREAM_KEY = "19cr-ehfp-pycp-m8yj-2m85"
            FIXED_RTMP_URL = "rtmp://a.rtmp.youtube.com/live2"
            
            if not stream_key or not rtmp_url:
                print("💡 Usando stream key fixa (sempre a mesma)")
                stream_key = FIXED_STREAM_KEY
                rtmp_url = FIXED_RTMP_URL
            else:
                # Mesmo se a API retornar, usa a fixa
                print("💡 Usando stream key fixa (sempre a mesma)")
                stream_key = FIXED_STREAM_KEY
                rtmp_url = FIXED_RTMP_URL
            
            print(f"✅ Live criado com sucesso!")
            print(f"🎥 Broadcast ID: {broadcast_id}")
            print(f"📡 Stream ID: {stream_id}")
            print(f"🔗 Link: https://www.youtube.com/watch?v={broadcast_id}")
            if use_permanent_stream:
                print(f"♻️  Stream permanente reutilizado (mesmo stream_key para todas as lives)")
            print(f"🔑 Stream Key: {'✅ Disponível' if stream_key else '❌ Não disponível'}")
            print(f"📍 RTMP URL: {'✅ Disponível' if rtmp_url else '❌ Não disponível'}")
            
            # SEMPRE garante que tem stream key fixa
            if not stream_key or not rtmp_url:
                FIXED_STREAM_KEY = "19cr-ehfp-pycp-m8yj-2m85"
                FIXED_RTMP_URL = "rtmp://a.rtmp.youtube.com/live2"
                print("💡 Usando stream key fixa (sempre a mesma)")
                stream_key = FIXED_STREAM_KEY
                rtmp_url = FIXED_RTMP_URL
            
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
    
    def transition_broadcast_to_live(self, broadcast_id, max_retries=10, retry_delay=30):
        """
        Transiciona o broadcast de 'ready' para 'live' (publica a live)
        Tenta múltiplas vezes até o stream estar ativo
        
        Args:
            broadcast_id: ID do broadcast
            max_retries: Número máximo de tentativas
            retry_delay: Segundos entre tentativas
        
        Returns:
            True se sucesso, False caso contrário
        """
        if not self.youtube:
            print("❌ Não autenticado no YouTube")
            return False
        
        import time
        
        for attempt in range(1, max_retries + 1):
            try:
                # Verifica status do broadcast ANTES de tentar transição
                broadcast_status = None
                stream_status = None
                try:
                    broadcast_info = self.youtube.liveBroadcasts().list(
                        part='status,contentDetails',
                        id=broadcast_id
                    ).execute()
                    
                    if broadcast_info.get('items'):
                        status = broadcast_info['items'][0].get('status', {})
                        content_details = broadcast_info['items'][0].get('contentDetails', {})
                        snippet = broadcast_info['items'][0].get('snippet', {})
                        
                        broadcast_status = status.get('lifeCycleStatus', '')
                        recording_status = status.get('recordingStatus', '')
                        made_for_kids = snippet.get('selfDeclaredMadeForKids', False)
                        stream_id = content_details.get('boundStreamId', '')
                        
                        # Log detalhado do status
                        print(f"   📋 Detalhes do broadcast:")
                        print(f"      - lifeCycleStatus: {broadcast_status}")
                        print(f"      - recordingStatus: {recording_status}")
                        print(f"      - madeForKids: {made_for_kids}")
                        print(f"      - boundStreamId: {stream_id}")
                        
                        # Verifica status do stream
                        if stream_id:
                            try:
                                stream_info = self.youtube.liveStreams().list(
                                    part='status,snippet',
                                    id=stream_id
                                ).execute()
                                
                                if stream_info.get('items'):
                                    stream_status_obj = stream_info['items'][0].get('status', {})
                                    stream_status = stream_status_obj.get('streamStatus', '')
                                    health_status = stream_status_obj.get('healthStatus', {})
                                    
                                    print(f"   📋 Detalhes do stream:")
                                    print(f"      - streamStatus: {stream_status}")
                                    print(f"      - healthStatus: {health_status}")
                            except Exception as e:
                                print(f"   ⚠️  Erro ao obter detalhes do stream: {e}")
                                pass
                        
                        # Se já está 'live', retorna sucesso
                        if broadcast_status == 'live':
                            print(f"✅ Live já está publicada!")
                            return True
                        # Se já está 'complete', não pode mais transicionar
                        elif broadcast_status == 'complete':
                            print(f"⚠️  Live já foi encerrada")
                            return False
                        # Se está 'testing', precisa ir para 'ready' primeiro
                        elif broadcast_status == 'testing':
                            print(f"⚠️  Broadcast está em 'testing'. Transicionando para 'ready' primeiro...")
                            try:
                                self.youtube.liveBroadcasts().transition(
                                    broadcastStatus='ready',
                                    id=broadcast_id,
                                    part='id,snippet,contentDetails,status'
                                ).execute()
                                print(f"✅ Transicionado para 'ready'. Aguardando {retry_delay}s...")
                                time.sleep(retry_delay)
                            except:
                                pass
                except Exception as e:
                    print(f"⚠️  Erro ao verificar status: {e}")
                    pass  # Continua mesmo se não conseguir verificar
                
                # Log do status atual
                if broadcast_status:
                    print(f"📊 Status atual do broadcast: {broadcast_status}")
                if stream_status:
                    print(f"📊 Status do stream: {stream_status}")
                
                # Verifica se o stream está realmente ativo antes de tentar transicionar
                if stream_status and stream_status != 'active':
                    if attempt < max_retries:
                        print(f"⏳ Stream ainda não está ativo (status: {stream_status}). Aguardando {retry_delay}s...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        print(f"⚠️  Stream não está ativo após {max_retries} tentativas (status: {stream_status})")
                        return False
                
                # Só tenta transicionar se estiver em 'ready' e stream estiver 'active'
                if broadcast_status and broadcast_status not in ['ready', 'live']:
                    if attempt < max_retries:
                        print(f"⏳ Broadcast está em '{broadcast_status}'. Aguardando {retry_delay}s...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        print(f"⚠️  Broadcast não está em estado 'ready' (está em '{broadcast_status}')")
                        return False
                
                # Se stream está ativo mas broadcast não está em 'ready', aguarda mais
                if stream_status == 'active' and broadcast_status != 'ready' and broadcast_status != 'live':
                    if attempt < max_retries:
                        print(f"⏳ Stream ativo mas broadcast em '{broadcast_status}'. Aguardando {retry_delay}s...")
                        time.sleep(retry_delay)
                        continue
                
                print(f"🔄 Tentativa {attempt}/{max_retries}: Transicionando broadcast para 'live'...")
                print(f"   📊 Broadcast: {broadcast_status}, Stream: {stream_status}")
                
                # Verifica se o stream está ativo há tempo suficiente
                # O YouTube pode precisar de pelo menos 2-3 minutos de stream ativo antes de permitir transição
                if attempt < 3 and stream_status == 'active':
                    print(f"💡 Stream está ativo mas pode precisar de mais tempo. Aguardando {retry_delay}s...")
                    time.sleep(retry_delay)
                    continue
                
                # Transição: 'testing' -> 'ready' -> 'live' -> 'complete'
                # Vamos de 'ready' para 'live'
                try:
                    transition_response = self.youtube.liveBroadcasts().transition(
                        broadcastStatus='live',
                        id=broadcast_id,
                        part='id,snippet,contentDetails,status'
                    ).execute()
                except Exception as e:
                    # Se falhar, tenta verificar se já está live (pode ter sido publicado automaticamente)
                    try:
                        check_response = self.youtube.liveBroadcasts().list(
                            part='status',
                            id=broadcast_id
                        ).execute()
                        if check_response.get('items'):
                            current_status = check_response['items'][0].get('status', {}).get('lifeCycleStatus', '')
                            if current_status == 'live':
                                print(f"✅ Live foi publicada automaticamente pelo YouTube!")
                                print(f"🔗 Link: https://www.youtube.com/watch?v={broadcast_id}")
                                return True
                    except:
                        pass
                    raise  # Re-lança o erro original
                
                print(f"✅ Live publicada com sucesso!")
                print(f"🔗 Link: https://www.youtube.com/watch?v={broadcast_id}")
                return True
                
            except HttpError as e:
                error_details = e.error_details if hasattr(e, 'error_details') else []
                error_reason = None
                for detail in error_details:
                    if isinstance(detail, dict) and 'reason' in detail:
                        error_reason = detail['reason']
                        break
                
                if error_reason == 'streamNotActive':
                    if attempt < max_retries:
                        print(f"⏳ Stream ainda não está ativo. Aguardando {retry_delay}s antes de tentar novamente...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        print("⚠️  Stream ainda não está ativo após múltiplas tentativas")
                        print("💡 A live será publicada automaticamente quando o YouTube detectar o stream")
                        return False
                elif error_reason == 'broadcastNotReady':
                    if attempt < max_retries:
                        print(f"⏳ Broadcast ainda não está pronto. Aguardando {retry_delay}s...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        print("⚠️  Broadcast ainda não está pronto para transição")
                        return False
                elif error_reason == 'invalidTransition':
                    if attempt < max_retries:
                        print(f"⏳ Transição inválida - broadcast pode não estar no estado correto")
                        print(f"💡 Aguardando {retry_delay}s para o YouTube processar o stream...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        print("⚠️  Não foi possível transicionar para 'live'")
                        print("💡 O YouTube pode publicar automaticamente quando detectar o stream ativo")
                        print(f"💡 Verifique manualmente: https://www.youtube.com/watch?v={broadcast_id}")
                        return False
                else:
                    if attempt < max_retries:
                        print(f"⚠️  Erro na tentativa {attempt}: {e}")
                        print(f"⏳ Aguardando {retry_delay}s antes de tentar novamente...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        print(f"⚠️  Erro ao transicionar para 'live' após {max_retries} tentativas: {e}")
                        print(f"💡 A live pode ser publicada manualmente no YouTube Studio")
                        return False
            except Exception as e:
                if attempt < max_retries:
                    print(f"⚠️  Erro na tentativa {attempt}: {e}")
                    print(f"⏳ Aguardando {retry_delay}s antes de tentar novamente...")
                    time.sleep(retry_delay)
                    continue
                else:
                    print(f"⚠️  Erro ao transicionar broadcast após {max_retries} tentativas: {e}")
                    return False
        
        return False
    
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
    
    def end_broadcast(self, broadcast_id):
        """
        Encerra uma live broadcast (transiciona para 'complete')
        
        Args:
            broadcast_id: ID do broadcast a ser encerrado
            
        Returns:
            True se sucesso, False caso contrário
        """
        if not self.youtube:
            print("❌ Não autenticado no YouTube")
            return False
        
        try:
            # Transiciona para 'complete' (encerra a live)
            transition_response = self.youtube.liveBroadcasts().transition(
                broadcastStatus='complete',
                id=broadcast_id,
                part='id,snippet,contentDetails,status'
            ).execute()
            
            print(f"✅ Live encerrada com sucesso: {broadcast_id}")
            return True
            
        except HttpError as e:
            error_details = e.error_details if hasattr(e, 'error_details') else []
            error_reason = None
            for detail in error_details:
                if isinstance(detail, dict) and 'reason' in detail:
                    error_reason = detail['reason']
                    break
            
            print(f"⚠️  Erro ao encerrar live: {error_reason or str(e)}")
            return False
        except Exception as e:
            print(f"⚠️  Erro ao encerrar live: {e}")
            return False


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

