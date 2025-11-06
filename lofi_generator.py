"""
Gerador de Vídeos LOFI para YouTube
Gera imagens, sons e combina tudo em vídeos
"""
import os
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import math

def generate_lofi_image(width=1920, height=1080, output_path="lofi_image.png"):
    """
    Gera uma imagem estilo LOFI com gradientes suaves e elementos mínimos
    """
    # Cores estilo LOFI (tons pastéis, quentes, suaves)
    colors = [
        [(255, 182, 193), (255, 228, 181)],  # Rosa para bege
        [(240, 248, 255), (255, 240, 245)],  # Azul claro para rosa claro
        [(255, 245, 238), (255, 228, 196)],  # Bege para pêssego
        [(230, 255, 255), (255, 250, 240)],  # Cyan claro para creme
        [(250, 235, 215), (255, 218, 185)],  # Bisque para pêssego
    ]
    
    # Seleciona cor aleatória
    color1, color2 = random.choice(colors)
    
    # Cria a imagem
    img = Image.new('RGB', (width, height), color1)
    draw = ImageDraw.Draw(img)
    
    # Desenha elementos LOFI mínimos
    # Window frame (retângulo na parte superior)
    window_color = (139, 139, 139)
    window_alpha = 100
    window_y = height // 8
    draw.rectangle(
        [(width // 4, window_y), (width * 3 // 4, window_y + height // 3)],
        outline=window_color, width=8
    )
    
    # Sun/Moon (círculo suave)
    center_x = width // 2
    center_y = window_y + height // 6
    radius = min(width, height) // 10
    
    # Desenha o círculo com gradiente simulado
    for i in range(radius, 0, -2):
        alpha = int(255 * (1 - i / radius))
        if random.random() < 0.7:  # Moon
            color = (255, 255, 255)
        else:  # Sun
            color = (255, 253, 208)
        
        draw.ellipse(
            [
                (center_x - i, center_y - i),
                (center_x + i, center_y + i)
            ],
            fill=color, outline=None
        )
    
    # Linhas decorativas minimalistas
    line_color = (180, 180, 180, 120)
    for i in range(3):
        y = height * (0.7 + i * 0.08)
        draw.rectangle(
            [(width // 6, y), (width * 5 // 6, y + 2)],
            fill=(180, 180, 180)
        )
    
    # Salva a imagem
    img.save(output_path)
    print(f"✅ Imagem LOFI gerada: {output_path}")
    return output_path


def generate_lofi_audio(duration=60, sample_rate=44100, output_path="lofi_audio.wav"):
    """
    Gera um som LOFI usando ondas senoidais
    Cria batidas suaves estilo LOFI HIP HOP
    """
    import wave
    
    # Parâmetros para o som LOFI
    # Frequências para acordes (escala menor)
    frequencies = {
        'bass': 65.41,  # C2
        'kick': [60, 80, 100],
        'snare': [200, 400, 600],
        'hihat': [800, 1200, 1600],
        'melody': [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88]  # Dó menor
    }
    
    samples = int(duration * sample_rate)
    t = np.linspace(0, duration, samples)
    
    # Inicializa o áudio
    audio = np.zeros(samples)
    
    # BPM LOFI típico (~80-90 BPM)
    bpm = 85
    beat_duration = 60.0 / bpm
    beats_per_bar = 4
    
    # Gera cada batida
    num_beats = int(duration / beat_duration)
    
    for beat in range(num_beats):
        beat_time = beat * beat_duration
        beat_start = int(beat_time * sample_rate)
        beat_end = min(int((beat_time + beat_duration) * sample_rate), samples)
        
        # Kick no 1
        if beat % beats_per_bar == 0:
            # Gera o kick
            kick_samples = min(len(t) - beat_start, beat_end - beat_start)
            kick_time = t[beat_start:beat_start + kick_samples] - beat_time
            
            # Kick com decay
            kick_audio = np.zeros(kick_samples)
            for freq in frequencies['kick']:
                kick_audio += 0.15 * np.sin(2 * np.pi * freq * kick_time) * \
                             np.exp(-kick_time * 30)
            
            # Adiciona um pouco de sub-bass
            sub_bass = 0.2 * np.sin(2 * np.pi * frequencies['bass'] * kick_time) * \
                      np.exp(-kick_time * 20)
            
            if beat_start + len(kick_audio) <= len(audio):
                audio[beat_start:beat_start + len(kick_audio)] += kick_audio
                audio[beat_start:beat_start + len(kick_audio)] += sub_bass
        
        # Snare no 2 e 4
        elif beat % beats_per_bar == 2:
            snare_samples = min(len(t) - beat_start, beat_end - beat_start)
            snare_time = t[beat_start:beat_start + snare_samples] - beat_time
            
            snare_audio = np.zeros(snare_samples)
            for freq in frequencies['snare']:
                snare_audio += 0.1 * np.sin(2 * np.pi * freq * snare_time) * \
                              np.exp(-snare_time * 40)
            
            if beat_start + len(snare_audio) <= len(audio):
                audio[beat_start:beat_start + len(snare_audio)] += snare_audio
        
        # Hi-hat leve
        else:
            hihat_samples = min(len(t) - beat_start, beat_end - beat_start)
            hihat_time = t[beat_start:beat_start + hihat_samples] - beat_time
            
            hihat_audio = np.zeros(hihat_samples)
            for freq in frequencies['hihat']:
                hihat_audio += 0.03 * np.sin(2 * np.pi * freq * hihat_time) * \
                              np.exp(-hihat_time * 100)
            
            if beat_start + len(hihat_audio) <= len(audio):
                audio[beat_start:beat_start + len(hihat_audio)] += hihat_audio
        
        # Melodia suave (não em todas as batidas)
        if beat % 8 == 0:
            melody_freq = random.choice(frequencies['melody'])
            melody_samples = min(len(t) - beat_start, int(beat_duration * 4 * sample_rate))
            melody_time = t[beat_start:beat_start + melody_samples] - beat_time
            
            melody = 0.05 * np.sin(2 * np.pi * melody_freq * melody_time) * \
                    np.exp(-melody_time * 2)
            
            if beat_start + len(melody) <= len(audio):
                audio[beat_start:beat_start + len(melody)] += melody
    
    # Normaliza o áudio
    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio)) * 0.7
    
    # Salva como WAV
    with wave.open(output_path, 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        # Converte para int16
        audio_int16 = (audio * 32767).astype(np.int16)
        wav_file.writeframes(audio_int16.tobytes())
    
    print(f"✅ Áudio LOFI gerado: {output_path}")
    return output_path


if __name__ == "__main__":
    print("🎵 Gerador de Vídeos LOFI")
    print("=" * 40)
    
    # Gera imagem
    img_path = generate_lofi_image()
    
    # Gera áudio (60 segundos)
    audio_path = generate_lofi_audio(duration=60)
    
    print("\n✅ Imagem e áudio gerados com sucesso!")
    print("Agora use create_lofi_video.py para criar o vídeo final.")

