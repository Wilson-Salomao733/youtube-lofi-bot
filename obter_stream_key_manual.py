#!/usr/bin/env python3
"""
Script para obter Stream Key manualmente de uma live existente
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from youtube_uploader import YouTubeUploader

def obter_stream_key(broadcast_id):
    """Obtém stream_key de uma live existente"""
    print("=" * 60)
    print("🔑 OBTENDO STREAM KEY DE LIVE EXISTENTE")
    print("=" * 60)
    
    try:
        uploader = YouTubeUploader()
        
        # Busca informações do broadcast
        broadcast_info = uploader.youtube.liveBroadcasts().list(
            part='snippet,contentDetails,status',
            id=broadcast_id
        ).execute()
        
        if not broadcast_info.get('items'):
            print(f"❌ Broadcast {broadcast_id} não encontrado")
            return None
        
        # Obtém stream_id do broadcast
        content_details = broadcast_info['items'][0].get('contentDetails', {})
        stream_id = content_details.get('boundStreamId')
        
        if not stream_id:
            print("❌ Stream ID não encontrado no broadcast")
            return None
        
        print(f"✅ Stream ID encontrado: {stream_id}")
        
        # Busca informações do stream incluindo stream_key
        stream_info = uploader.youtube.liveStreams().list(
            part='cdn,status,snippet',
            id=stream_id
        ).execute()
        
        if not stream_info.get('items'):
            print("❌ Stream não encontrado")
            return None
        
        item = stream_info['items'][0]
        cdn_info = item.get('cdn', {})
        ingestion_info = cdn_info.get('ingestionInfo', {})
        stream_key = ingestion_info.get('streamKey', '')
        rtmp_url = ingestion_info.get('ingestionAddress', '')
        
        print("\n" + "=" * 60)
        print("✅ INFORMAÇÕES DO STREAM")
        print("=" * 60)
        print(f"📡 Stream ID: {stream_id}")
        print(f"📍 RTMP URL: {rtmp_url}")
        print(f"🔑 Stream Key: {stream_key}")
        
        if stream_key and rtmp_url:
            print("\n" + "=" * 60)
            print("🎥 COMANDO FFMPEG COMPLETO")
            print("=" * 60)
            print(f"ffmpeg -re -stream_loop -1 -i SEU_VIDEO.mp4 \\")
            print(f"  -c:v libx264 -preset veryfast -maxrate 4000k -bufsize 8000k \\")
            print(f"  -c:a aac -b:a 128k -f flv \\")
            print(f"  {rtmp_url}/{stream_key}")
            print("=" * 60)
            return stream_key, rtmp_url
        else:
            print("\n⚠️  Stream Key ou RTMP URL não disponíveis")
            print("💡 Tente obter manualmente do YouTube Studio:")
            print(f"   https://studio.youtube.com/video/{broadcast_id}/edit")
            return None
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python obter_stream_key_manual.py <BROADCAST_ID>")
        print("\nExemplo:")
        print("  python obter_stream_key_manual.py 27vGJLO4WeA")
        print("\n💡 Para encontrar o Broadcast ID, veja os logs:")
        print("   docker logs lofi-live-bot | grep 'Live criada'")
        sys.exit(1)
    
    broadcast_id = sys.argv[1]
    obter_stream_key(broadcast_id)

