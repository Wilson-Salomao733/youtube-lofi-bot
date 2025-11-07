"""
Script para criar vídeos noturnos com sons da natureza
Combina imagem e áudio da mesma categoria (Chuva, Fogueira, etc)
"""
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips
from lofi_generator_ultra import LofiUltraGenerator
import os
import sys
import shutil
import glob
import random


def get_categories(images_dir="imagens noite", audios_dir="audio_noite"):
    """
    Obtém lista de categorias disponíveis (pastas que existem em ambos os diretórios)
    
    Returns:
        Lista de nomes de categorias disponíveis
    """
    if not os.path.exists(images_dir) or not os.path.exists(audios_dir):
        return []
    
    # Lista categorias em imagens
    image_categories = [d for d in os.listdir(images_dir) 
                        if os.path.isdir(os.path.join(images_dir, d))]
    
    # Lista categorias em áudios
    audio_categories = [d for d in os.listdir(audios_dir) 
                       if os.path.isdir(os.path.join(audios_dir, d))]
    
    # Retorna apenas categorias que existem em ambos
    categories = list(set(image_categories) & set(audio_categories))
    return sorted(categories)


def select_random_category(images_dir="imagens noite", audios_dir="audio_noite"):
    """
    Seleciona uma categoria aleatória que tenha imagens e áudios
    
    Returns:
        Nome da categoria selecionada ou None
    """
    categories = get_categories(images_dir, audios_dir)
    if not categories:
        return None
    return random.choice(categories)


def find_images_in_category(category, images_dir="imagens noite"):
    """
    Encontra todas as imagens de uma categoria específica
    
    Args:
        category: Nome da categoria (ex: "Chuva", "Fogueira")
        images_dir: Diretório base das imagens
        
    Returns:
        Lista de caminhos para imagens
    """
    category_path = os.path.join(images_dir, category)
    if not os.path.exists(category_path):
        return []
    
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
    images = []
    
    for ext in image_extensions:
        images.extend(glob.glob(os.path.join(category_path, ext)))
    
    return sorted(images)


def find_audios_in_category(category, audios_dir="audio_noite"):
    """
    Encontra todos os áudios de uma categoria específica
    
    Args:
        category: Nome da categoria (ex: "Chuva", "Fogueira")
        audios_dir: Diretório base dos áudios
        
    Returns:
        Lista de caminhos para áudios
    """
    category_path = os.path.join(audios_dir, category)
    if not os.path.exists(category_path):
        return []
    
    audio_extensions = ['*.mp3', '*.wav', '*.m4a', '*.aac', '*.ogg', '*.flac']
    audios = []
    
    for ext in audio_extensions:
        audios.extend(glob.glob(os.path.join(category_path, ext)))
        audios.extend(glob.glob(os.path.join(category_path, ext.upper())))
    
    return sorted(audios)


def create_night_video(video_duration=60, width=1920, height=1080, 
                      images_dir="imagens noite", audios_dir="audio_noite",
                      category=None):
    """
    Cria um vídeo noturno combinando imagem e áudio da mesma categoria
    
    Args:
        video_duration: Duração do vídeo em segundos
        width: Largura do vídeo
        height: Altura do vídeo
        images_dir: Pasta base com imagens por categoria
        audios_dir: Pasta base com áudios por categoria
        category: Categoria específica (None = seleciona aleatória)
    
    Returns:
        Caminho do vídeo criado
    """
    print("🌙 Criando Vídeo Noturno (Sons da Natureza)...")
    print("=" * 50)
    
    audio_path = "lofi_temp_audio.wav"
    frames_dir = "lofi_temp_frames"
    
    # Garante que a pasta de frames existe (caminho absoluto)
    frames_dir = os.path.abspath(frames_dir)
    os.makedirs(frames_dir, exist_ok=True)
    
    generator = LofiUltraGenerator()
    
    # Seleciona categoria
    if category is None:
        category = select_random_category(images_dir, audios_dir)
        if category is None:
            raise Exception(f"❌ Nenhuma categoria encontrada! Verifique as pastas '{images_dir}' e '{audios_dir}'")
    
    print(f"\n📂 Categoria selecionada: {category}")
    
    # Procura imagens da categoria
    print(f"\n1️⃣  Procurando imagens na categoria '{category}'...")
    image_files = find_images_in_category(category, images_dir)
    
    if not image_files:
        raise Exception(f"❌ Nenhuma imagem encontrada em '{images_dir}/{category}/'!")
    
    selected_image = random.choice(image_files)
    print(f"   🖼️  Usando imagem: {os.path.basename(selected_image)}")
    
    # Procura áudios da categoria
    print(f"\n2️⃣  Procurando áudios na categoria '{category}'...")
    audio_files = find_audios_in_category(category, audios_dir)
    
    if not audio_files:
        raise Exception(f"❌ Nenhum áudio encontrado em '{audios_dir}/{category}/'!")
    
    selected_audio = random.choice(audio_files)
    print(f"   🎵 Usando áudio: {os.path.basename(selected_audio)}")
    
    # Carrega o áudio
    audio_clip = AudioFileClip(selected_audio)
    print(f"   ⏱️  Duração do áudio: {audio_clip.duration:.1f}s")
    
    # Se o áudio for maior que o vídeo, CORTA (não faz loop)
    if audio_clip.duration > video_duration:
        print(f"   ✂️  Cortando áudio para {video_duration}s...")
        audio_clip = audio_clip.subclip(0, video_duration)
    # Se o áudio for menor, faz loop
    elif audio_clip.duration < video_duration:
        print(f"   🔁 Áudio ({audio_clip.duration:.1f}s) menor que vídeo ({video_duration}s), fazendo loop...")
        from moviepy.editor import concatenate_audioclips
        loops_needed = int(video_duration / audio_clip.duration) + 1
        audio_clip = concatenate_audioclips([audio_clip] * loops_needed)
        audio_clip = audio_clip.subclip(0, video_duration)
    
    # Salva temporariamente
    print("   💾 Processando áudio...")
    audio_clip.write_audiofile(audio_path, logger=None, verbose=False)
    audio_clip.close()
    
    # Gera frames animados
    print(f"\n3️⃣  Gerando frames animados...")
    fps = 30
    num_frames = int(video_duration * fps)
    
    print(f"   🖼️  Usando imagem: {os.path.basename(selected_image)}")
    
    # Gera frames animadas a partir da imagem
    frame_paths, scene_type = generator.generate_animated_frames(
        width=width,
        height=height,
        num_frames=num_frames,
        fps=fps,
        output_dir=frames_dir,
        base_image_path=selected_image
    )
    
    print(f"\n4️⃣  Criando vídeo com {num_frames} frames...")
    
    # Verifica e filtra frames corrompidas
    print("   🔍 Verificando frames...")
    valid_frames = []
    for frame_path in frame_paths:
        try:
            from PIL import Image
            # Tenta abrir e verificar a imagem
            with Image.open(frame_path) as img:
                img.verify()  # Verifica se a imagem não está corrompida
            # Reabre para uso (verify fecha o arquivo)
            with Image.open(frame_path) as img:
                img.load()  # Carrega completamente
            valid_frames.append(frame_path)
        except Exception as e:
            print(f"   ⚠️  Frame corrompida ignorada: {os.path.basename(frame_path)}")
            continue
    
    if not valid_frames:
        raise Exception("Nenhuma frame válida encontrada! Verifique as imagens.")
    
    if len(valid_frames) < len(frame_paths):
        print(f"   ℹ️  Usando {len(valid_frames)}/{len(frame_paths)} frames válidas")
    
    # Configura PIL para ignorar arquivos truncados durante o carregamento
    from PIL import ImageFile
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    
    # Cria clip de vídeo a partir das frames válidas
    print("   🎬 Criando vídeo a partir das frames...")
    video_clip = ImageSequenceClip(valid_frames, fps=fps)
    
    # Carrega áudio
    audio_clip = AudioFileClip(audio_path)
    
    # Sincroniza áudio com vídeo
    if audio_clip.duration < video_clip.duration:
        # Loop do áudio se necessário
        from moviepy.editor import concatenate_audioclips
        loops_needed = int(video_clip.duration / audio_clip.duration) + 1
        audio_clip = concatenate_audioclips([audio_clip] * loops_needed)
    
    audio_clip = audio_clip.subclip(0, video_clip.duration)
    video_clip = video_clip.set_audio(audio_clip)
    
    # Garante que a pasta output existe
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    
    # Nome do arquivo
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_folder, f"night_video_{category.lower().replace(' ', '_')}_{timestamp}.mp4")
    
    # Salva vídeo
    print(f"\n5️⃣  Salvando vídeo: {output_path}")
    print("   ⏳ Isso pode levar alguns minutos...")
    video_clip.write_videofile(
        output_path,
        fps=fps,
        codec='libx264',
        audio_codec='aac',
        bitrate='8000k',
        preset='medium',
        logger=None,
        verbose=False
    )
    
    # Limpa recursos
    video_clip.close()
    audio_clip.close()
    
    # Limpa arquivos temporários
    try:
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(frames_dir):
            shutil.rmtree(frames_dir)
    except:
        pass
    
    print(f"\n✅ Vídeo criado com sucesso!")
    print(f"   📁 {output_path}")
    print(f"   📂 Categoria: {category}")
    print(f"   ⏱️  Duração: {video_duration}s")
    
    return output_path


if __name__ == "__main__":
    # Teste
    try:
        video_path = create_night_video(video_duration=30)
        print(f"\n🎉 Sucesso! Vídeo salvo em: {video_path}")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

