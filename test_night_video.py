#!/usr/bin/env python3
"""
Script de teste para criar vídeo noturno
"""
import sys
from create_night_video import create_night_video, get_categories, select_random_category

print("🌙 Teste de Criação de Vídeo Noturno")
print("=" * 50)

# Verifica categorias disponíveis
print("\n📂 Verificando categorias disponíveis...")
categories = get_categories()
print(f"   Categorias encontradas: {categories}")

if not categories:
    print("❌ Nenhuma categoria encontrada!")
    print("   Verifique se as pastas 'imagens noite' e 'audio_noite' existem")
    sys.exit(1)

# Seleciona categoria
category = select_random_category()
print(f"\n🎲 Categoria selecionada: {category}")

# Cria vídeo de teste (10 segundos para teste rápido)
print(f"\n🎬 Criando vídeo de teste (10 segundos)...")
try:
    video_path = create_night_video(
        video_duration=10,  # 10 segundos para teste rápido
        category=category
    )
    print(f"\n✅ SUCESSO! Vídeo criado: {video_path}")
except Exception as e:
    print(f"\n❌ ERRO: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

