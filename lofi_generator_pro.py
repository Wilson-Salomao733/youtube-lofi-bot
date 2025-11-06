"""
Gerador PROFISSIONAL de Vídeos LOFI
Versão melhorada com mais elementos visuais e áudio refinado
"""
import os
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import math


class LofiGeneratorPro:
    """Gerador profissional de conteúdo LOFI"""
    
    def __init__(self):
        self.color_palettes = [
            # Rosa para bege
            {"bg1": (255, 182, 193), "bg2": (255, 228, 181), 
             "accent": (255, 105, 180), "text": (139, 69, 19)},
            # Azul claro
            {"bg1": (240, 248, 255), "bg2": (255, 240, 245),
             "accent": (70, 130, 180), "text": (105, 105, 105)},
            # Bege para pêssego
            {"bg1": (255, 245, 238), "bg2": (255, 228, 196),
             "accent": (255, 165, 0), "text": (160, 82, 45)},
            # Cyan claro
            {"bg1": (230, 255, 255), "bg2": (255, 250, 240),
             "accent": (0, 191, 255), "text": (72, 61, 139)},
            # Tons quentes
            {"bg1": (255, 248, 220), "bg2": (255, 218, 185),
             "accent": (255, 69, 0), "text": (139, 69, 19)},
        ]
    
    def generate_professional_image(self, width=1920, height=1080, output_path="lofi_image_pro.png"):
        """Gera imagem LOFI profissional com gradiente, elementos e profundidade"""
        
        # Seleciona paleta aleatória
        palette = random.choice(self.color_palettes)
        
        # Cria a imagem base
        img = Image.new('RGB', (width, height), palette["bg1"])
        draw = ImageDraw.Draw(img)
        
        # Cria gradiente radial simulado
        center_x, center_y = width // 2, height // 2
        max_dist = math.sqrt(center_x**2 + center_y**2)
        
        for y in range(height):
            for x in range(width):
                # Distância do centro
                dist = math.sqrt((x - center_x)**2 + (y - center_y)**2)
                ratio = min(dist / max_dist, 1.0)
                
                # Interpola entre cores
                r = int(palette["bg1"][0] * (1 - ratio) + palette["bg2"][0] * ratio)
                g = int(palette["bg1"][1] * (1 - ratio) + palette["bg2"][1] * ratio)
                b = int(palette["bg1"][2] * (1 - ratio) + palette["bg2"][2] * ratio)
                
                img.putpixel((x, y), (r, g, b))
        
        # Desenha janela arquitetônica (elemento clássico LOFI)
        window_width = width // 3
        window_height = height // 2.5
        window_x = (width - window_width) // 2
        window_y = height // 8
        
        # Moldura da janela
        frame_thickness = 12
        draw.rectangle(
            [(window_x, window_y), (window_x + window_width, window_y + window_height)],
            outline=(100, 100, 100), width=frame_thickness
        )
        
        # Cruzamento da janela (vidros)
        draw.line(
            [(window_x + window_width // 2, window_y), 
             (window_x + window_width // 2, window_y + window_height)],
            fill=(150, 150, 150), width=8
        )
        draw.line(
            [(window_x, window_y + window_height // 2), 
             (window_x + window_width, window_y + window_height // 2)],
            fill=(150, 150, 150), width=8
        )
        
        # Astro (sol/lua) no céu da janela
        astro_x = window_x + window_width // 2
        astro_y = window_y + window_height // 3
        astro_radius = min(window_width, window_height) // 8
        
        # Decidir se é sol ou lua
        is_sun = random.random() < 0.6
        
        if is_sun:
            # Desenha sol com raios
            draw.ellipse(
                [(astro_x - astro_radius, astro_y - astro_radius),
                 (astro_x + astro_radius, astro_y + astro_radius)],
                fill=(255, 253, 208), outline=(255, 200, 100), width=2
            )
            # Raios do sol
            for i in range(8):
                angle = (i * 45) * math.pi / 180
                x1 = astro_x + (astro_radius + 15) * math.cos(angle)
                y1 = astro_y + (astro_radius + 15) * math.sin(angle)
                x2 = astro_x + (astro_radius + 25) * math.cos(angle)
                y2 = astro_y + (astro_radius + 25) * math.sin(angle)
                draw.line([(x1, y1), (x2, y2)], fill=(255, 200, 100), width=2)
        else:
            # Desenha lua
            draw.ellipse(
                [(astro_x - astro_radius, astro_y - astro_radius),
                 (astro_x + astro_radius, astro_y + astro_radius)],
                fill=(255, 255, 255), outline=(200, 200, 200), width=2
            )
            # Sombra da lua
            draw.ellipse(
                [(astro_x - astro_radius * 0.6, astro_y - astro_radius * 0.6),
                 (astro_x + astro_radius * 0.3, astro_y + astro_radius * 0.3)],
                fill=(220, 220, 220)
            )
        
        # Nuvens sutis
        for _ in range(random.randint(2, 4)):
            cloud_x = random.randint(0, width)
            cloud_y = random.randint(height // 12, height // 3)
            cloud_width = random.randint(100, 200)
            cloud_height = random.randint(30, 50)
            
            # Cria forma de nuvem com múltiplos círculos
            for i in range(3):
                offset_x = random.randint(-20, 20)
                offset_y = random.randint(-10, 10)
                size = cloud_width // 3
                draw.ellipse(
                    [(cloud_x + offset_x - size, cloud_y + offset_y - cloud_height // 2),
                     (cloud_x + offset_x + size, cloud_y + offset_y + cloud_height // 2)],
                    fill=(240, 240, 240), outline=(220, 220, 220), width=1
                )
        
        # Plantas minimalistas na janela
        plant_positions = [
            (window_x + window_width // 4, window_y + window_height),
            (window_x + 3 * window_width // 4, window_y + window_height),
        ]
        
        for px, py in plant_positions:
            # Vaso
            vase_width = 40
            vase_height = 60
            draw.rectangle(
                [(px - vase_width // 2, py), (px + vase_width // 2, py + vase_height)],
                fill=(139, 69, 19), outline=(101, 67, 33), width=2
            )
            
            # Folhas
            for i in range(3):
                leaf_x = px + random.randint(-30, 30)
                leaf_y = py - random.randint(10, 50)
                draw.ellipse(
                    [(leaf_x - 20, leaf_y - 20), (leaf_x + 20, leaf_y + 20)],
                    fill=(144, 238, 144), outline=(85, 200, 85), width=1
                )
        
        # Linhas decorativas horizontais
        for i in range(random.randint(3, 5)):
            line_y = height * (0.65 + i * 0.08)
            line_length = random.randint(width // 3, width * 2 // 3)
            line_start = (width - line_length) // 2
            
            # Linha com pequena variação de altura
            variance = random.randint(-3, 3)
            for j in range(line_length):
                point_y = line_y + math.sin(j / 10) * variance
                draw.rectangle(
                    [(line_start + j, point_y), (line_start + j + 1, point_y + 2)],
                    fill=(100 + i * 15, 100 + i * 15, 100 + i * 15)
                )
        
        # Adiciona granulado (grain) para efeito vintage
        self._add_film_grain(img, intensity=0.1)
        
        # Aplica leve blur para suavizar
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # Salva
        img.save(output_path, quality=95)
        print(f"✅ Imagem LOFI profissional gerada: {output_path}")
        return output_path
    
    def _add_film_grain(self, img, intensity=0.1):
        """Adiciona granulado vintage à imagem"""
        pixels = np.array(img)
        noise = np.random.normal(0, intensity * 255, pixels.shape)
        noisy_pixels = np.clip(pixels + noise, 0, 255)
        
        for i in range(img.height):
            for j in range(img.width):
                img.putpixel((j, i), tuple(noisy_pixels[i, j].astype(int)))
    
    def generate_professional_audio(self, duration=60, sample_rate=44100, 
                                     output_path="lofi_audio_pro.wav"):
        """Gera áudio LOFI profissional com múltiplas camadas"""
        import wave
        
        # Frequências musicais (escala menor harmônica)
        scale = {
            'C': 261.63,  # Dó
            'C#': 277.18,
            'D': 293.66,  # Ré
            'D#': 311.13,
            'E': 329.63,  # Mi
            'F': 349.23,  # Fá
            'F#': 369.99,
            'G': 392.00,  # Sol
            'G#': 415.30,
            'A': 440.00,  # Lá
            'A#': 466.16,
            'B': 493.88,  # Si
        }
        
        # Acorde LOFI típico (Dó menor)
        chord = [scale['C'], scale['D#'], scale['G']]
        
        samples = int(duration * sample_rate)
        t = np.linspace(0, duration, samples)
        
        # Inicializa o áudio
        audio = np.zeros(samples)
        
        # BPM LOFI (85 BPM)
        bpm = 85
        beat_duration = 60.0 / bpm
        beats_per_bar = 4
        
        # Gera cada batida
        num_beats = int(duration / beat_duration)
        
        for beat in range(num_beats):
            beat_time = beat * beat_duration
            beat_start = int(beat_time * sample_rate)
            beat_end = min(int((beat_time + beat_duration) * sample_rate), samples)
            
            # Kick (batida 1)
            if beat % beats_per_bar == 0:
                kick_samples = min(len(t) - beat_start, beat_end - beat_start)
                kick_time = t[beat_start:beat_start + kick_samples] - beat_time
                
                # Kick principal
                kick_audio = 0.3 * np.sin(2 * np.pi * 60 * kick_time) * \
                            np.exp(-kick_time * 25)
                
                # Sub-bass
                sub_bass = 0.2 * np.sin(2 * np.pi * 40 * kick_time) * \
                          np.exp(-kick_time * 15)
                
                if beat_start + len(kick_audio) <= len(audio):
                    audio[beat_start:beat_start + len(kick_audio)] += kick_audio + sub_bass
            
            # Snare (batidas 2 e 4)
            elif beat % beats_per_bar == 2 or beat % beats_per_bar == 0:
                snare_samples = min(len(t) - beat_start, beat_end - beat_start)
                snare_time = t[beat_start:beat_start + snare_samples] - beat_time
                
                snare_audio = np.zeros(snare_samples)
                for freq in [200, 300, 400]:
                    snare_audio += 0.12 * np.sin(2 * np.pi * freq * snare_time) * \
                                  np.exp(-snare_time * 35)
                
                if beat_start + len(snare_audio) <= len(audio):
                    audio[beat_start:beat_start + len(snare_audio)] += snare_audio
            
            # Hi-hat leve
            elif beat % beats_per_bar in [1, 3]:
                hihat_samples = min(len(t) - beat_start, beat_end - beat_start)
                hihat_time = t[beat_start:beat_start + hihat_samples] - beat_time
                
                hihat_audio = 0.04 * np.sin(2 * np.pi * 1000 * hihat_time) * \
                             np.exp(-hihat_time * 150)
                
                if beat_start + len(hihat_audio) <= len(audio):
                    audio[beat_start:beat_start + len(hihat_audio)] += hihat_audio
            
            # Melodia suave (a cada 4 batidas)
            if beat % (beats_per_bar * 2) == 0 and beat_start < len(audio):
                melody_note = random.choice(chord)
                melody_samples = int(beat_duration * 4 * sample_rate)
                melody_samples = min(melody_samples, samples - beat_start)
                melody_time = t[beat_start:beat_start + melody_samples] - beat_time
                
                melody = 0.08 * np.sin(2 * np.pi * melody_note * melody_time) * \
                        (1 + 0.3 * np.sin(2 * np.pi * melody_note * 2 * melody_time)) * \
                        np.exp(-melody_time * 1.5)
                
                if beat_start + len(melody) <= len(audio):
                    audio[beat_start:beat_start + len(melody)] += melody
        
        # Adiciona reverb simples
        audio = self._apply_reverb(audio, sample_rate)
        
        # Normaliza
        if np.max(np.abs(audio)) > 0:
            audio = audio / np.max(np.abs(audio)) * 0.7
        
        # Salva WAV
        with wave.open(output_path, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            audio_int16 = (audio * 32767).astype(np.int16)
            wav_file.writeframes(audio_int16.tobytes())
        
        print(f"✅ Áudio LOFI profissional gerado: {output_path}")
        return output_path
    
    def _apply_reverb(self, audio, sample_rate, room_size=0.3):
        """Aplica reverb simples"""
        reverb_delay = int(0.03 * sample_rate)  # 30ms delay
        reverb = np.zeros(len(audio))
        
        for i in range(reverb_delay, len(audio)):
            reverb[i] = audio[i - reverb_delay] * room_size
        
        return audio + reverb


# Função global para compatibilidade
def generate_lofi_image(width=1920, height=1080, output_path="lofi_image.png"):
    gen = LofiGeneratorPro()
    return gen.generate_professional_image(width, height, output_path)


def generate_lofi_audio(duration=60, sample_rate=44100, output_path="lofi_audio.wav"):
    gen = LofiGeneratorPro()
    return gen.generate_professional_audio(duration, sample_rate, output_path)


if __name__ == "__main__":
    print("🎵 Gerador LOFI Profissional")
    print("=" * 40)
    
    gen = LofiGeneratorPro()
    
    # Gera imagem profissional
    img_path = gen.generate_professional_image(output_path="lofi_pro_image.png")
    
    # Gera áudio profissional
    audio_path = gen.generate_professional_audio(duration=60, output_path="lofi_pro_audio.wav")
    
    print("\n✅ Recursos profissionais gerados!")

