"""
Script para testar APENAS a criação de live no YouTube
(sem criar vídeo, sem streaming - só testar a API)
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

def test_live_creation():
    """Testa apenas a criação de live no YouTube"""
    logger.info("=" * 60)
    logger.info("🧪 TESTE DE CRIAÇÃO DE LIVE NO YOUTUBE")
    logger.info("=" * 60)
    
    # Conectar ao YouTube
    logger.info("\n1️⃣  Conectando ao YouTube...")
    try:
        uploader = YouTubeUploader()
        if not uploader.youtube:
            logger.error("❌ Falha na autenticação do YouTube")
            return False
        logger.info("✅ Conectado com sucesso!")
    except Exception as e:
        logger.error(f"❌ Erro ao conectar: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Tentar criar live
    logger.info("\n2️⃣  Tentando criar live de teste...")
    
    title = f"LOFI Test Live - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    description = "Teste de criação de live automatizada"
    scheduled_time = datetime.now() + timedelta(minutes=5)
    
    logger.info(f"   📝 Título: {title}")
    logger.info(f"   ⏰ Agendado para: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
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
            logger.info("\n💡 Verifique as mensagens acima para mais detalhes")
            return False
            
    except Exception as e:
        logger.error(f"\n❌ Erro ao criar live: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = test_live_creation()
        if success:
            logger.info("\n✅ Teste concluído com sucesso!")
            logger.info("💡 Agora você pode usar o sistema completo de live!")
            sys.exit(0)
        else:
            logger.error("\n❌ Teste falhou")
            logger.info("\n📋 Próximos passos:")
            logger.info("   1. Habilite live streaming no seu canal do YouTube")
            logger.info("   2. Verifique se tem pelo menos 1,000 inscritos")
            logger.info("   3. Ou verifique seu canal no YouTube")
            logger.info("   4. Tente novamente depois")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Teste interrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n❌ Erro crítico: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

