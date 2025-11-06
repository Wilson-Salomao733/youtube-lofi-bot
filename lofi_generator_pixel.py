"""
Gerador LOFI em PIXEL ART
Estilo pixelado/retro com cenas minimalistas
"""
import os
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import math


class LofiPixelGenerator:
    """Gerador LOFI com estilo pixel art"""
    
    def __init__(self):
        self.scene_types = ['forest', 'city', 'cafe', 'lake', 'urban', 'mountain']
        self.pixel_colors = {
            'sky': [(135, 206, 250), (176, 224, 230), (173, 216, 230), (240, 248, 255)],
            'forest_green': [(34, 139, 34), (46, 125, 50), (56, 178, 172), (76, 175, 80)],
            'building': [(169, 169, 169), (128, 128, 128), (105, 105, 105), (70, 130, 180)],
            'sunset': [(255, 140, 0), (255, 165, 0), (255, 192, 203), (255, 182, 193)],
            'ocean': [(70, 130, 180), (100, 149, 237), (65, 105, 225), (123, 104, 238)],
        }
    
    def generate_pixel_scene(self, width=1920, height=1080, output_path="lofi_pixel.png", pixel_size=5):
        """Gera cena pixel art com alta qualidade"""
        # Reduz resolução para efeito pixel (mais detalhes)
        pixel_width = width // pixel_size
        pixel_height = height // pixel_size
        
        # Cria imagem pequena primeiro
        img = Image.new('RGB', (pixel_width, pixel_height), (135, 206, 250))
        draw = ImageDraw.Draw(img)
        
        scene_type = random.choice(self.scene_types)
        
        if scene_type == 'forest':
            self._draw_pixel_forest(draw, pixel_width, pixel_height)
        elif scene_type == 'city':
            self._draw_pixel_city(draw, pixel_width, pixel_height)
        elif scene_type == 'cafe':
            self._draw_pixel_cafe(draw, pixel_width, pixel_height)
        elif scene_type == 'lake':
            self._draw_pixel_lake(draw, pixel_width, pixel_height)
        elif scene_type == 'urban':
            self._draw_pixel_urban(draw, pixel_width, pixel_height)
        else:  # mountain
            self._draw_pixel_mountain(draw, pixel_width, pixel_height)
        
        # Escala para tamanho final (sem suavização)
        img = img.resize((width, height), Image.NEAREST)  # NEAREST mantém pixels definidos
        
        img.save(output_path, quality=95)
        print(f"✅ Cena pixel art gerada ({scene_type}): {output_path}")
        return output_path
    
    def _draw_pixel_forest(self, draw, w, h):
        """Floresta em pixel art"""
        # Céu
        sky_color = random.choice(self.pixel_colors['sky'])
        for y in range(h // 3):
            draw.rectangle([(0, y), (w, y)], fill=sky_color)
        
        # Grama/chão
        grass_color = (76, 175, 80)
        for y in range(h * 2 // 3, h):
            draw.rectangle([(0, y), (w, y)], fill=grass_color)
        
        # Árvores (silhuetas grandes)
        tree_positions = [(w // 6, h), (w // 3, h), (w // 2, h), (2 * w // 3, h), (5 * w // 6, h)]
        
        for tree_x in tree_positions:
            tree_height = random.randint(8, 15)
            tree_width = random.randint(4, 8)
            
            # Tronco
            trunk_color = (101, 67, 33)
            draw.rectangle(
                [(tree_x, h - tree_height - 2),
                 (min(tree_x + 2, w), h)],
                fill=trunk_color
            )
            
            # Copa da árvore
            crown_color = random.choice(self.pixel_colors['forest_green'])
            draw.ellipse(
                [(max(0, tree_x - tree_width), h - tree_height - 3),
                 (min(w, tree_x + tree_width), h - 3)],
                fill=crown_color
            )
        
        # Sol/lua pixelado
        astro_x = random.randint(w // 4, 3 * w // 4)
        astro_y = random.randint(h // 8, h // 4)
        astro_size = random.randint(3, 6)
        
        if random.random() < 0.7:  # Sol
            draw.ellipse(
                [(astro_x - astro_size, astro_y - astro_size),
                 (astro_x + astro_size, astro_y + astro_size)],
                fill=(255, 235, 150)
            )
        else:  # Lua
            draw.ellipse(
                [(astro_x - astro_size, astro_y - astro_size),
                 (astro_x + astro_size, astro_y + astro_size)],
                fill=(255, 255, 240)
            )
    
    def _draw_pixel_city(self, draw, w, h):
        """Cidade noturna em pixel art"""
        # Céu escuro
        for y in range(h // 3):
            draw.rectangle([(0, y), (w, y)], fill=(25, 25, 50))
        
        # Estrelas
        for _ in range(30):
            x = random.randint(0, w)
            y = random.randint(0, h // 3)
            draw.rectangle([(x, y), (x, y)], fill=(255, 255, 255))
        
        # Prédios
        num_buildings = 12
        for i in range(num_buildings):
            x = w * i // num_buildings
            building_w = w // num_buildings
            building_h = random.randint(h // 3, h * 2 // 3)
            
            # Variação de altura
            if i % 3 == 0:
                building_h = random.randint(h // 2, h * 3 // 4)
            
            # Prédio
            draw.rectangle(
                [(x, h - building_h),
                 (x + building_w, h)],
                fill=random.choice(self.pixel_colors['building'])
            )
            
            # Janelas acesas (pixels individuais)
            for row in range(3):
                for col in range(2):
                    window_x = x + col * building_w // 2
                    window_y = h - building_h + row * building_h // 3
                    if random.random() < 0.4:
                        draw.rectangle(
                            [(window_x, window_y),
                             (window_x + 2, window_y + 2)],
                            fill=(255, 200, 100)
                        )
        
        # Lua grande
        moon_x = random.randint(3 * w // 4, 4 * w // 5)
        moon_y = random.randint(h // 8, h // 4)
        moon_size = random.randint(6, 10)
        draw.ellipse(
            [(moon_x - moon_size, moon_y - moon_size),
             (moon_x + moon_size, moon_y + moon_size)],
            fill=(255, 255, 240)
        )
    
    def _draw_pixel_cafe(self, draw, w, h):
        """Cena de café em pixel art"""
        # Céu claro
        sky_color = random.choice(self.pixel_colors['sky'])
        for y in range(h // 2):
            draw.rectangle([(0, y), (w, y)], fill=sky_color)
        
        # Paredes do café (lado esquerdo)
        cafe_x = 0
        cafe_w = w // 3
        cafe_h = h
        
        # Parede
        draw.rectangle(
            [(cafe_x, 0), (cafe_x + cafe_w, cafe_h)],
            fill=(245, 245, 220)
        )
        
        # Janelas do café
        for i in range(2):
            window_x = cafe_x + cafe_w // 4
            window_y = cafe_h // 3 + i * cafe_h // 3
            window_w = cafe_w // 2
            window_h = cafe_h // 4
            
            draw.rectangle(
                [(window_x, window_y),
                 (window_x + window_w, window_y + window_h)],
                fill=(135, 206, 250)
            )
        
        # Terraço (lado direito)
        terrace_y = h * 2 // 3
        for y in range(terrace_y, h):
            draw.rectangle([(w // 3, y), (w, y)], fill=(139, 69, 19))
        
        # Mesa e cadeiras
        table_x = w // 2
        table_y = terrace_y + 5
        
        # Mesa
        draw.rectangle(
            [(table_x - 10, table_y - 5),
             (table_x + 10, table_y)],
            fill=(101, 67, 33)
        )
        
        # Xícaras
        draw.ellipse(
            [(table_x - 8, table_y - 8),
             (table_x - 3, table_y - 3)],
            fill=(255, 255, 255)
        )
        draw.ellipse(
            [(table_x + 3, table_y - 8),
             (table_x + 8, table_y - 3)],
            fill=(255, 255, 255)
        )
        
        # Sol
        sun_x = random.randint(w // 2, 4 * w // 5)
        sun_y = random.randint(h // 10, h // 3)
        sun_size = random.randint(5, 8)
        draw.ellipse(
            [(sun_x - sun_size, sun_y - sun_size),
             (sun_x + sun_size, sun_y + sun_size)],
            fill=(255, 235, 150)
        )
    
    def _draw_pixel_lake(self, draw, w, h):
        """Lago em pixel art"""
        # Céu
        sky_color = random.choice(self.pixel_colors['sky'])
        for y in range(h // 2):
            draw.rectangle([(0, y), (w, y)], fill=sky_color)
        
        # Lago
        lake_color = random.choice(self.pixel_colors['ocean'])
        for y in range(h // 2, h):
            draw.rectangle([(0, y), (w, y)], fill=lake_color)
        
        # Folhas flutuantes
        for _ in range(8):
            leaf_x = random.randint(0, w)
            leaf_y = random.randint(h // 2 + 5, h - 10)
            leaf_size = random.randint(3, 5)
            
            draw.ellipse(
                [(leaf_x - leaf_size, leaf_y - leaf_size),
                 (leaf_x + leaf_size, leaf_y + leaf_size)],
                fill=(144, 238, 144)
            )
        
        # Árvores na margem
        for tree_x in [w // 6, w // 2, 5 * w // 6]:
            tree_h = random.randint(8, 12)
            tree_w = random.randint(4, 7)
            
            # Tronco
            draw.rectangle(
                [(tree_x, h // 2 - tree_h),
                 (tree_x + 2, h // 2)],
                fill=(139, 69, 19)
            )
            
            # Copa
            draw.ellipse(
                [(tree_x - tree_w, h // 2 - tree_h - 5),
                 (tree_x + tree_w, h // 2 - 3)],
                fill=(34, 139, 34)
            )
        
        # Sol com reflexo
        sun_x = w // 2
        sun_y = h * random.uniform(0.2, 0.3)
        sun_size = 6
        
        # Reflexo na água
        draw.ellipse(
            [(sun_x - sun_size * 2, h // 2 + 3),
             (sun_x + sun_size * 2, h // 2 + 15)],
            fill=(255, 245, 180)
        )
        
        # Sol
        draw.ellipse(
            [(sun_x - sun_size, sun_y - sun_size),
             (sun_x + sun_size, sun_y + sun_size)],
            fill=(255, 215, 0)
        )
    
    def _draw_pixel_urban(self, draw, w, h):
        """Cena urbana moderna"""
        # Céu
        sky_color = random.choice(self.pixel_colors['sky'])
        for y in range(h // 3):
            draw.rectangle([(0, y), (w, y)], fill=sky_color)
        
        # Prédios modernos (retangulares simples)
        colors = [(220, 220, 220), (200, 200, 200), (180, 180, 180), (210, 210, 210)]
        
        num_buildings = 15
        for i in range(num_buildings):
            x = w * i // num_buildings
            building_w = w // num_buildings
            building_h = random.randint(h // 2, h * 3 // 4)
            
            draw.rectangle(
                [(x, h - building_h),
                 (x + building_w, h)],
                fill=random.choice(colors)
            )
            
            # Algumas janelas coloridas
            if random.random() < 0.3:
                for row in range(2):
                    for col in range(2):
                        if random.random() < 0.4:
                            draw.rectangle(
                                [(x + col * building_w // 2, h - building_h + row * building_h // 2),
                                 (x + (col + 1) * building_w // 2 - 2, h - building_h + (row + 1) * building_h // 2)],
                                fill=(100, 149, 237)
                            )
    
    def _draw_pixel_mountain(self, draw, w, h):
        """Paisagem de montanhas"""
        # Céu gradiente
        sky_colors = [(176, 196, 222), (255, 228, 196), (240, 248, 255)]
        for y in range(h // 2):
            color = random.choice(sky_colors)
            draw.rectangle([(0, y), (w, y)], fill=color)
        
        # Montanhas em silhueta (triângulos simples)
        peaks = [
            (0, h // 2), (w // 3, h // 3), (2 * w // 3, h // 2.5), (w, h // 2)
        ]
        for i in range(len(peaks) - 1):
            # Desenha triângulo de montanha
            points = [
                peaks[i],
                peaks[i + 1],
                (peaks[i + 1][0], h)
            ]
            if i > 0:
                points.insert(1, (peaks[i][0], h))
            
            mountain_color = (100, 130, 100)
            draw.polygon(points, fill=mountain_color)
        
        # Sol
        sun_x = random.randint(3 * w // 4, 4 * w // 5)
        sun_y = random.randint(h // 6, h // 3)
        sun_size = random.randint(5, 8)
        draw.ellipse(
            [(sun_x - sun_size, sun_y - sun_size),
             (sun_x + sun_size, sun_y + sun_size)],
            fill=(255, 235, 150)
        )
    
    def generate_fluid_audio(self, duration=60, sample_rate=44100, output_path="lofi_audio_fluid.wav"):
        """Gera áudio LOFI fluido e variado"""
        import wave
        
        pentatonic_scale = [262, 294, 330, 392, 440, 523, 587, 659, 784]
        samples = int(duration * sample_rate)
        t = np.linspace(0, duration, samples)
        audio = np.zeros(samples)
        
        bpm = 75  # BPM mais lento e suave
        beat_duration = 60.0 / bpm
        
        for beat in range(int(duration / beat_duration)):
            beat_time = beat * beat_duration
            beat_start = int(beat_time * sample_rate)
            beat_end = min(int((beat_time + beat_duration) * sample_rate), samples)
            
            # Kick muito suave
            if beat % 4 == 0:
                kick_samples = beat_end - beat_start
                if kick_samples > 0:
                    kick_time = t[beat_start:beat_end] - beat_time
                    kick = 0.15 * np.sin(2 * np.pi * 45 * kick_time) * np.exp(-kick_time * 25)
                    if beat_start + len(kick) <= len(audio):
                        audio[beat_start:beat_start + len(kick)] += kick
            
            # Pad constante e suave
            pad_samples = beat_end - beat_start
            if pad_samples > 0:
                pad_time = t[beat_start:beat_end] - beat_time
                for freq in [165, 220, 330]:  # Acordes em tons baixos
                    pad = 0.02 * np.sin(2 * np.pi * freq * pad_time)
                    audio[beat_start:beat_end] += pad
            
            # Melodia esporádica e suave
            if random.random() < 0.2:  # Apenas 20% das vezes
                melody_samples = int(beat_duration * 3 * sample_rate)
                melody_samples = min(melody_samples, samples - beat_start)
                if melody_samples > 0:
                    melody_time = t[beat_start:beat_start + melody_samples] - beat_time
                    melody_freq = random.choice(pentatonic_scale)
                    melody = 0.04 * np.sin(2 * np.pi * melody_freq * melody_time) * \
                            np.exp(-melody_time * 0.3)
                    
                    if beat_start + len(melody) <= len(audio):
                        audio[beat_start:beat_start + len(melody)] += melody
        
        # Normaliza
        if np.max(np.abs(audio)) > 0:
            audio = audio / np.max(np.abs(audio)) * 0.5  # Mais suave
        
        # Salva
        with wave.open(output_path, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            audio_int16 = (audio * 32767).astype(np.int16)
            wav_file.writeframes(audio_int16.tobytes())
        
        print(f"✅ Áudio fluido gerado: {output_path}")
        return output_path


def generate_lofi_image(width=1920, height=1080, output_path="lofi_image.png"):
    gen = LofiPixelGenerator()
    return gen.generate_pixel_scene(width, height, output_path)


def generate_lofi_audio(duration=60, sample_rate=44100, output_path="lofi_audio.wav"):
    gen = LofiPixelGenerator()
    return gen.generate_fluid_audio(duration, sample_rate, output_path)


if __name__ == "__main__":
    print("🎵 Gerador LOFI Pixel Art")
    print("=" * 40)
    
    gen = LofiPixelGenerator()
    
    # Gera cena pixel art
    img_path = gen.generate_pixel_scene(output_path="lofi_pixel_scene.png")
    
    # Gera áudio fluido
    audio_path = gen.generate_fluid_audio(duration=60, output_path="lofi_fluid_audio.wav")
    
    print("\n✅ Recursos pixel art gerados!")

