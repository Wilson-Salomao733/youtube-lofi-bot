"""
Script para criar Live pública no YouTube (transmitir via OBS com vídeo em loop)
"""
import os
import sys
from datetime import datetime, timedelta
from youtube_uploader import YouTubeUploader
from create_lofi_video import create_lofi_video
import argparse


def create_and_publish_live(video_path=None, title=None, description=None, 
                            scheduled_minutes=10):
    """
    Cria uma live pública no YouTube para transmitir via OBS
    
    Args:
        video_path: Caminho do vídeo de 30s (None = cria um novo)
        title: Título do live
        description: Descrição do live
        scheduled_minutes: Minutos até começar o live
    """
    print("🎬 Criando Live Pública no YouTube")
    print("=" * 60)
    
    # Se não tem vídeo, cria um curto de 30 segundos
    if video_path is None or not os.path.exists(video_path):
        print("\n1️⃣  Criando vídeo curto de 30 segundos...")
        video_path = create_lofi_video(video_duration=30)
        print(f"   ✅ Vídeo criado: {video_path}")
        print(f"   💡 Você usará este vídeo no OBS para fazer loop infinito")
    else:
        print(f"\n1️⃣  Usando vídeo existente: {video_path}")
    
    # Configura título e descrição
    if title is None:
        title = f"LOFI Hip Hop Study Music 🎵 Chill Beats - Live 24/7"
    
    if description is None:
        description = f"""
🎵 Welcome to LOFI Hip Hop Study Music!

Perfect for:
• Studying and focusing 📚
• Working and productivity 💼
• Relaxing and unwinding 🌙
• Meditation and yoga 🧘

This live stream features smooth beats and calming visuals 24/7.

🎨 All visuals and sounds are generated programmatically.
No copyright claims - feel free to use this music.

👉 Subscribe for more LOFI content!
🔔 Turn on notifications for new uploads

Tags: #lofi #study #music #chill #beats #hiphop #focus #live
"""
    
    # Cria uploader
    print("\n2️⃣  Conectando ao YouTube...")
    try:
        uploader = YouTubeUploader()
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        print("\n💡 Dica: Certifique-se de ter configurado as credenciais:")
        print("   1. credentials/credentials.json")
        print("   2. Autorizado o app no Google Cloud Console")
        return None
    
    # Agenda o live
    scheduled_time = datetime.now() + timedelta(minutes=scheduled_minutes)
    print(f"\n3️⃣  Criando live agendado para: {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    broadcast_id, stream_id, stream_key, rtmp_url = uploader.create_live_broadcast(
        title=title,
        scheduled_start_time=scheduled_time,
        description=description,
        privacy_status="public"  # Live pública
    )
    
    if not broadcast_id:
        print("❌ Falha ao criar live")
        return None
    
    print(f"\n✅ Live criado com sucesso!")
    print("=" * 60)
    print(f"🎥 Broadcast ID: {broadcast_id}")
    print(f"📡 Stream ID: {stream_id}")
    print(f"🔗 Link da Live: https://www.youtube.com/watch?v={broadcast_id}")
    print("\n" + "=" * 60)
    print("📺 CONFIGURAÇÃO PARA OBS STUDIO:")
    print("=" * 60)
    
    if stream_key and rtmp_url:
        print(f"\n📍 URL do Servidor RTMP:")
        print(f"   {rtmp_url}")
        print(f"\n🔑 Stream Key:")
        print(f"   {stream_key}")
    else:
        print(f"\n⚠️  Stream Key não encontrada automaticamente.")
        print(f"   Acesse o YouTube Studio para obter:")
        print(f"   https://studio.youtube.com/")
        print(f"   Ir em: Transmissões → Transmitir agora")
    
    print(f"\n📝 Passos para configurar OBS:")
    print(f"   1. Abra OBS Studio")
    print(f"   2. Vá em: Configurações → Transmissão")
    print(f"   3. Serviço: YouTube / YouTube Gaming")
    print(f"   4. Servidor: {rtmp_url or 'Use o do YouTube Studio'}")
    print(f"   5. Chave de transmissão: {stream_key or 'Use a do YouTube Studio'}")
    print(f"\n   6. Adicione o vídeo como fonte:")
    print(f"      - Clique direito em 'Fontes' → Adicionar → Fonte de Mídia")
    print(f"      - Escolha: {video_path}")
    print(f"      - Marque: 'Repetir quando o arquivo terminar'")
    print(f"      - OK!")
    print(f"\n   7. Clique em 'Iniciar transmissão' no OBS")
    print(f"\n✅ Pronto! Sua live estará no ar com o vídeo em loop infinito!")
    print(f"\n🔗 Link da Live: https://www.youtube.com/watch?v={broadcast_id}")
    
    return broadcast_id, stream_id, stream_key, video_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Cria Live Pública no YouTube com vídeo LOFI"
    )
    parser.add_argument(
        "--video", "-v",
        type=str,
        default=None,
        help="Caminho do vídeo de 30s para usar no OBS (None = cria novo)"
    )
    parser.add_argument(
        "--title", "-t",
        type=str,
        default=None,
        help="Título do live (padrão: gerado automaticamente)"
    )
    parser.add_argument(
        "--description",
        type=str,
        default=None,
        help="Descrição do live (padrão: gerada automaticamente)"
    )
    parser.add_argument(
        "--scheduled", "-s",
        type=int,
        default=10,
        help="Minutos até começar o live (padrão: 10)"
    )
    
    args = parser.parse_args()
    
    try:
        create_and_publish_live(
            video_path=args.video,
            title=args.title,
            description=args.description,
            scheduled_minutes=args.scheduled
        )
    except KeyboardInterrupt:
        print("\n\n⚠️  Processo cancelado pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

