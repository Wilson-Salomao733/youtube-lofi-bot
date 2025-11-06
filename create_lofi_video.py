"""
Script principal para criar vídeos LOFI
Combina frames animados com áudio em um vídeo
"""
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_videoclips
from lofi_generator_ultra import LofiUltraGenerator
import os
import sys
import shutil
import glob


def find_audio_files(audio_dir="audios"):
    """
    Procura arquivos de áudio na pasta especificada
    
    Args:
        audio_dir: Diretório para procurar áudios
        
    Returns:
        Lista de caminhos para arquivos de áudio encontrados
    """
    if not os.path.exists(audio_dir):
        return []
    
    audio_extensions = ['*.mp3', '*.wav', '*.m4a', '*.aac', '*.ogg', '*.flac']
    audio_files = []
    
    for ext in audio_extensions:
        audio_files.extend(glob.glob(os.path.join(audio_dir, ext)))
        audio_files.extend(glob.glob(os.path.join(audio_dir, ext.upper())))
    
    return sorted(audio_files)


def create_lofi_video(video_duration=60, width=1920, height=1080, animated=True, images_dir="images", audios_dir="audios"):
    """
    Cria um vídeo LOFI completo usando APENAS arquivos das pastas (sem gerar nada)
    
    Args:
        video_duration: Duração do vídeo em segundos
        width: Largura do vídeo
        height: Altura do vídeo
        animated: Se True, cria vídeo com movimento/animações
        images_dir: Pasta com imagens PNG/JPG (OBRIGATÓRIA)
        audios_dir: Pasta com áudios MP3/WAV (OBRIGATÓRIA)
    """
    print("🎬 Criando Vídeo LOFI (usando apenas arquivos das pastas)...")
    print("=" * 50)
    
    audio_path = "lofi_temp_audio.wav"
    frames_dir = "lofi_temp_frames"
    
    # Garante que a pasta de frames existe (caminho absoluto)
    frames_dir = os.path.abspath(frames_dir)
    os.makedirs(frames_dir, exist_ok=True)
    
    generator = LofiUltraGenerator()
    
    # Procura áudios na pasta (OBRIGATÓRIO)
    print("\n1️⃣  Procurando áudio...")
    audio_files = find_audio_files(audios_dir)
    
    if not audio_files:
        raise Exception(f"❌ Nenhum áudio encontrado em '{audios_dir}/'! Coloque arquivos MP3/WAV na pasta.")
    
    import random
    selected_audio = random.choice(audio_files)
    print(f"   🎵 Usando áudio: {os.path.basename(selected_audio)}")
    
    # Carrega o áudio
    from moviepy.editor import AudioFileClip
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
    
    if animated:
        print("\n2️⃣  Gerando frames animados...")
        fps = 30
        num_frames = int(video_duration * fps)
        
        # Procura imagens na pasta (OBRIGATÓRIO)
        background_images = generator.find_background_images(images_dir)
        
        if not background_images:
            raise Exception(f"❌ Nenhuma imagem encontrada em '{images_dir}/'! Coloque arquivos PNG/JPG na pasta.")
        
        # Usa imagem aleatória da pasta
        import random
        selected_image = random.choice(background_images)
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
        
        print(f"\n3️⃣  Criando vídeo com {num_frames} frames...")
        
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
        
    else:
        # Modo estático (fallback - não deve ser usado com novo fluxo)
        print("\n2️⃣  Gerando imagem estática...")
        img_path = "lofi_temp_image.png"
        generator.generate_ultra_scene(width=width, height=height, output_path=img_path)
        
        print("\n3️⃣  Criando vídeo...")
        from moviepy.editor import ImageClip
        video_clip = ImageClip(img_path, duration=video_duration)
        audio_clip = AudioFileClip(audio_path)
        video_clip = video_clip.set_audio(audio_clip)
        video_clip = video_clip.resize((width, height))
    
    # Garante que a pasta output existe
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    
    # Nome do arquivo
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_folder, f"lofi_video_{timestamp}.mp4")
    
    # Exporta o vídeo
    print(f"\n4️⃣  Exportando vídeo para: {output_path}")
    print("    ⏳ Isso pode demorar alguns minutos...")
    video_clip.write_videofile(
        output_path,
        fps=30,
        codec='libx264',
        audio_codec='aac',
        bitrate='10M',
        threads=4,
        preset='medium'
    )
    
    # Limpa arquivos temporários
    print("\n🧹 Limpando arquivos temporários...")
    if os.path.exists(audio_path):
        os.remove(audio_path)
    if animated and os.path.exists(frames_dir):
        shutil.rmtree(frames_dir)
        print(f"   ✅ {len(frame_paths)} frames removidas")
    elif not animated and os.path.exists("lofi_temp_image.png"):
        os.remove("lofi_temp_image.png")
    
    print(f"\n✅ Vídeo criado com sucesso: {output_path}")
    return output_path


def loop_video(video_path, target_duration=3600, output_path=None):
    """
    Repete um vídeo curto várias vezes para atingir duração desejada
    
    Args:
        video_path: Caminho do vídeo original (curto)
        target_duration: Duração desejada em segundos
        output_path: Caminho de saída (None = gera automaticamente)
    
    Returns:
        Caminho do vídeo com loop
    """
    from moviepy.editor import VideoFileClip
    from datetime import datetime
    
    print(f"🔄 Criando loop do vídeo: {video_path}")
    print(f"⏱️  Duração desejada: {target_duration} segundos")
    
    # Carrega o vídeo
    video_clip = VideoFileClip(video_path)
    clip_duration = video_clip.duration
    
    if clip_duration >= target_duration:
        print(f"⚠️  Vídeo já tem {clip_duration}s, maior que {target_duration}s")
        return video_path
    
    # Calcula quantas repetições são necessárias
    num_loops = int(target_duration / clip_duration) + 1
    print(f"📊 Repetindo {num_loops} vezes para atingir {target_duration}s")
    
    # Cria lista de clips
    clips = [video_clip] * num_loops
    
    # Concatena todos os clips
    print("🔗 Concatenando vídeos...")
    final_clip = concatenate_videoclips(clips, method="compose")
    
    # Corta para duração exata
    final_clip = final_clip.subclip(0, target_duration)
    
    # Garante que a pasta output existe
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    
    # Nome do arquivo
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_folder, f"lofi_video_looped_{timestamp}.mp4")
    
    # Exporta
    print(f"💾 Exportando vídeo com loop para: {output_path}")
    print("    ⏳ Isso pode demorar alguns minutos...")
    final_clip.write_videofile(
        output_path,
        fps=30,
        codec='libx264',
        audio_codec='aac',
        bitrate='10M',
        threads=4,
        preset='medium'
    )
    
    video_clip.close()
    final_clip.close()
    
    print(f"✅ Vídeo com loop criado: {output_path}")
    return output_path


def create_multiple_videos(num_videos=5, duration=60):
    """
    Cria múltiplos vídeos LOFI automaticamente
    
    Args:
        num_videos: Número de vídeos a criar
        duration: Duração de cada vídeo
    """
    print(f"🎵 Criando {num_videos} vídeos LOFI...")
    print("=" * 50)
    
    videos = []
    for i in range(num_videos):
        print(f"\n📹 Vídeo {i+1}/{num_videos}")
        video_path = create_lofi_video(video_duration=duration)
        videos.append(video_path)
    
    print(f"\n✅ Todos os vídeos criados com sucesso!")
    return videos


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Gerador de Vídeos LOFI")
    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=60,
        help="Duração do vídeo em segundos (padrão: 60)"
    )
    parser.add_argument(
        "--multiple", "-m",
        type=int,
        help="Cria múltiplos vídeos (especifique a quantidade)"
    )
    parser.add_argument(
        "--width", "-w",
        type=int,
        default=1920,
        help="Largura do vídeo (padrão: 1920)"
    )
    parser.add_argument(
        "--height", "-ht",
        type=int,
        default=1080,
        help="Altura do vídeo (padrão: 1080)"
    )
    parser.add_argument(
        "--images-dir", "-i",
        type=str,
        default="images",
        help="Pasta com imagens PNG/JPG para usar como background (padrão: images/)"
    )
    parser.add_argument(
        "--audios-dir", "-a",
        type=str,
        default="audios",
        help="Pasta com áudios MP3/WAV para usar (padrão: audios/, se não encontrar, gera automaticamente)"
    )
    
    args = parser.parse_args()
    
    try:
        if args.multiple:
            create_multiple_videos(num_videos=args.multiple, duration=args.duration)
        else:
            create_lofi_video(
                video_duration=args.duration,
                width=args.width,
                height=args.height,
                images_dir=args.images_dir,
                audios_dir=args.audios_dir
            )
    except KeyboardInterrupt:
        print("\n\n⚠️  Processo cancelado pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro ao criar vídeo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

