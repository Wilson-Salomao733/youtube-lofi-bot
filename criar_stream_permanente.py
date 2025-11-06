#!/usr/bin/env python3
"""
Script para criar stream permanente manualmente
Este stream será reutilizado para todas as lives
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from youtube_uploader import YouTubeUploader

def main():
    print("=" * 60)
    print("🔑 CRIANDO STREAM PERMANENTE")
    print("=" * 60)
    print()
    print("Este stream será reutilizado para TODAS as lives criadas.")
    print("O stream_key será o MESMO para todas as lives.")
    print()
    
    try:
        uploader = YouTubeUploader()
        
        stream_id, stream_key, rtmp_url = uploader.get_or_create_permanent_stream()
        
        if stream_id and stream_key and rtmp_url:
            print()
            print("=" * 60)
            print("✅ STREAM PERMANENTE CRIADO COM SUCESSO!")
            print("=" * 60)
            print()
            print(f"📡 Stream ID: {stream_id}")
            print(f"🔑 Stream Key: {stream_key}")
            print(f"📍 RTMP URL: {rtmp_url}")
            print()
            print("💾 Configuração salva em: credentials/stream_config.json")
            print()
            print("♻️  Este stream_key será usado para TODAS as lives criadas!")
            print("=" * 60)
        else:
            print()
            print("=" * 60)
            print("⚠️  STREAM CRIADO MAS STREAM_KEY NÃO DISPONÍVEL")
            print("=" * 60)
            print()
            print("💡 O YouTube pode levar alguns minutos para disponibilizar o stream_key.")
            print("💡 Tente novamente em alguns minutos ou obtenha manualmente no YouTube Studio:")
            print("   https://studio.youtube.com/")
            print()
            if stream_id:
                print(f"📡 Stream ID criado: {stream_id}")
                print("💡 Você pode obter o stream_key manualmente e salvar em:")
                print("   credentials/stream_config.json")
                print()
                print("   Formato do arquivo:")
                print("   {")
                print(f'     "stream_id": "{stream_id}",')
                print('     "stream_key": "SUA_KEY_AQUI",')
                print('     "rtmp_url": "rtmp://a.rtmp.youtube.com/live2"')
                print("   }")
            print("=" * 60)
            
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ ERRO AO CRIAR STREAM PERMANENTE")
        print("=" * 60)
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()

