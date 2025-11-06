#!/usr/bin/env python3
"""
Bot Automatizado para Criar e Publicar Vídeos LOFI no YouTube
Sistema profissional com Docker e integração completa
"""
import os
import sys
import time
import random
import schedule
from datetime import datetime, timedelta
import argparse

from create_lofi_video import create_lofi_video
from youtube_uploader import YouTubeUploader


class LofiYouTubeBot:
    """Bot automatizado para criar e publicar vídeos LOFI"""
    
    def __init__(self, upload_to_youtube=False, credentials_file="credentials/credentials.json"):
        """
        Inicializa o bot
        
        Args:
            upload_to_youtube: Se True, faz upload para o YouTube
            credentials_file: Caminho do arquivo de credenciais
        """
        self.upload_to_youtube = upload_to_youtube
        self.uploader = None
        self.output_dir = "output"
        
        # Cria diretórios necessários
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs("credentials", exist_ok=True)
        
        if upload_to_youtube:
            try:
                self.uploader = YouTubeUploader(credentials_file)
            except Exception as e:
                print(f"⚠️  Aviso: Não foi possível conectar ao YouTube: {e}")
                print("📝 Continuando sem upload automático...")
                self.upload_to_youtube = False
    
    def create_and_publish(self, duration=3600, title=None, tags=None):
        """
        Cria um vídeo LOFI e publica no YouTube
        
        Args:
            duration: Duração do vídeo em segundos
            title: Título do vídeo (gerado automaticamente se None)
            tags: Lista de tags (padrão se None)
        """
        print("🎬 Iniciando criação de vídeo LOFI...")
        print("=" * 60)
        
        # Gera título se não fornecido
        if title is None:
            title = self._generate_video_title(duration)
        
        # Define tags padrão
        if tags is None:
            tags = self._get_default_tags()
        
        # Gera descrição
        description = self._generate_description(duration)
        
        # Cria o vídeo
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_filename = f"lofi_video_{timestamp}.mp4"
        video_path = os.path.join(self.output_dir, video_filename)
        
        print(f"\n📹 Criando vídeo: {title}")
        print(f"⏱️  Duração: {self._format_duration(duration)}")
        
        # Cria vídeo temporário para depois mover
        temp_video = create_lofi_video(video_duration=duration)
        
        # Move para output
        if os.path.exists(temp_video):
            os.rename(temp_video, video_path)
            print(f"✅ Vídeo salvo: {video_path}")
        
        # Faz upload se configurado
        if self.upload_to_youtube and self.uploader:
            print(f"\n📤 Fazendo upload para o YouTube...")
            video_id = self.uploader.upload_video(
                video_file=video_path,
                title=title,
                description=description,
                tags=tags,
                privacy_status="unlisted"  # Altere para "public" quando estiver pronto
            )
            
            if video_id:
                print(f"🎉 Vídeo publicado com sucesso!")
                print(f"🔗 https://www.youtube.com/watch?v={video_id}")
            else:
                print("⚠️  Falha no upload, mas vídeo foi criado localmente")
        
        return video_path
    
    def schedule_daily_videos(self, time_str="09:00", duration=3600):
        """
        Agenda criação diária de vídeos
        
        Args:
            time_str: Hora para criar (formato HH:MM)
            duration: Duração de cada vídeo
        """
        print(f"📅 Agendando vídeos diários às {time_str}")
        
        def create_video():
            try:
                self.create_and_publish(duration=duration)
            except Exception as e:
                print(f"❌ Erro ao criar vídeo: {e}")
        
        schedule.every().day.at(time_str).do(create_video)
        
        print("✅ Agendamento configurado!")
        print("⏳ Rodando agendador... (Ctrl+C para parar)")
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    def create_multiple_videos(self, count=5, duration=3600, delay_minutes=60):
        """
        Cria múltiplos vídeos em série
        
        Args:
            count: Número de vídeos
            duration: Duração de cada vídeo
            delay_minutes: Delay entre vídeos (em minutos)
        """
        print(f"📹 Criando {count} vídeos LOFI...")
        print("=" * 60)
        
        videos = []
        
        for i in range(count):
            print(f"\n{'='*60}")
            print(f"📊 Vídeo {i+1}/{count}")
            print(f"{'='*60}")
            
            try:
                video_path = self.create_and_publish(duration=duration)
                videos.append(video_path)
                
                if i < count - 1:
                    print(f"\n⏳ Aguardando {delay_minutes} minutos até o próximo vídeo...")
                    time.sleep(delay_minutes * 60)
                    
            except Exception as e:
                print(f"❌ Erro ao criar vídeo {i+1}: {e}")
                continue
        
        print(f"\n✅ Processo concluído!")
        print(f"📁 {len(videos)} vídeos criados em {self.output_dir}/")
        
        return videos
    
    def _generate_video_title(self, duration):
        """Gera título automático para o vídeo"""
        duration_minutes = duration // 60
        
        titles = [
            f"LOFI Hip Hop Study Music - {duration_minutes} min Mix",
            f"Chill Beats to Study/Relax - LOFI Mix {duration_minutes} min",
            f"LOFI Vibes 🎵 Study Music {duration_minutes} Minutes",
            f"Relaxing LOFI Music - {duration_minutes} Min Study Session",
            f"LOFI Hip Hop Beats - {duration_minutes} Min Mix (No Copyright)",
        ]
        
        return random.choice(titles)
    
    def _get_default_tags(self):
        """Retorna tags padrão para vídeos LOFI"""
        return [
            "lofi", "lofi hip hop", "study music", "chill beats",
            "lo-fi", "lo fi", "lofi music", "chill music",
            "focus music", "relaxing music", "no copyright",
            "study beats", "background music", "lofi mix",
            "lo fi hip hop", "chill vibes", "ambient music"
        ]
    
    def _generate_description(self, duration):
        """Gera descrição automática"""
        hours = duration // 3600
        minutes = (duration % 3600) // 60
        
        description = f"""
🎵 Welcome to LOFI Hip Hop Study Music!

This {hours}h {minutes}min mix is perfect for:
• Studying and focusing
• Working and productivity
• Relaxing and unwinding
• Meditation and yoga

🎨 All visuals and sounds are generated programmatically.
No copyright claims - feel free to use this music.

👉 Subscribe for more LOFI content!
🔔 Turn on notifications for new uploads

Tags: #lofi #study #music #chill #beats
"""
        return description.strip()
    
    def _format_duration(self, seconds):
        """Formata duração em formato legível"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        
        if hours > 0:
            return f"{hours}h {minutes}min"
        else:
            return f"{minutes}min"


# Função principal
def main():
    parser = argparse.ArgumentParser(
        description="Bot Automatizado para Vídeos LOFI no YouTube"
    )
    parser.add_argument("--duration", "-d", type=int, default=3600,
                        help="Duração em segundos (padrão: 3600 = 1 hora)")
    parser.add_argument("--multiple", "-m", type=int, default=1,
                        help="Número de vídeos para criar")
    parser.add_argument("--upload", "-u", action="store_true",
                        help="Faz upload automático para o YouTube")
    parser.add_argument("--schedule", "-s", type=str,
                        help="Agenda criação diária (formato: HH:MM)")
    parser.add_argument("--title", "-t", type=str,
                        help="Título customizado para o vídeo")
    
    args = parser.parse_args()
    
    # Cria o bot
    bot = LofiYouTubeBot(upload_to_youtube=args.upload)
    
    # Modo agendamento
    if args.schedule:
        bot.schedule_daily_videos(time_str=args.schedule, duration=args.duration)
    # Múltiplos vídeos
    elif args.multiple > 1:
        bot.create_multiple_videos(count=args.multiple, duration=args.duration)
    # Vídeo único
    else:
        bot.create_and_publish(
            duration=args.duration,
            title=args.title
        )


if __name__ == "__main__":
    main()


