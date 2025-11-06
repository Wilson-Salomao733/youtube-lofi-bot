#!/usr/bin/env python3
"""
Script para configurar stream_key fixo
Use uma das suas 3 keys fixas
"""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(__file__))

def main():
    print("=" * 60)
    print("🔑 CONFIGURAR STREAM KEY FIXO")
    print("=" * 60)
    print()
    print("Você tem 3 stream_keys fixas:")
    print("  1. exxa-sfyy-sy27-hvm3-58sb")
    print("  2. 45ud-7dwd-dqfe-urcc-er5f")
    print("  3. j2ej-v13s-tbbz-zy7w-e7wk")
    print()
    print("Escolha UMA para usar em TODAS as lives:")
    print()
    
    choice = input("Digite o número (1, 2 ou 3): ").strip()
    
    stream_keys = {
        '1': 'exxa-sfyy-sy27-hvm3-58sb',
        '2': '45ud-7dwd-dqfe-urcc-er5f',
        '3': 'j2ej-v13s-tbbz-zy7w-e7wk'
    }
    
    if choice not in stream_keys:
        print("❌ Opção inválida! Use 1, 2 ou 3")
        sys.exit(1)
    
    stream_key = stream_keys[choice]
    
    print()
    print(f"✅ Stream Key selecionada: {stream_key}")
    print()
    
    # Precisamos do stream_id também
    print("📡 Para obter o stream_id:")
    print("   1. Acesse: https://studio.youtube.com/")
    print("   2. Vá em: Conteúdo → Transmissões")
    print("   3. Encontre o stream que tem essa key")
    print("   4. O stream_id aparece na URL ou nos detalhes")
    print()
    print("   OU deixe vazio para usar o stream_id atual do arquivo")
    print()
    
    stream_id = input("Digite o Stream ID (ou Enter para manter atual): ").strip()
    
    # Carrega config atual se existir
    config_file = 'credentials/stream_config.json'
    current_stream_id = None
    
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                current_config = json.load(f)
                current_stream_id = current_config.get('stream_id')
        except:
            pass
    
    if not stream_id:
        if current_stream_id:
            stream_id = current_stream_id
            print(f"✅ Usando stream_id atual: {stream_id}")
        else:
            print("❌ Nenhum stream_id encontrado! Você precisa fornecer um.")
            sys.exit(1)
    
    rtmp_url = input("Digite o RTMP URL (ou Enter para padrão): ").strip()
    if not rtmp_url:
        rtmp_url = 'rtmp://a.rtmp.youtube.com/live2'
    
    config = {
        'stream_id': stream_id,
        'stream_key': stream_key,
        'rtmp_url': rtmp_url,
        'created_at': __import__('datetime').datetime.now().isoformat(),
        'is_fixed_key': True  # Marca como key fixa
    }
    
    # Salva configuração
    os.makedirs(os.path.dirname(config_file), exist_ok=True)
    
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print()
    print("=" * 60)
    print("✅ STREAM KEY FIXO CONFIGURADO COM SUCESSO!")
    print("=" * 60)
    print()
    print(f"📡 Stream ID: {config['stream_id']}")
    print(f"🔑 Stream Key: {config['stream_key']}")
    print(f"📍 RTMP URL: {config['rtmp_url']}")
    print()
    print(f"💾 Configuração salva em: {config_file}")
    print()
    print("♻️  Esta key será usada para TODAS as lives criadas!")
    print("✅ Não precisa mais obter manualmente - o sistema usa automaticamente!")
    print("=" * 60)

if __name__ == "__main__":
    main()

