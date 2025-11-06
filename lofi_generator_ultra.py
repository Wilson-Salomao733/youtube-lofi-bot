"""
Gerador ULTRA de Vídeos LOFI
Máximo detalhe e realismo mantendo estilo pixel art
Com animações e movimento suave
"""
import os
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import numpy as np
import math


class LofiUltraGenerator:
    """Gerador LOFI ultra detalhado com animações"""
    
    def __init__(self):
        self.scene_types = [
            'room_ocean_view',  # Quarto com vista pro mar (prioridade)
            'study_room',       # Quarto de estudos com notebook
            'forest', 'lake', 'mountain', 'cafe', 
            'urban', 'city'  # Menos frequentes
        ]
        self.pixel_colors = {
            'sky': [(135, 206, 250), (176, 224, 230), (173, 216, 230), (240, 248, 255)],
            'forest_green': [(34, 139, 34), (46, 125, 50), (56, 178, 172), (76, 175, 80)],
            'building': [(169, 169, 169), (128, 128, 128), (105, 105, 105), (70, 130, 180)],
            'sunset': [(255, 140, 0), (255, 165, 0), (255, 192, 203), (255, 182, 193)],
            'ocean': [(70, 130, 180), (100, 149, 237), (65, 105, 225), (123, 104, 238)],
        }
        self.animation_state = {
            'cloud_offset_x': 0,
            'wave_offset': 0,
            'pan_offset': 0,
            'zoom_factor': 1.0,
            'particle_positions': []
        }
    
    def generate_ultra_scene(self, width=1920, height=1080, output_path="lofi_ultra.png", pixel_size=3):
        """Gera cena com qualidade HD melhorada (menos pixelização)"""
        # Reduz pixel_size para melhor qualidade (de 6 para 3 ou menos)
        pixel_width = width // pixel_size
        pixel_height = height // pixel_size
        
        # Cria imagem maior primeiro para suavização
        base_width = pixel_width * 2
        base_height = pixel_height * 2
        img = Image.new('RGB', (base_width, base_height), (135, 206, 250))
        draw = ImageDraw.Draw(img)
        
        # Prioriza cenas de quarto (mais frequentes)
        weights = [3, 3, 1, 1, 1, 1, 0.3, 0.3]  # room_ocean_view e study_room têm peso 3
        scene_type = random.choices(self.scene_types, weights=weights)[0]
        
        if scene_type == 'room_ocean_view':
            self._draw_room_ocean_view(draw, base_width, base_height)
        elif scene_type == 'study_room':
            self._draw_study_room(draw, base_width, base_height)
        elif scene_type == 'forest':
            self._draw_ultra_forest(draw, base_width, base_height)
        elif scene_type == 'city':
            self._draw_ultra_city(draw, base_width, base_height)
        elif scene_type == 'cafe':
            self._draw_ultra_cafe(draw, base_width, base_height)
        elif scene_type == 'lake':
            self._draw_ultra_lake(draw, base_width, base_height)
        elif scene_type == 'urban':
            self._draw_ultra_urban(draw, base_width, base_height)
        else:  # mountain
            self._draw_ultra_mountain(draw, base_width, base_height)
        
        # Aplica filtro de suavização para melhor qualidade
        img = img.filter(ImageFilter.SMOOTH_MORE)
        
        # Redimensiona para tamanho final com alta qualidade
        img = img.resize((width, height), Image.LANCZOS)
        
        # Melhora contraste e saturação
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.15)
        
        img.save(output_path, quality=95)
        print(f"✅ Cena ultra detalhada gerada ({scene_type}): {output_path}")
        return output_path
    
    def generate_animated_frames_from_image(self, base_image_path, width=1920, height=1080, num_frames=90, fps=30, output_dir="frames"):
        """Gera frames animadas a partir de uma imagem PNG existente"""
        # Garante que a pasta de output existe (caminho absoluto)
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        if not os.path.exists(output_dir):
            raise OSError(f"Não foi possível criar o diretório: {output_dir}")
        
        # Carrega a imagem base
        if not os.path.exists(base_image_path):
            raise FileNotFoundError(f"Imagem não encontrada: {base_image_path}")
        
        base_img = Image.open(base_image_path)
        img_width, img_height = base_img.size
        
        # Redimensiona para tamanho maior para permitir zoom/pan
        canvas_width = int(width * 1.5)
        canvas_height = int(height * 1.5)
        
        # Redimensiona mantendo aspect ratio
        aspect_ratio = img_width / img_height
        if canvas_width / canvas_height > aspect_ratio:
            new_height = canvas_height
            new_width = int(new_height * aspect_ratio)
        else:
            new_width = canvas_width
            new_height = int(new_width / aspect_ratio)
        
        # Redimensiona a imagem base
        base_img = base_img.resize((new_width, new_height), Image.LANCZOS)
        
        # Cria canvas maior com a imagem centralizada
        canvas = Image.new('RGB', (canvas_width, canvas_height), (135, 206, 250))
        paste_x = (canvas_width - new_width) // 2
        paste_y = (canvas_height - new_height) // 2
        canvas.paste(base_img, (paste_x, paste_y))
        
        duration = num_frames / fps
        pan_speed = width * 0.1 / duration
        zoom_start = 1.0
        zoom_end = 1.05
        
        frame_paths = []
        
        for frame_num in range(num_frames):
            t = frame_num / num_frames
            
            # Calcula offsets de animação
            pan_offset = int(pan_speed * t * duration) % (width // 4)
            zoom = zoom_start + (zoom_end - zoom_start) * t
            
            # Aplica zoom e crop
            zoomed_width = int(canvas_width * zoom)
            zoomed_height = int(canvas_height * zoom)
            img_zoomed = canvas.resize((zoomed_width, zoomed_height), Image.LANCZOS)
            
            # Crop centralizado com pan
            left = (zoomed_width - width) // 2 + pan_offset
            top = (zoomed_height - height) // 2
            right = left + width
            bottom = top + height
            
            # Garante que o crop está dentro dos limites
            left = max(0, min(left, zoomed_width - width))
            top = max(0, min(top, zoomed_height - height))
            right = left + width
            bottom = top + height
            
            img = img_zoomed.crop((left, top, right, bottom))
            
            # Melhora qualidade
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.05)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.1)
            
            # Gera frame - garante que o diretório existe antes de salvar
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            frame_path = os.path.join(output_dir, f"frame_{frame_num:05d}.png")
            img.save(frame_path, quality=95)
            frame_paths.append(frame_path)
            
            if (frame_num + 1) % 30 == 0:
                print(f"   📸 {frame_num + 1}/{num_frames} frames geradas...")
        
        print(f"✅ {num_frames} frames animadas geradas a partir de {base_image_path}")
        return frame_paths, "custom_image"
    
    def find_background_images(self, image_dir="images"):
        """Procura imagens PNG/JPG na pasta especificada"""
        import glob
        import os
        
        if not os.path.exists(image_dir):
            return []
        
        # Procura por PNG e JPG
        image_files = []
        image_files.extend(glob.glob(os.path.join(image_dir, "*.png")))
        image_files.extend(glob.glob(os.path.join(image_dir, "*.jpg")))
        image_files.extend(glob.glob(os.path.join(image_dir, "*.jpeg")))
        image_files.extend(glob.glob(os.path.join(image_dir, "*.PNG")))
        image_files.extend(glob.glob(os.path.join(image_dir, "*.JPG")))
        image_files.extend(glob.glob(os.path.join(image_dir, "*.JPEG")))
        
        return sorted(image_files)
    
    def generate_animated_frames(self, width=1920, height=1080, num_frames=90, fps=30, output_dir="frames", base_image_path=None):
        """Gera múltiplas frames animadas para criar movimento"""
        # Garante que a pasta de output existe (caminho absoluto)
        output_dir = os.path.abspath(output_dir)
        os.makedirs(output_dir, exist_ok=True)
        if not os.path.exists(output_dir):
            raise OSError(f"Não foi possível criar o diretório: {output_dir}")
        
        # Se uma imagem base foi fornecida, usa ela
        if base_image_path:
            return self.generate_animated_frames_from_image(
                base_image_path, width, height, num_frames, fps, output_dir
            )
        
        # Fixa seed para cena base consistente
        scene_seed = random.randint(0, 1000000)
        # Prioriza cenas de quarto (mais frequentes)
        weights = [3, 3, 1, 1, 1, 1, 0.3, 0.3]  # room_ocean_view e study_room têm peso 3
        scene_type = random.choices(self.scene_types, weights=weights)[0]
        duration = num_frames / fps
        
        # Inicializa estado de animação
        pan_speed = width * 0.1 / duration  # Pan de 10% da tela
        cloud_speed = width * 0.05 / duration
        wave_speed = 2.0  # Ciclos por segundo
        zoom_start = 1.0
        zoom_end = 1.05  # Zoom suave de 5%
        
        frame_paths = []
        
        # Gera cena base uma vez (sem animação)
        random.seed(scene_seed)
        canvas_width = int(width * 1.5)
        canvas_height = int(height * 1.5)
        pixel_size = 2
        pixel_width = canvas_width // pixel_size
        pixel_height = canvas_height // pixel_size
        base_width = pixel_width * 2
        base_height = pixel_height * 2
        
        # Cria imagem base
        base_img = Image.new('RGB', (base_width, base_height), (135, 206, 250))
        base_draw = ImageDraw.Draw(base_img)
        
        # Desenha cena base (sem animação)
        if scene_type == 'room_ocean_view':
            self._draw_room_ocean_view(base_draw, base_width, base_height)
        elif scene_type == 'study_room':
            self._draw_study_room(base_draw, base_width, base_height)
        elif scene_type == 'forest':
            self._draw_ultra_forest(base_draw, base_width, base_height)
        elif scene_type == 'city':
            self._draw_ultra_city(base_draw, base_width, base_height)
        elif scene_type == 'cafe':
            self._draw_ultra_cafe(base_draw, base_width, base_height)
        elif scene_type == 'lake':
            self._draw_ultra_lake(base_draw, base_width, base_height)
        elif scene_type == 'urban':
            self._draw_ultra_urban(base_draw, base_width, base_height)
        else:  # mountain
            self._draw_ultra_mountain(base_draw, base_width, base_height)
        
        # Aplica suavização na base
        base_img = base_img.filter(ImageFilter.SMOOTH_MORE)
        base_img = base_img.resize((canvas_width, canvas_height), Image.LANCZOS)
        
        for frame_num in range(num_frames):
            t = frame_num / num_frames
            
            # Calcula offsets de animação
            pan_offset = int(pan_speed * t * duration) % (width // 4)
            cloud_offset = int(cloud_speed * t * duration)
            wave_phase = (t * duration * wave_speed) % (2 * math.pi)
            zoom = zoom_start + (zoom_end - zoom_start) * t
            
            # Copia imagem base
            img = base_img.copy()
            draw = ImageDraw.Draw(img)
            
            # Adiciona elementos animados
            if scene_type == 'room_ocean_view':
                self._draw_animated_waves(draw, canvas_width, canvas_height, wave_phase)
                self._draw_animated_clouds(draw, canvas_width, canvas_height, cloud_offset)
            elif scene_type == 'study_room':
                # Movimento sutil na luz da janela
                pass  # Pode adicionar animações sutis depois
            elif scene_type == 'forest':
                self._draw_animated_clouds(draw, canvas_width, canvas_height, cloud_offset)
            elif scene_type == 'city':
                self._draw_animated_clouds(draw, canvas_width, canvas_height, cloud_offset)
            elif scene_type == 'cafe':
                self._draw_animated_clouds(draw, canvas_width, canvas_height, cloud_offset)
            elif scene_type == 'lake':
                self._draw_animated_waves(draw, canvas_width, canvas_height, wave_phase)
                self._draw_animated_clouds(draw, canvas_width, canvas_height, cloud_offset)
            elif scene_type == 'urban':
                self._draw_animated_clouds(draw, canvas_width, canvas_height, cloud_offset)
            else:  # mountain
                self._draw_animated_clouds(draw, canvas_width, canvas_height, cloud_offset)
            
            # Aplica zoom e crop
            zoomed_width = int(canvas_width * zoom)
            zoomed_height = int(canvas_height * zoom)
            img = img.resize((zoomed_width, zoomed_height), Image.LANCZOS)
            
            # Crop centralizado com pan
            left = (zoomed_width - width) // 2 + pan_offset
            top = (zoomed_height - height) // 2
            right = left + width
            bottom = top + height
            
            # Garante que o crop está dentro dos limites
            left = max(0, min(left, zoomed_width - width))
            top = max(0, min(top, zoomed_height - height))
            right = left + width
            bottom = top + height
            
            img = img.crop((left, top, right, bottom))
            
            # Melhora qualidade
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.1)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.15)
            
            # Gera frame - garante que o diretório existe antes de salvar
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            frame_path = os.path.join(output_dir, f"frame_{frame_num:05d}.png")
            img.save(frame_path, quality=95)
            frame_paths.append(frame_path)
            
            if (frame_num + 1) % 30 == 0:
                print(f"   📸 {frame_num + 1}/{num_frames} frames geradas...")
        
        print(f"✅ {num_frames} frames animadas geradas ({scene_type})")
        return frame_paths, scene_type
    
    def _draw_animated_clouds(self, draw, w, h, cloud_offset):
        """Desenha nuvens animadas que se movem"""
        # Posições fixas das nuvens para consistência
        cloud_positions = [
            (h // 10, 50), (h // 8, 55), (h // 7, 45), 
            (h // 6, 60), (h // 9, 50)
        ]
        
        for i, (cloud_y, cloud_w) in enumerate(cloud_positions):
            cloud_x = (w * i / 5 + cloud_offset) % (w * 2) - w // 4
            if -w // 4 <= cloud_x <= w * 1.25:
                # Desenha nuvem em camadas para parecer mais natural
                offsets = [(-12, -8), (0, 0), (12, 8), (-8, -5), (8, 5), (-5, -3)]
                for offset_x, offset_y in offsets:
                    draw.ellipse(
                        [(cloud_x + offset_x - cloud_w // 6, cloud_y + offset_y),
                         (cloud_x + offset_x + cloud_w // 6, cloud_y + offset_y + 20)],
                        fill=(240, 240, 250)
                    )
    
    def _draw_animated_waves(self, draw, w, h, wave_phase):
        """Desenha ondas animadas"""
        wave_amplitude = 3
        water_level = h // 2 + 20
        for i in range(20):
            wave_x = i * w // 20
            wave_offset = int(wave_amplitude * math.sin(wave_phase + i * 0.5))
            wave_y = water_level + wave_offset
            
            for x in range(30):
                if (x + int(wave_phase * 10)) % 8 < 4:
                    draw.rectangle(
                        [(wave_x + x, wave_y), (wave_x + x + 1, wave_y + 2)],
                        fill=(90, 150, 210)
                    )
    
    
    def _draw_room_ocean_view(self, draw, w, h):
        """Quarto minimalista com vista pro mar"""
        # Parede do quarto (lado esquerdo e direito)
        wall_color = (245, 245, 240)
        draw.rectangle([(0, 0), (w // 3, h)], fill=wall_color)
        draw.rectangle([(2 * w // 3, 0), (w, h)], fill=wall_color)
        
        # Janela grande central com vista pro mar
        window_x = w // 3
        window_y = h // 6
        window_w = w // 3
        window_h = h * 2 // 3
        
        # Moldura da janela
        window_frame_color = (139, 139, 139)
        draw.rectangle([(window_x, window_y), (window_x + window_w, window_y + window_h)], 
                      outline=window_frame_color, width=8)
        
        # Divisor de vidro (cruz)
        draw.line([(window_x + window_w // 2, window_y), 
                  (window_x + window_w // 2, window_y + window_h)], 
                 fill=window_frame_color, width=4)
        draw.line([(window_x, window_y + window_h // 2), 
                  (window_x + window_w, window_y + window_h // 2)], 
                 fill=window_frame_color, width=4)
        
        # Vista do mar através da janela
        ocean_start = window_y + window_h // 2
        for y in range(ocean_start, window_y + window_h):
            ratio = (y - ocean_start) / (window_h // 2)
            ocean_r = int(100 * (1 - ratio) + 135 * ratio)
            ocean_g = int(149 * (1 - ratio) + 206 * ratio)
            ocean_b = int(237 * (1 - ratio) + 250 * ratio)
            draw.line(
                [(window_x + 10, y), (window_x + window_w - 10, y)],
                fill=(ocean_r, ocean_g, ocean_b)
            )
        
        # Céu na janela
        for y in range(window_y + 10, ocean_start):
            ratio = (y - window_y - 10) / (ocean_start - window_y - 10)
            sky_r = int(135 * (1 - ratio) + 240 * ratio)
            sky_g = int(206 * (1 - ratio) + 248 * ratio)
            sky_b = int(250 * (1 - ratio) + 255 * ratio)
            draw.line(
                [(window_x + 10, y), (window_x + window_w - 10, y)],
                fill=(sky_r, sky_g, sky_b)
            )
        
        # Mesa/parede abaixo da janela
        desk_color = (220, 200, 180)
        desk_y = window_y + window_h + 10
        draw.rectangle([(window_x, desk_y), (window_x + window_w, h)], fill=desk_color)
        
        # Alguns objetos na mesa (opcional)
        # Planta
        plant_x = window_x + window_w // 4
        plant_y = desk_y + 20
        draw.ellipse(
            [(plant_x - 10, plant_y - 15), (plant_x + 10, plant_y + 5)],
            fill=(34, 139, 34)
        )
        draw.rectangle(
            [(plant_x - 5, plant_y + 5), (plant_x + 5, plant_y + 20)],
            fill=(139, 69, 19)
        )
        
        # Cadeira/banco abaixo da janela
        chair_y = desk_y + 40
        draw.rectangle(
            [(window_x + window_w // 2 - 15, chair_y), 
             (window_x + window_w // 2 + 15, chair_y + 30)],
            fill=(101, 67, 33)
        )
        
        # Sol/lua no céu
        astro_x = window_x + window_w // 2
        astro_y = window_y + window_h // 4
        astro_size = 15
        draw.ellipse(
            [(astro_x - astro_size, astro_y - astro_size),
             (astro_x + astro_size, astro_y + astro_size)],
            fill=(255, 253, 208)
        )
    
    def _draw_study_room(self, draw, w, h):
        """Quarto de estudos com notebook e pessoa estudando"""
        # Parede de fundo
        wall_color = (250, 248, 240)
        draw.rectangle([(0, 0), (w, h)], fill=wall_color)
        
        # Mesa no centro inferior
        desk_y = h * 3 // 4
        desk_w = w // 2
        desk_x = w // 2 - desk_w // 2
        desk_h = h // 8
        
        desk_color = (139, 115, 85)
        draw.rectangle(
            [(desk_x, desk_y), (desk_x + desk_w, desk_y + desk_h)],
            fill=desk_color
        )
        
        # Notebook na mesa
        laptop_w = desk_w // 3
        laptop_h = desk_h
        laptop_x = desk_x + desk_w // 2 - laptop_w // 2
        laptop_y = desk_y - laptop_h // 3
        
        # Tela do notebook (aberta)
        screen_color = (50, 50, 70)
        screen_top = laptop_y - laptop_h
        draw.rectangle(
            [(laptop_x, screen_top), (laptop_x + laptop_w, laptop_y)],
            fill=screen_color
        )
        
        # Borda da tela
        draw.rectangle(
            [(laptop_x, screen_top), (laptop_x + laptop_w, laptop_y)],
            outline=(100, 100, 120), width=3
        )
        
        # Base do notebook
        base_color = (80, 80, 100)
        draw.rectangle(
            [(laptop_x, laptop_y), (laptop_x + laptop_w, laptop_y + laptop_h // 3)],
            fill=base_color
        )
        
        # Teclado (linhas)
        for i in range(3):
            key_y = laptop_y + i * (laptop_h // 9)
            draw.rectangle(
                [(laptop_x + 5, key_y), (laptop_x + laptop_w - 5, key_y + 2)],
                fill=(120, 120, 140)
            )
        
        # Teclas brilhantes (indicação de uso)
        draw.ellipse(
            [(laptop_x + laptop_w // 4, laptop_y + 2),
             (laptop_x + laptop_w // 4 + 8, laptop_y + 8)],
            fill=(255, 200, 100)
        )
        
        # Pessoa estudando (silhueta simples)
        person_x = laptop_x + laptop_w + 20
        person_y = desk_y
        
        # Cabeça
        head_size = 15
        draw.ellipse(
            [(person_x - head_size, person_y - head_size * 2),
             (person_x + head_size, person_y - head_size)],
            fill=(60, 50, 40)
        )
        
        # Corpo (tronco)
        body_w = 25
        body_h = 30
        draw.rectangle(
            [(person_x - body_w // 2, person_y - head_size - body_h),
             (person_x + body_w // 2, person_y - head_size)],
            fill=(80, 70, 60)
        )
        
        # Braços (um apoiado na mesa)
        # Braço esquerdo
        draw.ellipse(
            [(person_x - body_w, person_y - head_size - body_h // 2),
             (person_x - body_w // 2, person_y - head_size)],
            fill=(80, 70, 60)
        )
        
        # Braço direito (sobre a mesa)
        draw.rectangle(
            [(person_x + body_w // 2, person_y - head_size - body_h // 2),
             (person_x + body_w, person_y - head_size - body_h // 4)],
            fill=(80, 70, 60)
        )
        
        # Cadeira
        chair_x = person_x
        chair_y = desk_y + desk_h
        chair_w = 30
        chair_h = 20
        
        draw.rectangle(
            [(chair_x - chair_w // 2, chair_y),
             (chair_x + chair_w // 2, chair_y + chair_h)],
            fill=(101, 67, 33)
        )
        
        # Encosto da cadeira
        draw.rectangle(
            [(chair_x - chair_w // 2, chair_y - 40),
             (chair_x + chair_w // 2, chair_y)],
            fill=(139, 69, 19)
        )
        
        # Janela lateral (opcional - no fundo)
        window_bg_x = w // 10
        window_bg_y = h // 10
        window_bg_w = w // 5
        window_bg_h = h // 3
        
        # Céu na janela de fundo
        for y in range(window_bg_y, window_bg_y + window_bg_h):
            ratio = (y - window_bg_y) / window_bg_h
            sky_r = int(200 * (1 - ratio) + 230 * ratio)
            sky_g = int(220 * (1 - ratio) + 240 * ratio)
            sky_b = int(240 * (1 - ratio) + 250 * ratio)
            draw.line(
                [(window_bg_x, y), (window_bg_x + window_bg_w, y)],
                fill=(sky_r, sky_g, sky_b)
            )
        
        # Moldura da janela de fundo
        draw.rectangle(
            [(window_bg_x, window_bg_y), 
             (window_bg_x + window_bg_w, window_bg_y + window_bg_h)],
            outline=(139, 139, 139), width=4
        )
        
        # Objetos na mesa (livros, caneta)
        # Livro
        book_x = desk_x + desk_w + 30
        book_y = desk_y + 5
        draw.rectangle(
            [(book_x, book_y), (book_x + 20, book_y + 15)],
            fill=(200, 150, 100)
        )
        draw.line(
            [(book_x + 5, book_y), (book_x + 5, book_y + 15)],
            fill=(150, 100, 50), width=2
        )
        
        # Caneta
        pen_x = book_x + 25
        draw.rectangle(
            [(pen_x, book_y + 5), (pen_x + 2, book_y + 20)],
            fill=(50, 50, 150)
        )
    
    def _draw_ultra_forest(self, draw, w, h):
        """Floresta realista com mais detalhes"""
        # Céu com gradiente suave melhorado
        for y in range(h // 3):
            ratio = y / (h // 3)
            sky_r = int(135 * (1 - ratio) + 240 * ratio)
            sky_g = int(206 * (1 - ratio) + 248 * ratio)
            sky_b = int(250 * (1 - ratio) + 255 * ratio)
            draw.rectangle([(0, y), (w, y)], fill=(sky_r, sky_g, sky_b))
        
        # Grama com variação de cor
        for y in range(h * 2 // 3, h):
            grass_variation = random.randint(-8, 8)
            grass_r = min(255, max(0, 76 + grass_variation))
            grass_g = min(255, max(0, 175 + grass_variation))
            grass_b = min(255, max(0, 80 + grass_variation))
            draw.rectangle([(0, y), (w, y)], fill=(grass_r, grass_g, grass_b))
        
        # Múltiplas árvores em profundidade
        tree_positions = []
        for i in range(12):
            tree_x = w * i // 13 + random.randint(-w // 50, w // 50)
            tree_positions.append(tree_x)
        
        # Árvores maiores atrás, menores na frente (perspectiva)
        for idx, tree_x in enumerate(tree_positions):
            # Árvores mais distantes são menores
            depth = idx / len(tree_positions)
            tree_height = int(h // 2.5 + (h // 2 - h // 2.5) * (1 - depth))
            tree_width = int(w // 12 + (w // 6 - w // 12) * (1 - depth))
            
            # Cor mais escura para árvores distantes
            crown_base = random.choice(self.pixel_colors['forest_green'])
            if depth < 0.5:  # Árvores distantes
                crown_color = tuple(max(0, c - 30) for c in crown_base)
            else:
                crown_color = crown_base
            
            # Tronco com profundidade
            trunk_w = max(2, int(w // 50 * (1 + depth)))
            trunk_h = int(tree_height // 2.8)
            
            # Sombra do tronco
            trunk_shadow = (70, 50, 30)
            draw.rectangle(
                [(max(0, tree_x - trunk_w - 1), h - trunk_h),
                 (min(w, tree_x + trunk_w + 1), h)],
                fill=trunk_shadow
            )
            
            # Tronco principal
            draw.rectangle(
                [(max(0, tree_x - trunk_w), h - trunk_h),
                 (min(w, tree_x + trunk_w), h)],
                fill=(101, 67, 33)
            )
            
            # Copa em camadas (mais realista)
            # Camada inferior (mais escura)
            draw.ellipse(
                [(max(0, tree_x - tree_width), h - trunk_h - tree_height * 2 // 3),
                 (min(w, tree_x + tree_width), h - trunk_h - tree_height // 3)],
                fill=tuple(max(0, c - 25) for c in crown_color)
            )
            
            # Camada superior (mais clara)
            draw.ellipse(
                [(max(0, tree_x - tree_width * 4 // 5), h - trunk_h - tree_height),
                 (min(w, tree_x + tree_width * 4 // 5), h - trunk_h - tree_height * 2 // 3)],
                fill=crown_color
            )
        
        # Sol/lua com brilho
        astro_x = random.randint(w // 4, 3 * w // 4)
        astro_y = random.randint(h // 8, h // 4)
        astro_size = random.randint(8, 12)
        
        if random.random() < 0.7:
            # Sol com brilho ao redor
            draw.ellipse(
                [(astro_x - astro_size - 2, astro_y - astro_size - 2),
                 (astro_x + astro_size + 2, astro_y + astro_size + 2)],
                fill=(255, 250, 200)
            )
            draw.ellipse(
                [(astro_x - astro_size, astro_y - astro_size),
                 (astro_x + astro_size, astro_y + astro_size)],
                fill=(255, 235, 150)
            )
        else:
            # Lua com fase
            draw.ellipse(
                [(astro_x - astro_size, astro_y - astro_size),
                 (astro_x + astro_size, astro_y + astro_size)],
                fill=(255, 255, 240)
            )
            # Sombra na lua (fase)
            draw.ellipse(
                [(astro_x - astro_size // 2, astro_y - astro_size),
                 (astro_x + astro_size // 3, astro_y + astro_size)],
                fill=(240, 240, 240)
            )
    
    
    def _draw_ultra_city(self, draw, w, h):
        """Cidade noturna simplificada com melhor qualidade"""
        # Céu escuro com gradiente
        for y in range(h // 3):
            ratio = y / (h // 3)
            r = int(25 * (1 - ratio) + 40 * ratio)
            g = int(25 * (1 - ratio) + 35 * ratio)
            b = int(50 * (1 - ratio) + 60 * ratio)
            draw.rectangle([(0, y), (w, y)], fill=(r, g, b))
        
        # Estrelas mais detalhadas
        for _ in range(50):
            x = random.randint(0, w)
            y = random.randint(0, h // 3)
            brightness = random.randint(200, 255)
            size = random.randint(1, 2)
            draw.ellipse(
                [(x-size, y-size), (x+size, y+size)],
                fill=(brightness, brightness, brightness)
            )
        
        # Prédios (quantidade balanceada)
        num_buildings = 12
        for i in range(num_buildings):
            x = w * i // num_buildings
            building_w = w // num_buildings
            building_h = random.randint(h // 3, h * 2 // 3)
            
            if i % 3 == 0:
                building_h = random.randint(h // 2, h * 3 // 4)
            
            # Prédio
            base_color = random.choice(self.pixel_colors['building'])
            draw.rectangle(
                [(x, h - building_h),
                 (x + building_w, h)],
                fill=base_color
            )
            
            # Janelas simples (algunas acesas)
            for row in range(2):
                for col in range(2):
                    if random.random() < 0.5:
                        window_x = x + col * building_w // 2 + building_w // 4
                        window_y = h - building_h + row * building_h // 2 + building_h // 4
                        window_size = building_w // 6
                        draw.rectangle(
                            [(window_x, window_y),
                             (window_x + window_size, window_y + window_size)],
                            fill=(255, 200, 100)
                        )
        
        # Lua
        moon_x = random.randint(3 * w // 4, 4 * w // 5)
        moon_y = random.randint(h // 8, h // 4)
        moon_size = random.randint(10, 15)
        draw.ellipse(
            [(moon_x - moon_size, moon_y - moon_size),
             (moon_x + moon_size, moon_y + moon_size)],
            fill=(255, 255, 240)
        )
    
    
    def _draw_ultra_cafe(self, draw, w, h):
        """Café simplificado com melhor qualidade"""
        # Céu com gradiente
        for y in range(h // 2):
            ratio = y / (h // 2)
            sky_r = int(135 * (1 - ratio) + 220 * ratio)
            sky_g = int(206 * (1 - ratio) + 238 * ratio)
            sky_b = int(250 * (1 - ratio) + 255 * ratio)
            draw.rectangle([(0, y), (w, y)], fill=(sky_r, sky_g, sky_b))
        
        # Café (lado esquerdo)
        cafe_w = w // 3
        cafe_h = h
        
        # Parede
        wall_color = (245, 230, 200)
        draw.rectangle([(0, 0), (cafe_w, cafe_h)], fill=wall_color)
        
        # Janelas simples
        for i in range(2):
            window_x = cafe_w // 4
            window_y = cafe_h // 3 + i * cafe_h // 3
            window_w = cafe_w // 2
            window_h = cafe_h // 4
            
            draw.rectangle([(window_x, window_y), (window_x + window_w, window_y + window_h)], 
                          fill=(70, 130, 180))
        
        # Terraço
        terrace_y = h * 2 // 3
        wood_color = (139, 69, 19)
        for y in range(terrace_y, h):
            draw.rectangle([(w // 3, y), (w, y)], fill=wood_color)
        
        # Mesa simples
        table_x = w // 2
        table_y = terrace_y + 5
        
        draw.ellipse([(table_x - 10, table_y - 5), (table_x + 10, table_y + 2)], 
                    fill=(101, 67, 33))
        
        # Xícaras
        draw.ellipse([(table_x - 8, table_y - 8), (table_x - 3, table_y - 3)], 
                    fill=(255, 255, 255))
        draw.ellipse([(table_x + 3, table_y - 8), (table_x + 8, table_y - 3)], 
                    fill=(255, 255, 255))
        
        # Sol
        sun_x = random.randint(w // 2, 4 * w // 5)
        sun_y = random.randint(h // 10, h // 3)
        sun_size = 8
        draw.ellipse([(sun_x - sun_size, sun_y - sun_size),
                     (sun_x + sun_size, sun_y + sun_size)], 
                    fill=(255, 235, 150))
    
    
    def _draw_ultra_lake(self, draw, w, h):
        """Lago ultra detalhado com melhor qualidade"""
        # Céu gradiente melhorado
        for y in range(h // 2):
            ratio = y / (h // 2)
            r = int(135 * (1 - ratio) + 240 * ratio)
            g = int(206 * (1 - ratio) + 248 * ratio)
            b = int(250 * (1 - ratio) + 255 * ratio)
            draw.rectangle([(0, y), (w, y)], fill=(r, g, b))
        
        # Lago com gradiente mais suave
        for y in range(h // 2, h):
            ratio = (y - h // 2) / (h // 2)
            ocean_r = int(70 * (1 - ratio) + 100 * ratio)
            ocean_g = int(130 * (1 - ratio) + 149 * ratio)
            ocean_b = int(180 * (1 - ratio) + 237 * ratio)
            draw.rectangle([(0, y), (w, y)], fill=(ocean_r, ocean_g, ocean_b))
        
        # Ondas no lago melhoradas
        for i in range(12):
            wave_y = h // 2 + random.randint(0, h // 4)
            wave_x = random.randint(0, w)
            wave_w = random.randint(w // 10, w // 5)
            
            for x in range(wave_w):
                if x % 4 < 2:
                    draw.rectangle([(wave_x + x, wave_y), (wave_x + x + 1, wave_y + 3)], 
                                 fill=(80, 140, 200))
        
        # Folhas flutuantes
        for _ in range(15):
            leaf_x = random.randint(0, w)
            leaf_y = random.randint(h // 2 + 10, h - 10)
            leaf_size = random.randint(4, 8)
            
            # Folha com sombra
            leaf_color = random.choice([(144, 238, 144), (152, 251, 152), (124, 252, 0)])
            draw.ellipse([(leaf_x - leaf_size, leaf_y - leaf_size),
                         (leaf_x + leaf_size, leaf_y + leaf_size)], 
                        fill=leaf_color)
            # Sombra debaixo
            draw.ellipse([(leaf_x - leaf_size, leaf_y),
                         (leaf_x + leaf_size, leaf_y + leaf_size // 2)], 
                        fill=(0, 80, 0))
        
        # Árvores na margem com detalhes
        for tree_x in [w // 8, w // 3, w // 2, 5 * w // 8, 7 * w // 8]:
            tree_h = random.randint(h // 4, h // 3)
            tree_w = random.randint(w // 15, w // 10)
            
            # Tronco
            trunk_w = max(1, w // 100)
            trunk_h = min(h, tree_h // 2)
            
            for tx in range(trunk_w):
                draw.rectangle(
                    [(tree_x + tx, h // 2 - trunk_h),
                     (tree_x + tx + 1, h // 2)],
                    fill=(139, 69, 19)
                )
            
            # Copa com gradiente
            for y_offset in range(trunk_h):
                crown_w = int(tree_w * (1 - y_offset / trunk_h))
                crown_color = random.choice(self.pixel_colors['forest_green'])
                draw.ellipse(
                    [(tree_x - crown_w, h // 2 - tree_h - y_offset * 2),
                     (tree_x + crown_w, h // 2 - trunk_h)],
                    fill=crown_color
                )
        
        # Sol com reflexo na água
        sun_x = w // 2
        sun_y = h * random.uniform(0.2, 0.3)
        sun_size = 10
        
        # Reflexo na água (alongado)
        draw.ellipse([(sun_x - sun_size * 3, h // 2 + 5),
                     (sun_x + sun_size * 3, h // 2 + 20)], 
                    fill=(255, 245, 180))
        
        # Sol principal
        draw.ellipse([(sun_x - sun_size, sun_y - sun_size),
                     (sun_x + sun_size, sun_y + sun_size)], 
                    fill=(255, 215, 0))
    
    
    def _draw_ultra_urban(self, draw, w, h):
        """Cidade urbana ultra detalhada com melhor qualidade"""
        # Céu gradiente melhorado
        for y in range(h // 3):
            ratio = y / (h // 3)
            r = int(176 * (1 - ratio) + 255 * ratio)
            g = int(196 * (1 - ratio) + 250 * ratio)
            b = int(222 * (1 - ratio) + 240 * ratio)
            draw.rectangle([(0, y), (w, y)], fill=(r, g, b))
        
        colors = [(220, 220, 220), (200, 200, 200), (180, 180, 180), 
                  (210, 210, 210), (190, 190, 190), (230, 230, 230)]
        
        num_buildings = 25
        for i in range(num_buildings):
            x = w * i // num_buildings
            building_w = w // num_buildings
            building_h = random.randint(h // 2, h * 3 // 4)
            
            # Prédio com sombra lateral
            base_color = random.choice(colors)
            draw.rectangle([(x, h - building_h), (x + building_w, h)], fill=base_color)
            
            # Sombra na lateral direita
            draw.rectangle([(x + building_w - 2, h - building_h), 
                          (x + building_w, h)], 
                         fill=(120, 120, 130))
            
            # Janelas detalhadas
            windows_per_row = 4
            rows = max(2, building_h // 20)
            for row in range(rows):
                for col in range(windows_per_row):
                    if random.random() < 0.4:
                        window_x = x + col * building_w // windows_per_row + building_w // 8
                        window_y = h - building_h + row * building_h // rows + building_h // (2 * rows)
                        window_size = max(2, building_w // 10)
                        
                        window_color = random.choice([
                            (100, 149, 237), (135, 206, 250), (255, 255, 200),
                            (255, 228, 181)
                        ])
                        draw.rectangle(
                            [(window_x, window_y),
                             (window_x + window_size, window_y + window_size)],
                            fill=window_color
                        )
                        
                        # Cruzamento
                        draw.line(
                            [(window_x + window_size // 2, window_y),
                             (window_x + window_size // 2, window_y + window_size)],
                            fill=(80, 100, 150)
                        )
                        draw.line(
                            [(window_x, window_y + window_size // 2),
                             (window_x + window_size, window_y + window_size // 2)],
                            fill=(80, 100, 150)
                        )
    
    
    def _draw_ultra_mountain(self, draw, w, h):
        """Montanhas ultra detalhadas com melhor qualidade"""
        # Céu gradiente melhorado
        for y in range(h // 2):
            ratio = y / (h // 2)
            sky_colors = [(176, 196, 222), (255, 228, 196), (240, 248, 255)]
            base_sky = random.choice(sky_colors)
            r = int(base_sky[0] * (1 - ratio) + 255 * ratio)
            g = int(base_sky[1] * (1 - ratio) + 248 * ratio)
            b = int(base_sky[2] * (1 - ratio) + 255 * ratio)
            draw.rectangle([(0, y), (w, y)], fill=(r, g, b))
        
        # Múltiplas camadas de montanhas
        # Camada mais distante (mais clara)
        distant_peaks = [(0, h // 2), (w // 4, h // 3), (w // 2, h // 2.5), 
                        (3 * w // 4, h // 2.7), (w, h // 2)]
        distant_color = (140, 160, 140)
        draw.polygon(distant_peaks + [(w, h)], fill=distant_color)
        
        # Camada média
        mid_peaks = [(0, h // 2), (w // 5, h // 2.3), (2 * w // 5, h // 1.8),
                    (3 * w // 5, h // 2.1), (4 * w // 5, h // 1.9), (w, h // 2)]
        mid_color = (120, 145, 120)
        draw.polygon(mid_peaks + [(w, h)], fill=mid_color)
        
        # Camada próxima (mais escura)
        near_peaks = [(0, h // 2), (w // 6, h // 1.5), (w // 3, h // 1.4),
                     (w // 2, h // 1.6), (2 * w // 3, h // 1.3),
                     (5 * w // 6, h // 1.5), (w, h // 2)]
        near_color = (100, 130, 100)
        draw.polygon(near_peaks + [(w, h)], fill=near_color)
        
        # Sombra nos picos
        for i in range(len(near_peaks) - 1):
            shadow_start = (near_peaks[i][0], near_peaks[i][1])
            shadow_end = (near_peaks[i+1][0], near_peaks[i+1][1])
            # Sombra à direita
            draw.line([shadow_start, shadow_end], fill=(80, 110, 80), width=2)
        
        # Sol
        sun_x = random.randint(3 * w // 4, 4 * w // 5)
        sun_y = random.randint(h // 8, h // 4)
        sun_size = 10
        draw.ellipse(
            [(sun_x - sun_size, sun_y - sun_size),
             (sun_x + sun_size, sun_y + sun_size)],
            fill=(255, 235, 150)
        )
    
    def generate_fluid_audio(self, duration=60, sample_rate=44100, output_path="lofi_audio_fluid.wav", seed=None):
        """Gera áudio LOFI ultra fluido e suave com variação aleatória"""
        import wave as wave_module
        
        # Usa seed para variar entre vídeos (baseado em timestamp se não fornecido)
        if seed is None:
            import time
            seed = int(time.time() * 1000) % 1000000
        random.seed(seed)
        np.random.seed(seed)
        
        # Escalas pentatônicas variadas
        pentatonic_scales = [
            [220, 247, 277, 311, 370, 415, 466, 523, 587, 659, 740, 831],  # Dó maior
            [233, 262, 294, 330, 392, 440, 494, 523, 587, 659, 784, 880],  # Ré maior
            [196, 220, 247, 277, 330, 370, 415, 466, 523, 587, 659, 740],  # Lá menor
            [207, 233, 262, 294, 349, 392, 440, 494, 523, 587, 698, 784],  # Si menor
        ]
        pentatonic_scale = random.choice(pentatonic_scales)
        
        # MUITAS progressões de acordes distintas (15 diferentes!)
        chord_progressions_options = [
            # 1-5: Progressões clássicas
            [[220, 262, 329, 370], [174, 220, 262, 329], [131, 165, 196, 262], [196, 247, 294, 392]],  # Am-F-C-G
            [[165, 196, 247, 294], [131, 165, 196, 262], [196, 247, 294, 392], [147, 175, 220, 294]],  # Em-C-G-D
            [[174, 220, 262, 329], [196, 247, 294, 392], [220, 262, 329, 370], [131, 165, 196, 262]],  # F-G-Am-C
            # 6-10: Progressões melancólicas
            [[147, 175, 220, 262], [233, 277, 349, 415], [174, 220, 262, 329], [131, 165, 196, 262]],  # Dm-Bb-F-C
            [[220, 262, 329, 370], [147, 175, 220, 262], [196, 247, 294, 392], [131, 165, 196, 262]],  # Am-Dm-G-C
            [[165, 196, 247, 294], [233, 277, 349, 415], [220, 262, 329, 370], [174, 220, 262, 329]],  # Em-Bb-Am-F
            # 11-15: Progressões alternativas/experimentais
            [[196, 247, 294, 392], [147, 175, 220, 262], [233, 277, 349, 415], [131, 165, 196, 262]],  # G-Dm-Bb-C
            [[220, 262, 329, 370], [196, 247, 294, 392], [147, 175, 220, 262], [174, 220, 262, 329]],  # Am-G-Dm-F
            [[131, 165, 196, 262], [220, 262, 329, 370], [196, 247, 294, 392], [174, 220, 262, 329]],  # C-Am-G-F
            [[147, 175, 220, 262], [131, 165, 196, 262], [174, 220, 262, 329], [196, 247, 294, 392]],  # Dm-C-F-G
            [[233, 277, 349, 415], [174, 220, 262, 329], [196, 247, 294, 392], [220, 262, 329, 370]],  # Bb-F-G-Am
            [[165, 196, 247, 294], [147, 175, 220, 262], [131, 165, 196, 262], [174, 220, 262, 329]],  # Em-Dm-C-F
            [[220, 262, 329, 370], [233, 277, 349, 415], [196, 247, 294, 392], [147, 175, 220, 262]],  # Am-Bb-G-Dm
            [[196, 247, 294, 392], [220, 262, 329, 370], [174, 220, 262, 329], [131, 165, 196, 262]],  # G-Am-F-C
            [[174, 220, 262, 329], [147, 175, 220, 262], [220, 262, 329, 370], [196, 247, 294, 392]],  # F-Dm-Am-G
        ]
        chord_progressions = random.choice(chord_progressions_options)
        
        samples = int(duration * sample_rate)
        t = np.linspace(0, duration, samples)
        audio = np.zeros(samples)
        
        # Escolhe ESTILO diferente (dramaticamente distintos)
        style = random.choice(['minimal', 'classic', 'energetic', 'melancholic', 'ambient', 'jazzy'])
        
        print(f"   🎨 Estilo escolhido: {style}")
        
        # BPM variado MUITO mais (cada estilo tem range diferente)
        if style == 'minimal':
            bpm = random.randint(55, 70)  # Muito lento e relaxante
        elif style == 'ambient':
            bpm = random.randint(60, 75)  # Lento e atmosférico
        elif style == 'melancholic':
            bpm = random.randint(65, 80)  # Lento-médio melancólico
        elif style == 'classic':
            bpm = random.randint(75, 90)  # Médio clássico
        elif style == 'jazzy':
            bpm = random.randint(80, 100)  # Mais rápido e animado
        else:  # energetic
            bpm = random.randint(85, 110)  # Rápido e energético
        
        beat_duration = 60.0 / bpm
        num_beats = int(duration / beat_duration)
        
        # Pad atmosférico - varia MUITO dependendo do estilo
        print("   🎵 Gerando pad atmosférico...")
        if style == 'minimal':
            pad_level = random.uniform(0.03, 0.06)  # Bem suave
        elif style == 'ambient':
            pad_level = random.uniform(0.08, 0.15)  # Mais presente
        elif style == 'energetic':
            pad_level = random.uniform(0.10, 0.18)  # Mais volume
        else:
            pad_level = random.uniform(0.06, 0.12)  # Padrão
        
        # Divide em chunks de 3-5 segundos (variável) para mudar acordes
        chunk_duration = random.uniform(3.5, 5.0)
        chunk_size = int(chunk_duration * sample_rate)
        num_chunks = int(np.ceil(len(t) / chunk_size))
        
        # Escolhe ordem de acordes (pode variar)
        chord_order = list(range(len(chord_progressions))) * (num_chunks // len(chord_progressions) + 1)
        random.shuffle(chord_order[:num_chunks])  # Embaralha para variar ordem
        
        for chunk_idx in range(num_chunks):
            chunk_start = chunk_idx * chunk_size
            chunk_end = min(chunk_start + chunk_size, len(t))
            chunk_time = t[chunk_start:chunk_end]
            
            chord = chord_progressions[chord_order[chunk_idx] % len(chord_progressions)]
            
            # Variação no timbre do pad (mais brilhante ou mais suave)
            harmonic_ratio = random.uniform(0.2, 0.4)
            
            for freq in chord:
                # Onda senoidal com harmônicos variados (vetorizado)
                wave_1 = np.sin(2 * np.pi * freq * chunk_time)
                wave_2 = harmonic_ratio * np.sin(2 * np.pi * freq * 2 * chunk_time)
                audio[chunk_start:chunk_end] += pad_level * (wave_1 + wave_2) / len(chord)
        
        # Padrão de batidas COMPLETAMENTE diferente por estilo
        print("   🎵 Adicionando batidas...")
        
        if style == 'minimal':
            # Mínimo - quase sem batidas
            kick_interval = random.choice([32, 64])  # Muito raro
            kick_volume = random.uniform(0.03, 0.06)
            kick_freq = random.uniform(50, 65)
            snare_interval = 999  # Quase nunca
            snare_volume = 0.01
        elif style == 'ambient':
            # Ambient - batidas muito suaves e espaçadas
            kick_interval = random.choice([16, 24])
            kick_volume = random.uniform(0.04, 0.08)
            kick_freq = random.uniform(55, 70)
            snare_interval = random.choice([64, 128])
            snare_volume = random.uniform(0.02, 0.04)
        elif style == 'energetic':
            # Energetic - batidas mais presentes e frequentes
            kick_interval = random.choice([4, 8])  # Mais frequente
            kick_volume = random.uniform(0.10, 0.18)
            kick_freq = random.uniform(60, 75)
            snare_interval = random.choice([8, 16])
            snare_volume = random.uniform(0.06, 0.12)
        elif style == 'jazzy':
            # Jazzy - padrão mais complexo
            kick_interval = random.choice([4, 6, 8])
            kick_volume = random.uniform(0.08, 0.14)
            kick_freq = random.uniform(58, 72)
            snare_interval = random.choice([8, 12, 16])
            snare_volume = random.uniform(0.05, 0.10)
        else:  # classic ou melancholic
            # Clássico - padrão médio
            kick_interval = random.choice([8, 12, 16])
            kick_volume = random.uniform(0.06, 0.12)
            kick_freq = random.uniform(55, 70)
            snare_interval = random.choice([16, 24, 32])
            snare_volume = random.uniform(0.03, 0.06)
        
        snare_freq1 = random.uniform(180, 220)
        snare_freq2 = random.uniform(380, 420)
        
        for beat in range(num_beats):
            beat_time = beat * beat_duration
            beat_idx = int(beat_time * sample_rate)
            
            # Kick
            if beat % kick_interval == 0:
                kick_samples = int(random.uniform(0.08, 0.20) * sample_rate)
                kick_end = min(beat_idx + kick_samples, samples)
                
                if kick_end > beat_idx:
                    kick_time = np.arange(0, kick_end - beat_idx) / sample_rate
                    decay = random.uniform(15, 35) if style != 'energetic' else random.uniform(20, 40)
                    kick = kick_volume * np.sin(2 * np.pi * kick_freq * kick_time) * \
                           np.exp(-kick_time * decay)
                    audio[beat_idx:kick_end] += kick
            
            # Snare/hihat
            if style != 'minimal' and beat % snare_interval == (snare_interval // 2 if snare_interval < 100 else 4):
                snare_samples = int(random.uniform(0.04, 0.10) * sample_rate)
                snare_end = min(beat_idx + snare_samples, samples)
                
                if snare_end > beat_idx:
                    snare_time = np.arange(0, snare_end - beat_idx) / sample_rate
                    snare = snare_volume * (np.sin(2 * np.pi * snare_freq1 * snare_time) + 
                                           np.sin(2 * np.pi * snare_freq2 * snare_time)) * \
                           np.exp(-snare_time * random.uniform(40, 70))
                    audio[beat_idx:snare_end] += snare
        
        # Melodias - MUITO diferente por estilo
        print("   🎵 Adicionando melodias...")
        melody_start_times = []
        
        if style == 'minimal':
            melody_interval = random.uniform(12, 20)  # Muito espaçado
            melody_volume = random.uniform(0.03, 0.06)  # Bem suave
            melody_duration_range = (1.5, 3.5)
        elif style == 'ambient':
            melody_interval = random.uniform(8, 15)
            melody_volume = random.uniform(0.05, 0.09)
            melody_duration_range = (3.0, 6.0)
        elif style == 'energetic':
            melody_interval = random.uniform(4, 8)  # Mais frequente
            melody_volume = random.uniform(0.08, 0.14)  # Mais presente
            melody_duration_range = (2.0, 4.5)
        elif style == 'jazzy':
            melody_interval = random.uniform(3, 6)  # Muito frequente
            melody_volume = random.uniform(0.10, 0.16)
            melody_duration_range = (1.5, 3.5)
        else:  # classic ou melancholic
            melody_interval = random.uniform(6, 12)
            melody_volume = random.uniform(0.05, 0.10)
            melody_duration_range = (2.5, 5.0)
        
        for i in range(int(duration / melody_interval)):
            start_time = i * melody_interval + random.uniform(0, melody_interval / 2)
            melody_start_times.append(start_time)
        
        for start_time in melody_start_times:
            melody_duration = random.uniform(*melody_duration_range)
            melody_samples = int(melody_duration * sample_rate)
            start_idx = int(start_time * sample_rate)
            end_idx = min(start_idx + melody_samples, samples)
            
            if end_idx > start_idx:
                melody_time = np.arange(0, end_idx - start_idx) / sample_rate
                
                # Número de notas varia por estilo
                if style == 'minimal':
                    num_notes = random.randint(2, 4)  # Poucas notas
                elif style == 'jazzy' or style == 'energetic':
                    num_notes = random.randint(5, 8)  # Mais notas
                else:
                    num_notes = random.randint(3, 6)
                
                # Escolhe notas - diferentes estratégias por estilo
                if style == 'jazzy':
                    # Notas rápidas e sequenciais
                    scale_indices = list(range(len(pentatonic_scale)))
                    random.shuffle(scale_indices)
                    selected_notes = [pentatonic_scale[i] for i in scale_indices[:num_notes]]
                elif style == 'energetic':
                    # Notas mais altas e brilhantes
                    high_notes = [f for f in pentatonic_scale if f > 400]
                    selected_notes = random.sample(high_notes if len(high_notes) >= num_notes else pentatonic_scale, 
                                                   min(num_notes, len(pentatonic_scale)))
                elif style == 'ambient':
                    # Notas longas e sustentadas
                    selected_notes = random.sample(pentatonic_scale, min(num_notes, len(pentatonic_scale)))
                elif random.random() < 0.5:
                    scale_indices = list(range(len(pentatonic_scale)))
                    random.shuffle(scale_indices)
                    selected_notes = [pentatonic_scale[i] for i in scale_indices[:num_notes]]
                else:
                    selected_notes = random.sample(pentatonic_scale, min(num_notes, len(pentatonic_scale)))
                
                for note_idx in range(num_notes):
                    note_start = int(note_idx * melody_samples / num_notes)
                    note_end = int((note_idx + 1) * melody_samples / num_notes)
                    
                    if note_end <= len(melody_time) and note_idx < len(selected_notes):
                        note_time = melody_time[note_start:note_end]
                        note_freq = selected_notes[note_idx]
                        
                        # Nota com envelope suave (attack e release variável)
                        envelope = np.ones(len(note_time))
                        fade_samples = int(random.uniform(0.08, 0.15) * sample_rate)
                        if len(envelope) > fade_samples * 2:
                            envelope[:fade_samples] = np.linspace(0, 1, fade_samples)
                            envelope[-fade_samples:] = np.linspace(1, 0, fade_samples)
                        
                        # Timbre varia muito por estilo
                        if style == 'jazzy' or style == 'energetic':
                            # Mais brilhante com harmônicos
                            wave = np.sin(2 * np.pi * note_freq * note_time)
                            wave += 0.3 * np.sin(2 * np.pi * note_freq * 2 * note_time)
                            if style == 'jazzy':
                                wave += 0.15 * np.sin(2 * np.pi * note_freq * 3 * note_time)
                        elif style == 'ambient':
                            # Mais suave e atmosférico
                            wave = np.sin(2 * np.pi * note_freq * note_time)
                            wave += 0.1 * np.sin(2 * np.pi * note_freq * 2 * note_time)
                        else:
                            # Padrão com chance de harmônico
                            wave = np.sin(2 * np.pi * note_freq * note_time)
                            if random.random() < 0.3:
                                wave += 0.2 * np.sin(2 * np.pi * note_freq * 2 * note_time)
                        
                        note = melody_volume * wave * envelope
                        audio[start_idx + note_start:start_idx + note_end] += note
        
        # Ruído de vinil - varia muito por estilo
        print("   🎵 Finalizando mix...")
        if style == 'minimal' or style == 'ambient':
            vinyl_amount = random.uniform(0.005, 0.012)  # Mais ruído para atmosfera
        elif style == 'jazzy':
            vinyl_amount = random.uniform(0.002, 0.006)  # Menos ruído, mais limpo
        else:
            vinyl_amount = random.uniform(0.003, 0.008)
        vinyl_noise = np.random.normal(0, vinyl_amount, samples)
        audio += vinyl_noise
        
        # Filtro passa-baixa - MUITO diferente por estilo
        from scipy import signal
        if len(audio) > 0:
            nyquist = sample_rate / 2
            if style == 'jazzy' or style == 'energetic':
                # Mais brilhante (corte mais alto)
                cutoff_freq = random.uniform(9000, 12000)
            elif style == 'minimal' or style == 'ambient':
                # Mais "warm" e suave (corte mais baixo)
                cutoff_freq = random.uniform(5000, 8000)
            else:
                # Padrão
                cutoff_freq = random.uniform(7000, 10000)
            cutoff = cutoff_freq / nyquist
            b, a = signal.butter(2, cutoff, btype='low')
            audio = signal.filtfilt(b, a, audio)
        
        # Normaliza - volume varia por estilo
        print("   🎵 Normalizando áudio...")
        if np.max(np.abs(audio)) > 0:
            if style == 'energetic' or style == 'jazzy':
                final_volume = random.uniform(0.60, 0.75)  # Mais alto
            elif style == 'minimal':
                final_volume = random.uniform(0.45, 0.55)  # Mais suave
            else:
                final_volume = random.uniform(0.55, 0.65)  # Padrão
            audio = audio / np.max(np.abs(audio)) * final_volume
        
        # Salva
        with wave_module.open(output_path, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            audio_int16 = (audio * 32767).astype(np.int16)
            wav_file.writeframes(audio_int16.tobytes())
        
        print(f"✅ Áudio fluido e suave gerado: {output_path}")
        return output_path


def generate_lofi_image(width=1920, height=1080, output_path="lofi_image.png"):
    gen = LofiUltraGenerator()
    return gen.generate_ultra_scene(width, height, output_path)


def generate_lofi_audio(duration=60, sample_rate=44100, output_path="lofi_audio.wav"):
    gen = LofiUltraGenerator()
    return gen.generate_fluid_audio(duration, sample_rate, output_path)


if __name__ == "__main__":
    print("🎵 Gerador LOFI Ultra")
    print("=" * 40)
    
    gen = LofiUltraGenerator()
    
    # Gera cena ultra
    img_path = gen.generate_ultra_scene(output_path="lofi_ultra_scene.png")
    
    # Gera áudio ultra
    audio_path = gen.generate_fluid_audio(duration=60, output_path="lofi_fluid_audio.wav")
    
    print("\n✅ Recursos ultra detalhados gerados!")

