"""
Gerador AVANÇADO de Vídeos LOFI
Com cenas variadas (florestas, cidades, paisagens) e música fluida
"""
import os
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import math


class LofiAdvancedGenerator:
    """Gerador avançado com cenas e música fluida"""
    
    def __init__(self):
        self.scene_types = ['forest', 'city', 'mountain', 'beach', 'urban']
        self.color_palettes = {
            'forest': [(34, 139, 34), (107, 142, 35), (85, 107, 47), (124, 252, 0)],
            'city': [(70, 130, 180), (119, 136, 153), (105, 105, 105), (220, 220, 220)],
            'mountain': [(176, 196, 222), (255, 228, 196), (230, 230, 250), (255, 250, 240)],
            'beach': [(173, 216, 230), (255, 228, 181), (240, 255, 255), (255, 250, 240)],
            'urban': [(169, 169, 169), (211, 211, 211), (220, 220, 220), (255, 245, 238)]
        }
    
    def generate_scene(self, width=1920, height=1080, output_path="lofi_scene.png"):
        """Gera cena aleatória"""
        scene_type = random.choice(self.scene_types)
        
        if scene_type == 'forest':
            return self._generate_forest_scene(width, height, output_path)
        elif scene_type == 'city':
            return self._generate_city_scene(width, height, output_path)
        elif scene_type == 'mountain':
            return self._generate_mountain_scene(width, height, output_path)
        elif scene_type == 'beach':
            return self._generate_beach_scene(width, height, output_path)
        else:  # urban
            return self._generate_urban_scene(width, height, output_path)
    
    def _generate_forest_scene(self, width, height, output_path):
        """Cena de floresta minimalista"""
        img = Image.new('RGB', (width, height), (135, 206, 250))
        draw = ImageDraw.Draw(img)
        
        # Céu com gradiente
        for y in range(height // 3):
            ratio = y / (height // 3)
            sky_color = (
                int(135 * (1 - ratio) + 255 * ratio),
                int(206 * (1 - ratio) + 248 * ratio),
                int(250 * (1 - ratio) + 255 * ratio)
            )
            draw.line([(0, y), (width, y)], fill=sky_color)
        
        # Árvores em camadas (perspectiva)
        num_trees = 15
        for i in range(num_trees):
            tree_x = width * (i + random.random()) / num_trees
            tree_width = random.randint(40, 80)
            tree_height = random.randint(200, 400)
            tree_bottom = height - random.randint(0, 100)
            
            # Tronco
            trunk_width = tree_width // 3
            trunk_color = (139, 69, 19)
            draw.ellipse(
                [(tree_x - trunk_width, tree_bottom - tree_height),
                 (tree_x + trunk_width, tree_bottom - tree_height // 3)],
                fill=trunk_color
            )
            
            # Copa da árvore
            crown_width = tree_width
            crown_height = tree_height // 2
            crown_colors = [
                (34, 139, 34), (46, 125, 50), (56, 178, 172), (76, 175, 80)
            ]
            draw.ellipse(
                [(tree_x - crown_width, tree_bottom - tree_height - crown_height // 2),
                 (tree_x + crown_width, tree_bottom - tree_height // 2)],
                fill=random.choice(crown_colors)
            )
        
        # Nuvens sutis
        for _ in range(3):
            cloud_x = random.randint(0, width)
            cloud_y = random.randint(50, height // 4)
            cloud_w = random.randint(100, 200)
            for _ in range(5):
                offset_x = random.randint(-30, 30)
                offset_y = random.randint(-20, 20)
                draw.ellipse(
                    [(cloud_x + offset_x - cloud_w // 5, cloud_y + offset_y),
                     (cloud_x + offset_x + cloud_w // 5, cloud_y + offset_y + 40)],
                    fill=(240, 240, 240)
                )
        
        # Sol/lua
        astro_x = width * random.uniform(0.2, 0.8)
        astro_y = height * random.uniform(0.05, 0.25)
        astro_radius = random.randint(40, 60)
        draw.ellipse(
            [(astro_x - astro_radius, astro_y - astro_radius),
             (astro_x + astro_radius, astro_y + astro_radius)],
            fill=(255, 253, 208)
        )
        
        img.save(output_path, quality=95)
        print(f"✅ Cena de floresta gerada: {output_path}")
        return output_path
    
    def _generate_city_scene(self, width, height, output_path):
        """Vista de cidade minimalista"""
        # Noite com estrelas
        img = Image.new('RGB', (width, height), (25, 25, 50))
        draw = ImageDraw.Draw(img)
        
        # Estrelas
        for _ in range(150):
            x = random.randint(0, width)
            y = random.randint(0, height // 2)
            brightness = random.randint(200, 255)
            size = random.randint(1, 3)
            draw.ellipse([(x-size, y-size), (x+size, y+size)], fill=(brightness, brightness, 255))
        
        # Prédios em silhueta
        num_buildings = 20
        for i in range(num_buildings):
            building_x = width * i / num_buildings
            building_width = width / num_buildings
            building_height = random.randint(height // 3, height * 2 // 3)
            
            # Variações na altura
            if random.random() < 0.7:
                building_height = random.randint(height // 2, height * 3 // 4)
            
            draw.rectangle(
                [(building_x, height - building_height),
                 (building_x + building_width, height)],
                fill=(40, 40, 70)
            )
            
            # Janelas acesas
            if random.random() < 0.6:
                window_x = building_x + building_width // 4
                window_y = height - building_height + building_height // 4
                window_size = building_width // 4
                
                for row in range(2):
                    for col in range(2):
                        wx = building_x + col * building_width // 2 + building_width // 4
                        wy = height - building_height + row * building_height // 2 + building_height // 4
                        if random.random() < 0.7:  # Algumas janelas acesas
                            draw.rectangle(
                                [(wx, wy), (wx + window_size, wy + building_height // 5)],
                                fill=(255, 200, 100)
                            )
        
        # Lua
        moon_x = width * random.uniform(0.7, 0.9)
        moon_y = height * random.uniform(0.1, 0.2)
        moon_radius = random.randint(50, 80)
        draw.ellipse(
            [(moon_x - moon_radius, moon_y - moon_radius),
             (moon_x + moon_radius, moon_y + moon_radius)],
            fill=(255, 255, 240)
        )
        
        img.save(output_path, quality=95)
        print(f"✅ Cena de cidade gerada: {output_path}")
        return output_path
    
    def _generate_mountain_scene(self, width, height, output_path):
        """Paisagem de montanhas"""
        # Céu com gradiente
        img = Image.new('RGB', (width, height), (176, 196, 222))
        draw = ImageDraw.Draw(img)
        
        # Gradiente do céu
        for y in range(height // 2):
            ratio = y / (height // 2)
            r = int(176 * (1 - ratio) + 255 * ratio)
            g = int(196 * (1 - ratio) + 248 * ratio)
            b = int(222 * (1 - ratio) + 255 * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Montanhas em camadas
        peaks = [(0, height), (width // 3, height * 0.4), (width * 2 // 3, height * 0.6), (width, height)]
        draw.polygon(peaks, fill=(100, 130, 100))
        
        # Segunda camada de montanhas (mais distante)
        peaks2 = [(0, height), (width // 4, height * 0.5), (width * 3 // 4, height * 0.7), (width, height)]
        draw.polygon(peaks2, fill=(120, 150, 120))
        
        # Nuvens
        for _ in range(4):
            cloud_x = random.randint(0, width)
            cloud_y = random.randint(50, height // 3)
            cloud_w = random.randint(150, 250)
            for _ in range(5):
                offset_x = random.randint(-40, 40)
                offset_y = random.randint(-25, 25)
                draw.ellipse(
                    [(cloud_x + offset_x - cloud_w // 5, cloud_y + offset_y),
                     (cloud_x + offset_x + cloud_w // 5, cloud_y + offset_y + 50)],
                    fill=(240, 240, 250)
                )
        
        # Sol
        sun_x = width * random.uniform(0.7, 0.9)
        sun_y = height * random.uniform(0.2, 0.4)
        sun_radius = random.randint(40, 60)
        draw.ellipse(
            [(sun_x - sun_radius, sun_y - sun_radius),
             (sun_x + sun_radius, sun_y + sun_radius)],
            fill=(255, 235, 150)
        )
        
        img.save(output_path, quality=95)
        print(f"✅ Cena de montanhas gerada: {output_path}")
        return output_path
    
    def _generate_beach_scene(self, width, height, output_path):
        """Cena de praia"""
        img = Image.new('RGB', (width, height), (173, 216, 230))
        draw = ImageDraw.Draw(img)
        
        # Céu
        for y in range(height // 2):
            ratio = y / (height // 2)
            sky_color = (
                int(173 * (1 - ratio) + 240 * ratio),
                int(216 * (1 - ratio) + 248 * ratio),
                int(230 * (1 - ratio) + 255 * ratio)
            )
            draw.line([(0, y), (width, y)], fill=sky_color)
        
        # Oceano
        ocean_start = height // 2
        for y in range(ocean_start, height):
            ratio = (y - ocean_start) / (height - ocean_start)
            ocean_color = (
                int(70 * (1 - ratio) + 100 * ratio),
                int(130 * (1 - ratio) + 149 * ratio),
                int(180 * (1 - ratio) + 237 * ratio)
            )
            draw.line([(0, y), (width, y)], fill=ocean_color)
        
        # Areia
        sand_start = int(height * 0.7)
        for y in range(sand_start, height):
            ratio = (y - sand_start) / (height - sand_start)
            sand_color = (
                int(238 * (1 - ratio) + 255 * ratio),
                int(203 * (1 - ratio) + 228 * ratio),
                int(173 * (1 - ratio) + 196 * ratio)
            )
            draw.line([(0, y), (width, y)], fill=sand_color)
        
        # Sol
        sun_y = height * random.uniform(0.25, 0.4)
        sun_radius = random.randint(60, 80)
        
        # Reflexo no oceano
        draw.ellipse(
            [(width // 2 - sun_radius * 2, height // 2 + 30),
             (width // 2 + sun_radius * 2, height // 2 + 100)],
            fill=(255, 245, 180)
        )
        
        draw.ellipse(
            [(width // 2 - sun_radius, sun_y - sun_radius),
             (width // 2 + sun_radius, sun_y + sun_radius)],
            fill=(255, 215, 0)
        )
        
        # Nuvens
        for _ in range(4):
            cloud_x = random.randint(0, width)
            cloud_y = random.randint(50, height // 3)
            cloud_w = random.randint(120, 200)
            for _ in range(4):
                offset_x = random.randint(-30, 30)
                offset_y = random.randint(-20, 20)
                draw.ellipse(
                    [(cloud_x + offset_x - cloud_w // 6, cloud_y + offset_y),
                     (cloud_x + offset_x + cloud_w // 6, cloud_y + offset_y + 35)],
                    fill=(240, 240, 250)
                )
        
        img.save(output_path, quality=95)
        print(f"✅ Cena de praia gerada: {output_path}")
        return output_path
    
    def _generate_urban_scene(self, width, height, output_path):
        """Cena urbana minimalista"""
        img = Image.new('RGB', (width, height), (255, 250, 240))
        draw = ImageDraw.Draw(img)
        
        # Céu claro
        for y in range(height // 3):
            ratio = y / (height // 3)
            sky_color = (
                int(176 * (1 - ratio) + 255 * ratio),
                int(196 * (1 - ratio) + 250 * ratio),
                int(222 * (1 - ratio) + 240 * ratio)
            )
            draw.line([(0, y), (width, y)], fill=sky_color)
        
        # Construções modernas
        num_buildings = 25
        for i in range(num_buildings):
            x = width * i / num_buildings
            w = width / num_buildings
            h = random.randint(height // 3, height * 2 // 3)
            
            # Tiras de cores
            color_bands = [
                (220, 220, 220), (200, 200, 200),
                (180, 180, 180), (210, 210, 210)
            ]
            
            draw.rectangle(
                [(x, height - h), (x + w, height)],
                fill=random.choice(color_bands)
            )
            
            # Janelas minimalistas
            if random.random() < 0.5:
                for row in range(3):
                    for col in range(2):
                        window_x = x + col * w / 2 + w / 4
                        window_y = height - h + row * h / 3 + h / 6
                        if random.random() < 0.6:
                            draw.rectangle(
                                [(window_x, window_y),
                                 (window_x + w / 5, window_y + h / 6)],
                                fill=(100, 149, 237) if random.random() < 0.3 else (220, 220, 220)
                            )
        
        img.save(output_path, quality=95)
        print(f"✅ Cena urbana gerada: {output_path}")
        return output_path
    
    def generate_fluid_audio(self, duration=60, sample_rate=44100, output_path="lofi_audio_fluid.wav"):
        """Gera áudio LOFI fluido e variado"""
        import wave
        
        # Escala LOFI suave (escala pentatônica)
        pentatonic_scale = [262, 294, 330, 392, 440, 523, 587, 659, 784]  # Dó, Ré, Mi, Sol, Lá
        
        samples = int(duration * sample_rate)
        t = np.linspace(0, duration, samples)
        audio = np.zeros(samples)
        
        bpm = 80  # BPM suave
        beat_duration = 60.0 / bpm
        
        for beat in range(int(duration / beat_duration)):
            beat_time = beat * beat_duration
            beat_start = int(beat_time * sample_rate)
            beat_end = min(int((beat_time + beat_duration) * sample_rate), samples)
            
            # Kick suave (nem toda batida)
            if beat % 4 == 0:
                kick_samples = beat_end - beat_start
                if kick_samples > 0:
                    kick_time = t[beat_start:beat_end] - beat_time
                    kick = 0.2 * np.sin(2 * np.pi * 50 * kick_time) * np.exp(-kick_time * 20)
                    if beat_start + len(kick) <= len(audio):
                        audio[beat_start:beat_start + len(kick)] += kick
            
            # Pad suave de fundo (sempre)
            pad_samples = beat_end - beat_start
            if pad_samples > 0:
                pad_time = t[beat_start:beat_end] - beat_time
                
                # Múltiplos tons suaves
                for freq in [220, 330, 440]:
                    pad = 0.03 * np.sin(2 * np.pi * freq * pad_time)
                    audio[beat_start:beat_end] += pad
            
            # Melodia variada (não em loop fixo)
            if random.random() < 0.3:  # 30% das vezes
                melody_samples = int(beat_duration * 2 * sample_rate)
                melody_samples = min(melody_samples, samples - beat_start)
                if melody_samples > 0:
                    melody_time = t[beat_start:beat_start + melody_samples] - beat_time
                    melody_freq = random.choice(pentatonic_scale)
                    melody = 0.06 * np.sin(2 * np.pi * melody_freq * melody_time) * \
                            (1 + 0.5 * np.sin(2 * np.pi * melody_freq * melody_time / 2)) * \
                            np.exp(-melody_time * 0.5)
                    
                    if beat_start + len(melody) <= len(audio):
                        audio[beat_start:beat_start + len(melody)] += melody
        
        # Normaliza
        if np.max(np.abs(audio)) > 0:
            audio = audio / np.max(np.abs(audio)) * 0.6
        
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
    gen = LofiAdvancedGenerator()
    return gen.generate_scene(width, height, output_path)


def generate_lofi_audio(duration=60, sample_rate=44100, output_path="lofi_audio.wav"):
    gen = LofiAdvancedGenerator()
    return gen.generate_fluid_audio(duration, sample_rate, output_path)


if __name__ == "__main__":
    print("🎵 Gerador LOFI Avançado")
    print("=" * 40)
    
    gen = LofiAdvancedGenerator()
    
    # Gera cena
    img_path = gen.generate_scene(output_path="lofi_advanced_scene.png")
    
    # Gera áudio fluido
    audio_path = gen.generate_fluid_audio(duration=60, output_path="lofi_fluid_audio.wav")
    
    print("\n✅ Recursos avançados gerados!")

