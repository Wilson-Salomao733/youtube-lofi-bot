"""
Módulo centralizado para criação de vídeos
Suporta fluxo de manhã (LOFI) e noite (Sons da Natureza)
"""
import os
import sys
import shutil
import glob
import random
import json
import time
from datetime import datetime
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_audioclips
from lofi_generator_ultra import LofiUltraGenerator


class VideoCreator:
    """Criador de vídeos unificado para manhã e noite"""
    
    def __init__(self):
        self.generator = LofiUltraGenerator()
    
    def find_audio_files(self, audio_dir):
        """Encontra arquivos de áudio em um diretório"""
        if not os.path.exists(audio_dir):
            return []
        
        audio_extensions = ['*.mp3', '*.wav', '*.m4a', '*.aac', '*.ogg', '*.flac']
        audio_files = []
        
        for ext in audio_extensions:
            audio_files.extend(glob.glob(os.path.join(audio_dir, ext)))
            audio_files.extend(glob.glob(os.path.join(audio_dir, ext.upper())))
        
        return sorted(audio_files)
    
    def find_images_in_dir(self, images_dir):
        """Encontra imagens em um diretório (sem subpastas)"""
        if not os.path.exists(images_dir):
            return []
        
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(glob.glob(os.path.join(images_dir, ext)))
            image_files.extend(glob.glob(os.path.join(images_dir, ext.upper())))
        
        return sorted(image_files)
    
    def get_categories(self, images_dir, audios_dir):
        """Obtém categorias disponíveis (pastas que existem em ambos os diretórios)"""
        if not os.path.exists(images_dir) or not os.path.exists(audios_dir):
            return []
        
        image_categories = [d for d in os.listdir(images_dir) 
                           if os.path.isdir(os.path.join(images_dir, d))]
        audio_categories = [d for d in os.listdir(audios_dir) 
                           if os.path.isdir(os.path.join(audios_dir, d))]
        
        categories = list(set(image_categories) & set(audio_categories))
        return sorted(categories)
    
    def find_images_in_category(self, category, images_dir):
        """Encontra imagens de uma categoria específica"""
        category_path = os.path.join(images_dir, category)
        if not os.path.exists(category_path):
            return []
        
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']
        images = []
        
        for ext in image_extensions:
            images.extend(glob.glob(os.path.join(category_path, ext)))
        
        return sorted(images)
    
    def find_audios_in_category(self, category, audios_dir):
        """Encontra áudios de uma categoria específica"""
        category_path = os.path.join(audios_dir, category)
        if not os.path.exists(category_path):
            return []
        
        audio_extensions = ['*.mp3', '*.wav', '*.m4a', '*.aac', '*.ogg', '*.flac']
        audios = []
        
        for ext in audio_extensions:
            audios.extend(glob.glob(os.path.join(category_path, ext)))
            audios.extend(glob.glob(os.path.join(category_path, ext.upper())))
        
        return sorted(audios)
    
    def select_image_with_history(self, images, images_dir):
        """Seleciona imagem evitando repetições recentes"""
        history_file = os.path.join(images_dir, '.image_history.json')
        used_images = []
        
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    history = json.load(f)
                    used_images = history.get('used_images', [])
            except:
                used_images = []
        
        # Filtra imagens já usadas recentemente (últimas 5)
        available_images = [img for img in images if img not in used_images[-5:]]
        
        if not available_images:
            available_images = images
            used_images = []
        
        selected_image = random.choice(available_images)
        
        # Atualiza histórico
        used_images.append(selected_image)
        if len(used_images) > 10:
            used_images = used_images[-10:]
        
        try:
            with open(history_file, 'w') as f:
                json.dump({'used_images': used_images}, f, indent=2)
        except:
            pass
        
        return selected_image
    
    def create_morning_video(self, video_duration=30, images_dir="images", audios_dir="audios"):
        """
        Cria vídeo LOFI para o fluxo da manhã
        
        Args:
            video_duration: Duração do vídeo em segundos
            images_dir: Pasta com imagens
            audios_dir: Pasta com áudios
        
        Returns:
            Caminho do vídeo criado
        """
        print("🎬 Criando Vídeo LOFI (Manhã)...")
        print("=" * 50)
        
        audio_path = "lofi_temp_audio.wav"
        frames_dir = "lofi_temp_frames"
        frames_dir = os.path.abspath(frames_dir)
        os.makedirs(frames_dir, exist_ok=True)
        
        # Procura áudios
        print("\n1️⃣  Procurando áudio...")
        audio_files = self.find_audio_files(audios_dir)
        
        if not audio_files:
            raise Exception(f"❌ Nenhum áudio encontrado em '{audios_dir}/'!")
        
        selected_audio = random.choice(audio_files)
        print(f"   🎵 Usando áudio: {os.path.basename(selected_audio)}")
        
        # Processa áudio
        audio_clip = AudioFileClip(selected_audio)
        print(f"   ⏱️  Duração do áudio: {audio_clip.duration:.1f}s")
        
        if audio_clip.duration > video_duration:
            print(f"   ✂️  Cortando áudio para {video_duration}s...")
            audio_clip = audio_clip.subclip(0, video_duration)
        elif audio_clip.duration < video_duration:
            print(f"   🔁 Áudio menor que vídeo, fazendo loop...")
            loops_needed = int(video_duration / audio_clip.duration) + 1
            audio_clip = concatenate_audioclips([audio_clip] * loops_needed)
            audio_clip = audio_clip.subclip(0, video_duration)
        
        print("   💾 Processando áudio...")
        audio_clip.write_audiofile(audio_path, logger=None, verbose=False)
        audio_clip.close()
        
        # Gera frames
        print("\n2️⃣  Gerando frames animados...")
        fps = 30
        num_frames = int(video_duration * fps)
        
        background_images = self.find_images_in_dir(images_dir)
        
        if not background_images:
            raise Exception(f"❌ Nenhuma imagem encontrada em '{images_dir}/'!")
        
        selected_image = self.select_image_with_history(background_images, images_dir)
        print(f"   🖼️  Usando imagem: {os.path.basename(selected_image)}")
        print(f"   📊 Total de imagens disponíveis: {len(background_images)}")
        
        # Gera frames animadas
        frame_paths, scene_type = self.generator.generate_animated_frames(
            width=1920,
            height=1080,
            num_frames=num_frames,
            fps=fps,
            output_dir=frames_dir,
            base_image_path=selected_image
        )
        
        print(f"\n3️⃣  Criando vídeo com {num_frames} frames...")
        
        # Valida frames
        print("   🔍 Verificando frames...")
        valid_frames = []
        for frame_path in frame_paths:
            try:
                from PIL import Image
                with Image.open(frame_path) as img:
                    img.verify()
                with Image.open(frame_path) as img:
                    img.load()
                valid_frames.append(frame_path)
            except Exception as e:
                print(f"   ⚠️  Frame corrompida ignorada: {os.path.basename(frame_path)}")
                continue
        
        if not valid_frames:
            raise Exception("Nenhuma frame válida encontrada!")
        
        if len(valid_frames) < len(frame_paths):
            print(f"   ℹ️  Usando {len(valid_frames)}/{len(frame_paths)} frames válidas")
        
        from PIL import ImageFile
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        
        # Cria vídeo
        print("   🎬 Criando vídeo a partir das frames...")
        video_clip = ImageSequenceClip(valid_frames, fps=fps)
        
        audio_clip = AudioFileClip(audio_path)
        if audio_clip.duration < video_clip.duration:
            loops_needed = int(video_clip.duration / audio_clip.duration) + 1
            audio_clip = concatenate_audioclips([audio_clip] * loops_needed)
        
        audio_clip = audio_clip.subclip(0, video_clip.duration)
        video_clip = video_clip.set_audio(audio_clip)
        
        # Salva vídeo
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_folder, f"lofi_video_{timestamp}.mp4")
        
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
        
        # Limpa recursos
        video_clip.close()
        audio_clip.close()
        
        # Limpa temporários
        print("\n🧹 Limpando arquivos temporários...")
        if os.path.exists(audio_path):
            os.remove(audio_path)
        if os.path.exists(frames_dir):
            shutil.rmtree(frames_dir)
            print(f"   ✅ {len(frame_paths)} frames removidas")
        
        print(f"\n✅ Vídeo criado com sucesso: {output_path}")
        return output_path
    
    def create_night_video(self, video_duration=30, images_dir="imagens noite", audios_dir="audio_noite", category=None):
        """
        Cria vídeo noturno com sons da natureza
        
        Args:
            video_duration: Duração do vídeo em segundos
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
        frames_dir = os.path.abspath(frames_dir)
        os.makedirs(frames_dir, exist_ok=True)
        
        # Seleciona categoria
        if category is None:
            categories = self.get_categories(images_dir, audios_dir)
            if not categories:
                raise Exception(f"❌ Nenhuma categoria encontrada! Verifique as pastas '{images_dir}' e '{audios_dir}'")
            category = random.choice(categories)
        
        print(f"\n📂 Categoria selecionada: {category}")
        
        # Procura imagens da categoria
        print(f"\n1️⃣  Procurando imagens na categoria '{category}'...")
        image_files = self.find_images_in_category(category, images_dir)
        
        if not image_files:
            raise Exception(f"❌ Nenhuma imagem encontrada em '{images_dir}/{category}/'!")
        
        selected_image = random.choice(image_files)
        print(f"   🖼️  Usando imagem: {os.path.basename(selected_image)}")
        
        # Procura áudios da categoria
        print(f"\n2️⃣  Procurando áudios na categoria '{category}'...")
        audio_files = self.find_audios_in_category(category, audios_dir)
        
        if not audio_files:
            raise Exception(f"❌ Nenhum áudio encontrado em '{audios_dir}/{category}/'!")
        
        selected_audio = random.choice(audio_files)
        print(f"   🎵 Usando áudio: {os.path.basename(selected_audio)}")
        
        # Processa áudio
        audio_clip = AudioFileClip(selected_audio)
        print(f"   ⏱️  Duração do áudio: {audio_clip.duration:.1f}s")
        
        if audio_clip.duration > video_duration:
            print(f"   ✂️  Cortando áudio para {video_duration}s...")
            audio_clip = audio_clip.subclip(0, video_duration)
        elif audio_clip.duration < video_duration:
            print(f"   🔁 Áudio menor que vídeo, fazendo loop...")
            loops_needed = int(video_duration / audio_clip.duration) + 1
            audio_clip = concatenate_audioclips([audio_clip] * loops_needed)
            audio_clip = audio_clip.subclip(0, video_duration)
        
        print("   💾 Processando áudio...")
        audio_clip.write_audiofile(audio_path, logger=None, verbose=False)
        audio_clip.close()
        
        # Gera frames
        print(f"\n3️⃣  Gerando frames animados...")
        fps = 30
        num_frames = int(video_duration * fps)
        
        frame_paths, scene_type = self.generator.generate_animated_frames(
            width=1920,
            height=1080,
            num_frames=num_frames,
            fps=fps,
            output_dir=frames_dir,
            base_image_path=selected_image
        )
        
        print(f"\n4️⃣  Criando vídeo com {num_frames} frames...")
        
        # Valida frames
        print("   🔍 Verificando frames...")
        valid_frames = []
        for frame_path in frame_paths:
            try:
                from PIL import Image
                with Image.open(frame_path) as img:
                    img.verify()
                with Image.open(frame_path) as img:
                    img.load()
                valid_frames.append(frame_path)
            except Exception as e:
                print(f"   ⚠️  Frame corrompida ignorada: {os.path.basename(frame_path)}")
                continue
        
        if not valid_frames:
            raise Exception("Nenhuma frame válida encontrada!")
        
        if len(valid_frames) < len(frame_paths):
            print(f"   ℹ️  Usando {len(valid_frames)}/{len(frame_paths)} frames válidas")
        
        from PIL import ImageFile
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        
        # Cria vídeo
        print("   🎬 Criando vídeo a partir das frames...")
        video_clip = ImageSequenceClip(valid_frames, fps=fps)
        
        audio_clip = AudioFileClip(audio_path)
        if audio_clip.duration < video_clip.duration:
            loops_needed = int(video_clip.duration / audio_clip.duration) + 1
            audio_clip = concatenate_audioclips([audio_clip] * loops_needed)
        
        audio_clip = audio_clip.subclip(0, video_clip.duration)
        video_clip = video_clip.set_audio(audio_clip)
        
        # Salva vídeo
        output_folder = "output"
        os.makedirs(output_folder, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_folder, f"night_video_{category.lower().replace(' ', '_')}_{timestamp}.mp4")
        
        print(f"\n5️⃣  Salvando vídeo: {output_path}")
        print("   ⏳ Isso pode levar alguns minutos...")
        
        # Tenta criar o vídeo com tratamento de erro melhorado
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Usa preset mais leve nas tentativas seguintes para reduzir uso de recursos
                preset = 'ultrafast' if attempt > 0 else 'medium'
                bitrate = '6000k' if attempt > 0 else '8000k'
                
                if attempt > 0:
                    print(f"   🔄 Tentativa {attempt + 1}/{max_retries} com preset mais leve...")
                    # Recria o video_clip se necessário
                    try:
                        video_clip.close()
                        audio_clip.close()
                    except:
                        pass
                    
                    # Recria os clips
                    video_clip = ImageSequenceClip(valid_frames, fps=fps)
                    audio_clip = AudioFileClip(audio_path)
                    if audio_clip.duration < video_clip.duration:
                        loops_needed = int(video_clip.duration / audio_clip.duration) + 1
                        audio_clip = concatenate_audioclips([audio_clip] * loops_needed)
                    audio_clip = audio_clip.subclip(0, video_clip.duration)
                    video_clip = video_clip.set_audio(audio_clip)
                
                video_clip.write_videofile(
                    output_path,
                    fps=fps,
                    codec='libx264',
                    audio_codec='aac',
                    bitrate=bitrate,
                    preset=preset,
                    logger=None,
                    verbose=False,
                    threads=2  # Limita threads para reduzir uso de recursos
                )
                break  # Sucesso, sai do loop
            except (BrokenPipeError, OSError) as e:
                if attempt < max_retries - 1:
                    print(f"   ⚠️  Erro ao criar vídeo (tentativa {attempt + 1}/{max_retries}): {e}")
                    print("   🔄 Tentando novamente em 10 segundos com configurações mais leves...")
                    time.sleep(10)
                    # Limpa recursos antes de tentar novamente
                    try:
                        video_clip.close()
                        audio_clip.close()
                    except:
                        pass
                    # Limpa arquivo parcial se existir
                    try:
                        if os.path.exists(output_path):
                            os.remove(output_path)
                    except:
                        pass
                else:
                    # Limpa recursos antes de lançar erro
                    try:
                        video_clip.close()
                        audio_clip.close()
                    except:
                        pass
                    raise  # Re-lança o erro na última tentativa
        
        # Limpa recursos
        video_clip.close()
        audio_clip.close()
        
        # Limpa temporários
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


# Funções de compatibilidade (mantém interface antiga)
def create_lofi_video(video_duration=60, images_dir="images", audios_dir="audios"):
    """Função de compatibilidade para criar vídeo LOFI"""
    creator = VideoCreator()
    return creator.create_morning_video(video_duration, images_dir, audios_dir)


def create_night_video(video_duration=60, images_dir="imagens noite", audios_dir="audio_noite", category=None):
    """Função de compatibilidade para criar vídeo noturno"""
    creator = VideoCreator()
    return creator.create_night_video(video_duration, images_dir, audios_dir, category)

