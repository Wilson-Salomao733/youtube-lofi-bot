# 📝 Exemplos de Uso

Guia prático com exemplos reais de como usar o bot LOFI.

## 🎬 Exemplos Básicos

### 1. Criar um vídeo de teste

```bash
python3 create_lofi_video.py --duration 60
```

Cria um vídeo de 1 minuto para testar.

### 2. Criar vídeo de 1 hora para YouTube

```bash
python3 create_lofi_video.py --duration 3600
```

Perfeito para conteúdo de YouTube.

## 📦 Exemplos com Docker

### 1. Primeiro teste com Docker

```bash
# Criar a imagem
docker-compose build

# Criar vídeo de teste
docker-compose run --rm lofi-generator python3 create_lofi_video.py --duration 60
```

### 2. Criar vídeo e salvar em output/

```bash
docker-compose run --rm -v $(pwd)/output:/app/output lofi-generator \
    python3 create_lofi_video.py --duration 3600
```

### 3. Múltiplos vídeos

```bash
docker-compose run --rm lofi-generator python3 automated_youtube_bot.py \
    --multiple 5 --duration 1800
```

## 🤖 Exemplos de Automação

### 1. Upload único para YouTube

```bash
python3 automated_youtube_bot.py --upload --duration 3600
```

### 2. Criar 10 vídeos e fazer upload

```bash
python3 automated_youtube_bot.py --multiple 10 --upload --duration 1800
```

### 3. Agendar criação diária

```bash
# Cria vídeo diariamente às 9h da manhã
python3 automated_youtube_bot.py --schedule "09:00" --duration 3600
```

### 4. Rodar em background com Docker

```bash
# Inicia o bot em background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

## 🎯 Casos de Uso Reais

### Caso 1: Canal novo no YouTube

```bash
# Criar 30 vídeos de 1 hora
for i in {1..30}; do
    python3 create_lofi_video.py --duration 3600
    sleep 60  # Wait 1 min between videos
done
```

**Resultado:** 30 horas de conteúdo LOFI!

### Caso 2: Upload automático semanal

```bash
# Criar vídeo toda segunda-feira às 8h
python3 automated_youtube_bot.py --schedule "mon 08:00" --upload
```

### Caso 3: Lives automatizadas

```python
# Criar live agendado
from youtube_uploader import YouTubeUploader
from datetime import datetime, timedelta

uploader = YouTubeUploader()

# Agenda live para 2 horas no futuro
broadcast_id, stream_key = uploader.create_live_broadcast(
    title="LOFI Live - Relaxing Music 🌙",
    scheduled_start_time=datetime.now() + timedelta(hours=2),
    description="🎵 24/7 LOFI Music - Study, Work, Relax",
    privacy_status="public"
)

print(f"🔗 Use no OBS: rtmp://a.rtmp.youtube.com/live2/{stream_key}")
```

## 🎨 Personalização

### Modificar cores

Edite `lofi_generator_pro.py` linha ~18-40:

```python
self.color_palettes = [
    # Adicione seus paletas aqui
    {"bg1": (SeuCor1), "bg2": (SeuCor2), ...},
]
```

### Mudar BPM do áudio

Edite `lofi_generator_pro.py` linha ~120:

```python
bpm = 70  # Mais lento
bpm = 100  # Mais rápido
```

### Criar vídeos em 4K

```bash
python3 create_lofi_video.py --duration 3600 --width 3840 --height 2160
```

## 📊 Monitoramento

### Ver espaço em disco

```bash
# Ver tamanho dos vídeos
du -sh output/

# Ver quantos vídeos
ls -1 output/*.mp4 | wc -l
```

### Limpar arquivos antigos

```bash
# Remover vídeos mais antigos que 7 dias
find output/ -name "*.mp4" -mtime +7 -delete
```

## 🔄 Workflows Completos

### Workflow 1: Canal automático 24/7

```python
# auto_lofi_channel.py
import schedule
import time
from automated_youtube_bot import LofiYouTubeBot

bot = LofiYouTubeBot(upload_to_youtube=True)

# Upload a cada 6 horas
schedule.every(6).hours.do(bot.create_and_publish, duration=3600)

# Upload de live a cada dia às 00:00
schedule.every().day.at("00:00").do(bot.create_live_broadcast)

while True:
    schedule.run_pending()
    time.sleep(60)
```

Execute:
```bash
python3 auto_lofi_channel.py
```

### Workflow 2: Batch de upload

```bash
# Cria 24 vídeos (1 para cada hora do dia)
./run_bot.sh  # Selecione opção 3

# No menu interativo, digite 24

# Depois faça upload de todos
python3 automated_youtube_bot.py --multiple 24 --upload
```

## 💡 Dicas Pro

### 1. Títulos eficazes

```python
titles = [
    "LOFI Study Music 2024 🎵 No Copyright",
    "Chill LOFI Hip Hop - 1 Hour Mix",
    "Relaxing LOFI Beats for Focus",
]
```

### 2. Tags recomendadas

```python
tags = [
    "lofi", "lofi hip hop", "study music", "chill beats",
    "focus music", "relaxing music", "no copyright",
    "lo-fi", "lofi music", "background music",
    "study", "work music", "concentration"
]
```

### 3. Descrições otimizadas

Inclua:
- Duração do vídeo
- Para que serve (study, work, relax)
- Informação de copyright (sem direitos)
- Call-to-action (subscribe, like)
- Timestamp para diferentes moods

### 4. Thumbnails

Crie thumbnails usando a mesma paleta de cores do vídeo para consistência visual.

## 🚀 Deploy em Produção

### Usando VPS/Droplet

```bash
# 1. Clone o repositório
git clone seu-repo
cd YOUTUBE

# 2. Build e run
docker-compose up -d --build

# 3. Ver logs
docker-compose logs -f

# 4. Verificar status
docker-compose ps
```

### Usando Cron

```bash
# Editar crontab
crontab -e

# Adicionar (toda segunda às 8h)
0 8 * * 1 cd /path/to/YOUTUBE && docker-compose run --rm lofi-generator python3 automated_youtube_bot.py --upload
```

## 📈 Métricas

Acompanhe performance:

```bash
# Contar vídeos criados
ls output/*.mp4 | wc -l

# Tamanho total
du -sh output/

# Últimos 10 vídeos
ls -lt output/*.mp4 | head -10
```

