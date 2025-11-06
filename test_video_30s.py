#!/usr/bin/env python3
"""
Script para criar e mostrar um vídeo de teste de 30 segundos
ANTES de subir para o YouTube
"""
import os
import sys
from create_lofi_video import create_lofi_video

def main():
    print("=" * 60)
    print("🧪 TESTE DE VÍDEO DE 30 SEGUNDOS")
    print("=" * 60)
    print("\n📋 Este script vai:")
    print("   1. Pegar uma imagem ALEATÓRIA da pasta 'images/'")
    print("   2. Pegar um áudio ALEATÓRIO da pasta 'audios/'")
    print("   3. Criar vídeo de 30 segundos COM ANIMAÇÕES")
    print("   4. Salvar o vídeo para você ver antes de subir")
    print("\n" + "=" * 60)
    
    # Verifica se há arquivos
    from create_lofi_video import find_audio_files
    from lofi_generator_ultra import LofiUltraGenerator
    
    audio_files = find_audio_files("audios")
    generator = LofiUltraGenerator()
    image_files = generator.find_background_images("images")
    
    if not audio_files:
        print("❌ Nenhum áudio encontrado em 'audios/'")
        return False
    
    if not image_files:
        print("❌ Nenhuma imagem encontrada em 'images/'")
        return False
    
    print(f"\n✅ Encontrados:")
    print(f"   • {len(audio_files)} áudio(s)")
    print(f"   • {len(image_files)} imagem(ns)")
    print("\n🎬 Criando vídeo de teste...")
    
    try:
        video_path = create_lofi_video(
            video_duration=30,
            images_dir="images",
            audios_dir="audios"
        )
        
        if not os.path.exists(video_path):
            print(f"❌ Vídeo não foi criado: {video_path}")
            return False
        
        # Mostra informações do vídeo
        file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
        
        print("\n" + "=" * 60)
        print("✅ VÍDEO DE TESTE CRIADO COM SUCESSO!")
        print("=" * 60)
        print(f"📹 Arquivo: {os.path.basename(video_path)}")
        print(f"📂 Caminho completo:")
        print(f"   {os.path.abspath(video_path)}")
        print(f"📊 Tamanho: {file_size:.2f} MB")
        print(f"⏱️  Duração: 30 segundos")
        print("\n💡 Próximos passos:")
        print("   1. Abra o vídeo para ver como ficou")
        print("   2. Se estiver bom, o sistema automatizado vai usar")
        print("   3. Ele criará vídeos assim todos os dias às 7h")
        print("   4. E fará live automática até 19h (7 da noite)")
        print("\n📺 Para ver o vídeo:")
        print(f"   xdg-open {video_path}")
        print("   (ou abra manualmente no seu player)")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao criar vídeo: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

