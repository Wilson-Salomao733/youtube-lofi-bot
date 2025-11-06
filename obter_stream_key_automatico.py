#!/usr/bin/env python3
"""
Script para obter stream_key automaticamente de um stream existente
Tenta várias vezes até conseguir o stream_key
"""
import sys
import os
import time
sys.path.insert(0, os.path.dirname(__file__))

from youtube_uploader import YouTubeUploader

def obter_stream_key(stream_id, max_tentativas=30, delay=20):
    """
    Tenta obter stream_key de um stream com múltiplas tentativas
    
    Args:
        stream_id: ID do stream
        max_tentativas: Número máximo de tentativas
        delay: Delay entre tentativas (segundos)
    
    Returns:
        (stream_key, rtmp_url) ou (None, None)
    """
    uploader = YouTubeUploader()
    
    print(f"🔍 Tentando obter stream_key para: {stream_id}")
    print(f"⏱️  Pode levar até {max_tentativas * delay / 60:.1f} minutos...")
    print()
    
    for attempt in range(1, max_tentativas + 1):
        try:
            stream_info = uploader.youtube.liveStreams().list(
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
                    print(f"✅ Stream Key obtido na tentativa {attempt}/{max_tentativas}!")
                    print(f"🔑 Stream Key: {stream_key}")
                    print(f"📍 RTMP URL: {rtmp_url}")
                    return stream_key, rtmp_url
                else:
                    if attempt % 3 == 0:
                        print(f"⏳ Tentativa {attempt}/{max_tentativas}: Stream Key ainda não disponível...")
                    if attempt < max_tentativas:
                        time.sleep(delay)
            else:
                print(f"❌ Stream não encontrado: {stream_id}")
                return None, None
                
        except Exception as e:
            if attempt % 3 == 0:
                print(f"⚠️  Erro na tentativa {attempt}/{max_tentativas}: {e}")
            if attempt < max_tentativas:
                time.sleep(delay)
    
    print(f"❌ Stream Key não disponível após {max_tentativas} tentativas")
    print("💡 O YouTube pode levar vários minutos para disponibilizar o stream_key")
    print("💡 Tente novamente mais tarde ou obtenha manualmente no YouTube Studio")
    return None, None

def main():
    import json
    
    # Tenta obter do arquivo de config
    config_file = 'credentials/stream_config.json'
    stream_id = None
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                stream_id = config.get('stream_id')
                existing_key = config.get('stream_key')
                
                if existing_key:
                    print(f"✅ Stream Key já existe no arquivo: {existing_key[:30]}...")
                    print(f"💡 Se quiser obter novamente, delete o arquivo ou forneça um stream_id diferente")
                    return
        except:
            pass
    
    if not stream_id:
        print("📡 Forneça o Stream ID:")
        stream_id = input("Stream ID: ").strip()
    
    if not stream_id:
        print("❌ Stream ID não fornecido")
        sys.exit(1)
    
    stream_key, rtmp_url = obter_stream_key(stream_id)
    
    if stream_key and rtmp_url:
        # Salva no arquivo de config
        config = {
            'stream_id': stream_id,
            'stream_key': stream_key,
            'rtmp_url': rtmp_url,
            'created_at': __import__('datetime').datetime.now().isoformat()
        }
        
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print()
        print("💾 Stream Key salvo em: credentials/stream_config.json")
        print("♻️  Este stream_key será usado para todas as lives!")

if __name__ == "__main__":
    main()

