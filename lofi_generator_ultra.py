"""
Gerador ULTRA de Vídeos LOFI
Versão melhorada com mais elementos visuais e áudio refinado
"""
import os
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import math


class LofiUltraGenerator:
    """Gerador ultra de conteúdo LOFI"""
    
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
    
    def generate_professional_image(self, width=1920, height=1080, output_path="lofi_image_ultra.png"):
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
        print(f"✅ Imagem LOFI ultra gerada: {output_path}")
        return output_path
    
    def _add_film_grain(self, img, intensity=0.1):
        """Adiciona granulado vintage à imagem"""
        pixels = np.array(img)
        noise = np.random.normal(0, intensity * 255, pixels.shape)
        noisy_pixels = np.clip(pixels + noise, 0, 255)
        
        for i in range(img.height):
            for j in range(img.width):
                img.putpixel((j, i), tuple(noisy_pixels[i, j].astype(int)))
    
    def generate_animated_frames(self, width=1920, height=1080, num_frames=900, 
                                fps=30, output_dir="lofi_temp_frames", 
                                base_image_path=None):
        """
        Gera frames animadas a partir de uma imagem base
        
        Args:
            width: Largura dos frames
            height: Altura dos frames
            num_frames: Número de frames a gerar
            fps: Frames por segundo
            output_dir: Diretório para salvar os frames
            base_image_path: Caminho da imagem base (se None, gera nova)
            
        Returns:
            (lista_de_caminhos, tipo_cena)
        """
        import os
        
        # Garante que o diretório existe
        os.makedirs(output_dir, exist_ok=True)
        
        # Se há imagem base, usa ela; senão gera nova
        if base_image_path and os.path.exists(base_image_path):
            base_img = Image.open(base_image_path)
            # Redimensiona se necessário
            if base_img.size != (width, height):
                base_img = base_img.resize((width, height), Image.Resampling.LANCZOS)
        else:
            # Gera nova imagem
            base_img_path = os.path.join(output_dir, "base_image.png")
            self.generate_professional_image(width, height, base_img_path)
            base_img = Image.open(base_img_path)
        
        frame_paths = []
        
        # Otimização: gera frames em lotes e reutiliza redimensionamentos
        # Para vídeos longos, gera menos frames únicos e repete
        # Para 30s a 30fps = 900 frames, mas podemos gerar apenas 300 únicos e repetir
        
        # Calcula quantos frames únicos gerar (máximo 300 para performance)
        unique_frames = min(num_frames, 300)
        frames_per_unique = max(1, num_frames // unique_frames)
        
        print(f"   ⚡ Gerando {unique_frames} frames únicos (repetindo para {num_frames} frames totais)...")
        
        # Gera frames únicos com leve movimento (zoom suave)
        for i in range(unique_frames):
            # Calcula zoom progressivo (1.0 a 1.05)
            zoom_factor = 1.0 + (i / unique_frames) * 0.05
            
            # Calcula novo tamanho
            new_width = int(width * zoom_factor)
            new_height = int(height * zoom_factor)
            
            # Redimensiona a imagem (usa BILINEAR para ser mais rápido que LANCZOS)
            zoomed_img = base_img.resize((new_width, new_height), Image.Resampling.BILINEAR)
            
            # Calcula crop para centralizar
            crop_x = (new_width - width) // 2
            crop_y = (new_height - height) // 2
            
            # Faz crop
            frame_img = zoomed_img.crop((crop_x, crop_y, crop_x + width, crop_y + height))
            
            # Salva frame único
            frame_path = os.path.join(output_dir, f"frame_{i+1:05d}.png")
            frame_img.save(frame_path, quality=85, optimize=True)  # quality 85 é suficiente e mais rápido
            frame_paths.append(frame_path)
            
            # Progresso a cada 50 frames
            if (i + 1) % 50 == 0:
                print(f"   ⏳ Progresso: {i+1}/{unique_frames} frames gerados...")
        
        # Se precisar de mais frames, duplica os últimos
        if len(frame_paths) < num_frames:
            last_frame = frame_paths[-1]
            for i in range(len(frame_paths), num_frames):
                # Copia o último frame
                new_frame_path = os.path.join(output_dir, f"frame_{i+1:05d}.png")
                import shutil
                shutil.copy2(last_frame, new_frame_path)
                frame_paths.append(new_frame_path)
        
        print(f"   ✅ {len(frame_paths)} frames gerados!")
        return frame_paths, "animated"


# Função global para compatibilidade
def generate_lofi_image(width=1920, height=1080, output_path="lofi_image.png"):
    gen = LofiUltraGenerator()
    return gen.generate_professional_image(width, height, output_path)


if __name__ == "__main__":
    print("🎵 Gerador LOFI Ultra")
    print("=" * 40)
    
    gen = LofiUltraGenerator()
    
    # Gera imagem profissional
    img_path = gen.generate_professional_image(output_path="lofi_ultra_image.png")
    
    print("\n✅ Recursos ultra gerados!")
