#!/usr/bin/env python3
"""
Script para configurar stream_key manualmente
Use uma das keys que você já tem para todas as lives
"""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(__file__))

def main():
    print("=" * 60)
    print("🔑 CONFIGURAR STREAM KEY PERMANENTE")
    print("=" * 60)
    print()
    print("Você tem 3 stream_keys criadas:")
    print("  1. exxa-sfyy-sy27-hvm3-58sb")
    print("  2. 45ud-7dwd-dqfe-urcc-er5f")
    print("  3. j2ej-v13s-tbbz-zy7w-e7wk")
    print()
    print("Escolha UMA para usar em TODAS as lives:")
    print()
    
    choice = input("Digite o número (1, 2 ou 3) ou cole a key completa: ").strip()
    
    stream_keys = {
        '1': 'exxa-sfyy-sy27-hvm3-58sb',
        '2': '45ud-7dwd-dqfe-urcc-er5f',
        '3': 'j2ej-v13s-tbbz-zy7w-e7wk'
    }
    
    if choice in stream_keys:
        stream_key = stream_keys[choice]
    elif choice in stream_keys.values():
        stream_key = choice
    else:
        print("❌ Opção inválida!")
        sys.exit(1)
    
    print()
    print(f"✅ Stream Key selecionada: {stream_key}")
    print()
    
    # Precisamos do stream_id também
    print("📡 Para obter o stream_id, você precisa:")
    print("   1. Acessar: https://studio.youtube.com/")
    print("   2. Ir em: Conteúdo → Transmissões")
    print("   3. Encontrar o stream que tem essa key")
    print("   4. O stream_id aparece na URL ou nos detalhes")
    print()
    
    stream_id = input("Digite o Stream ID (ou deixe vazio para criar novo): ").strip()
    
    if not stream_id:
        print()
        print("🆕 Criando novo stream permanente...")
        try:
            from youtube_uploader import YouTubeUploader
            uploader = YouTubeUploader()
            stream_id, _, rtmp_url = uploader.get_or_create_permanent_stream()
            
            if stream_id:
                print(f"✅ Stream criado: {stream_id}")
                # Atualiza com a key fornecida
                config = {
                    'stream_id': stream_id,
                    'stream_key': stream_key,
                    'rtmp_url': rtmp_url or 'rtmp://a.rtmp.youtube.com/live2',
                    'created_at': __import__('datetime').datetime.now().isoformat()
                }
            else:
                print("❌ Falha ao criar stream")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Erro: {e}")
            sys.exit(1)
    else:
        rtmp_url = input("Digite o RTMP URL (ou Enter para padrão): ").strip()
        if not rtmp_url:
            rtmp_url = 'rtmp://a.rtmp.youtube.com/live2'
        
        config = {
            'stream_id': stream_id,
            'stream_key': stream_key,
            'rtmp_url': rtmp_url,
            'created_at': __import__('datetime').datetime.now().isoformat()
        }
    
    # Salva configuração
    config_file = 'credentials/stream_config.json'
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print()
    print("=" * 60)
    print("✅ STREAM KEY CONFIGURADA COM SUCESSO!")
    print("=" * 60)
    print()
    print(f"📡 Stream ID: {config['stream_id']}")
    print(f"🔑 Stream Key: {config['stream_key']}")
    print(f"📍 RTMP URL: {config['rtmp_url']}")
    print()
    print(f"💾 Configuração salva em: {config_file}")
    print()
    print("♻️  Esta key será usada para TODAS as lives criadas!")
    print("=" * 60)

if __name__ == "__main__":
    main()

