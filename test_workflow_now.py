"""
Script para testar o workflow completo AGORA (sem esperar 7h)
"""
import os
import sys
import time
from datetime import datetime
from create_lofi_video import create_lofi_video
from youtube_uploader import YouTubeUploader
import logging

# Configura logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def test_workflow():
    """Testa o fluxo completo: criar vídeo + live + streaming"""
    logger.info("=" * 60)
    logger.info("🧪 TESTE DO WORKFLOW AUTOMATIZADO")
    logger.info("=" * 60)
    
    # 1. Criar vídeo
    logger.info("\n1️⃣  Criando vídeo de 30 segundos...")
    try:
        video_path = create_lofi_video(video_duration=30, images_dir="images", audios_dir="audios")
        logger.info(f"✅ Vídeo criado: {video_path}")
        if not os.path.exists(video_path):
            logger.error(f"❌ Vídeo não encontrado: {video_path}")
            return False
    except Exception as e:
        logger.error(f"❌ Erro ao criar vídeo: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 2. Criar live no YouTube
    logger.info("\n2️⃣  Criando live no YouTube...")
    try:
        uploader = YouTubeUploader()
        if not uploader.youtube:
            logger.error("❌ Falha na autenticação do YouTube")
            return False
        
        title = f"LOFI Hip Hop Study Music 🎵 Chill Beats - Live 24/7 [TESTE]"
        description = f"""
🎵 Welcome to LOFI Hip Hop Study Music!

This is a TEST broadcast to verify the automated system.

Perfect for:
• Studying and focusing 📚
• Working and productivity 💼
• Relaxing and unwinding 🌙
• Meditation and yoga 🧘

This live stream features smooth beats and calming visuals 24/7.

🎨 All visuals and sounds are generated programmatically.
No copyright claims - feel free to use this music.
"""
        
        from datetime import timedelta
        scheduled_time = datetime.now() + timedelta(minutes=2)  # Começa em 2 minutos
        
        logger.info(f"   Agendando para: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        broadcast_id, stream_id, stream_key, rtmp_url = uploader.create_live_broadcast(
            title=title,
            scheduled_start_time=scheduled_time,
            description=description,
            privacy_status="public"
        )
        
        if not broadcast_id:
            logger.error("❌ Falha ao criar live no YouTube")
            return False
        
        logger.info(f"✅ Live criado com sucesso!")
        logger.info(f"   📺 Broadcast ID: {broadcast_id}")
        logger.info(f"   📡 Stream ID: {stream_id}")
        logger.info(f"   🔗 Link: https://www.youtube.com/watch?v={broadcast_id}")
        logger.info(f"   🔑 Stream Key: {stream_key[:20]}..." if stream_key else "   ⚠️  Stream Key não disponível")
        logger.info(f"   📍 RTMP URL: {rtmp_url}" if rtmp_url else "   ⚠️  RTMP URL não disponível")
        
    except Exception as e:
        logger.error(f"❌ Erro ao criar live: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 3. Iniciar streaming com ffmpeg
    logger.info("\n3️⃣  Iniciando streaming com FFmpeg...")
    
    if not stream_key or not rtmp_url:
        logger.error("❌ Stream Key ou RTMP URL não disponíveis")
        logger.info("💡 Você pode iniciar o streaming manualmente com OBS")
        return False
    
    try:
        import subprocess
        
        rtmp_full_url = f"{rtmp_url}/{stream_key}"
        
        logger.info(f"   📍 RTMP URL completa preparada")
        logger.info(f"   🎥 Iniciando FFmpeg em loop...")
        
        ffmpeg_cmd = [
            'ffmpeg',
            '-re',  # Ler no ritmo real
            '-stream_loop', '-1',  # Loop infinito
            '-i', video_path,
            '-c:v', 'libx264',
            '-preset', 'veryfast',
            '-maxrate', '4000k',
            '-bufsize', '8000k',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-f', 'flv',
            '-flvflags', 'no_duration_filesize',
            rtmp_full_url
        ]
        
        logger.info(f"   Executando: ffmpeg -re -stream_loop -1 -i {video_path} ... [RTMP]")
        
        process = subprocess.Popen(
            ffmpeg_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Aguarda um pouco para ver se inicia
        time.sleep(5)
        
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            logger.error(f"❌ FFmpeg parou imediatamente")
            logger.error(f"   Erro: {stderr[:500] if stderr else 'Sem saída de erro'}")
            return False
        
        logger.info("✅ FFmpeg iniciado com sucesso!")
        logger.info("   🎬 Streaming em andamento...")
        logger.info(f"   🔗 Acesse a live: https://www.youtube.com/watch?v={broadcast_id}")
        logger.info("\n" + "=" * 60)
        logger.info("📊 TESTE EM EXECUÇÃO")
        logger.info("=" * 60)
        logger.info("✅ Vídeo criado")
        logger.info("✅ Live criada no YouTube")
        logger.info("✅ Streaming iniciado")
        logger.info("\n💡 O streaming continuará rodando.")
        logger.info("   Para parar, pressione Ctrl+C")
        logger.info(f"\n🔗 Link da Live: https://www.youtube.com/watch?v={broadcast_id}")
        
        # Aguarda até Ctrl+C
        try:
            process.wait()
        except KeyboardInterrupt:
            logger.info("\n\n🛑 Parando streaming...")
            process.terminate()
            process.wait(timeout=10)
            if process.poll() is None:
                process.kill()
            logger.info("✅ Streaming parado")
        
        return True
        
    except FileNotFoundError:
        logger.error("❌ FFmpeg não encontrado no sistema")
        logger.info("💡 Instale com: sudo apt-get install ffmpeg")
        logger.info("   Ou use Docker que já tem ffmpeg incluído")
        return False
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar streaming: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = test_workflow()
        if success:
            logger.info("\n✅ Teste concluído com sucesso!")
            sys.exit(0)
        else:
            logger.error("\n❌ Teste falhou")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("\n\n⚠️  Teste interrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n❌ Erro crítico: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

