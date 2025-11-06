#!/usr/bin/env python3
"""
Script para criar vídeo usando áudios da pasta audios/
"""
import os
import sys
from create_lofi_video import create_lofi_video, find_audio_files

def main():
    print("🎬 Criador de Vídeo LOFI com Áudio Personalizado")
    print("=" * 60)
    
    # Verifica se há áudios
    audio_files = find_audio_files("audios")
    
    if not audio_files:
        print("\n❌ Nenhum áudio encontrado na pasta 'audios/'")
        print("\n📋 INSTRUÇÕES:")
        print("1. Baixe um áudio LOFI do YouTube Audio Library")
        print("2. Coloque o arquivo (MP3, WAV, etc) na pasta:")
        print(f"   {os.path.abspath('audios')}")
        print("3. Execute este script novamente")
        print("\n💡 Formatos aceitos: MP3, WAV, M4A, AAC, OGG, FLAC")
        return False
    
    print(f"\n✅ Encontrados {len(audio_files)} áudio(s) na pasta:")
    for i, audio in enumerate(audio_files, 1):
        print(f"   {i}. {os.path.basename(audio)}")
    
    print("\n🎬 Criando vídeo de 30 segundos...")
    print("   (Usando áudio aleatório + imagens da pasta 'images/')")
    
    try:
        video_path = create_lofi_video(
            video_duration=30,
            images_dir="images",
            audios_dir="audios"
        )
        
        print("\n" + "=" * 60)
        print("✅ VÍDEO CRIADO COM SUCESSO!")
        print("=" * 60)
        print(f"📹 Arquivo: {video_path}")
        print(f"📂 Caminho completo: {os.path.abspath(video_path)}")
        print("\n💡 Você pode:")
        print("   • Visualizar o vídeo")
        print("   • Usar no sistema de live")
        print("   • Fazer upload manual")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao criar vídeo: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

