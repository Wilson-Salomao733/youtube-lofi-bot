#!/usr/bin/env python3
"""
Script rápido para criar um vídeo LOFI
Use este para começar rapidamente
"""

from create_lofi_video import create_lofi_video

if __name__ == "__main__":
    print("🎵 Quick Start - Gerador de Vídeo LOFI")
    print("=" * 50)
    
    print("\nCriando vídeo LOFI de 60 segundos...")
    
    try:
        video_path = create_lofi_video(video_duration=60)
        print(f"\n✨ Pronto! Vídeo criado: {video_path}")
        print("\nPróximos passos:")
        print("1. Faça upload no YouTube")
        print("2. Adicione tags: LOFI, hip hop, study, chill")
        print("3. Use títulos como 'LOFI Hip Hop Mix'")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("\nVerifique se:")
        print("1. Instalou todas as dependências: pip install -r requirements.txt")
        print("2. Tem FFmpeg instalado no sistema")
        print("3. Tem espaço em disco suficiente")

