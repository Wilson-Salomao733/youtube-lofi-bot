"""
Script para testar live e verificar qual conta está sendo usada
"""
import sys
from datetime import datetime, timedelta
from youtube_uploader import YouTubeUploader
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def test_live_with_account_check():
    """Testa criação de live e verifica a conta"""
    logger.info("=" * 60)
    logger.info("🧪 TESTE DE LIVE COM VERIFICAÇÃO DE CONTA")
    logger.info("=" * 60)
    
    # Conectar ao YouTube
    logger.info("\n1️⃣  Conectando ao YouTube...")
    logger.info("   ⚠️  IMPORTANTE: Escolha a conta lofiwilson0@gmail.com")
    logger.info("   ⚠️  Se abrir navegador, selecione: lofiwilson0@gmail.com")
    
    try:
        uploader = YouTubeUploader()
        if not uploader.youtube:
            logger.error("❌ Falha na autenticação do YouTube")
            return False
        logger.info("✅ Conectado com sucesso!")
        
        # Verifica qual canal está sendo usado
        try:
            logger.info("\n2️⃣  Verificando qual conta está sendo usada...")
            channels_response = uploader.youtube.channels().list(
                part='snippet',
                mine=True
            ).execute()
            
            if channels_response.get('items'):
                channel = channels_response['items'][0]
                channel_title = channel['snippet']['title']
                logger.info(f"   📺 Canal: {channel_title}")
                logger.info(f"   📧 ID do Canal: {channel['id']}")
                
                # Verifica se é o canal correto
                if 'lofi' in channel_title.lower() or 'wilson' in channel_title.lower():
                    logger.info("   ✅ Parece ser o canal correto!")
                else:
                    logger.warning("   ⚠️  Verifique se é o canal correto (lofiwilson0@gmail.com)")
            else:
                logger.warning("   ⚠️  Não foi possível identificar o canal")
        except Exception as e:
            logger.warning(f"   ⚠️  Não foi possível verificar canal: {e}")
        
        # Tentar criar live
        logger.info("\n3️⃣  Tentando criar live de teste...")
        
        title = f"LOFI Test Live - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        description = "Teste de criação de live automatizada - lofiwilson0@gmail.com"
        # YouTube requer scheduledStartTime entre 10 minutos e 7 dias no futuro
        # Vamos agendar para 30 minutos no futuro para garantir
        from datetime import timezone
        scheduled_time = datetime.now(timezone.utc) + timedelta(minutes=30)
        
        logger.info(f"   📝 Título: {title}")
        logger.info(f"   ⏰ Agendado para: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        try:
            broadcast_id, stream_id, stream_key, rtmp_url = uploader.create_live_broadcast(
                title=title,
                scheduled_start_time=scheduled_time,
                description=description,
                privacy_status="public"
            )
            
            if broadcast_id:
                logger.info("\n" + "=" * 60)
                logger.info("✅ LIVE CRIADA COM SUCESSO!")
                logger.info("=" * 60)
                logger.info(f"🎥 Broadcast ID: {broadcast_id}")
                logger.info(f"📡 Stream ID: {stream_id}")
                logger.info(f"🔗 Link: https://www.youtube.com/watch?v={broadcast_id}")
                if stream_key:
                    logger.info(f"🔑 Stream Key: {stream_key[:20]}...")
                if rtmp_url:
                    logger.info(f"📍 RTMP URL: {rtmp_url}")
                logger.info("\n✅ Seu canal ESTÁ habilitado para live streaming!")
                logger.info("=" * 60)
                return True
            else:
                logger.error("\n❌ Falha ao criar live")
                return False
                
        except Exception as e:
            logger.error(f"\n❌ Erro ao criar live: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        logger.error(f"❌ Erro ao conectar: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = test_live_with_account_check()
        if success:
            logger.info("\n✅ Teste concluído com sucesso!")
            logger.info("💡 Agora você pode usar o sistema completo de live!")
            sys.exit(0)
        else:
            logger.error("\n❌ Teste falhou")
            logger.info("\n📋 Dicas:")
            logger.info("   1. Certifique-se de escolher lofiwilson0@gmail.com na autenticação")
            logger.info("   2. Verifique se o live streaming está habilitado nessa conta")
            logger.info("   3. Tente novamente")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Teste interrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n❌ Erro crítico: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

