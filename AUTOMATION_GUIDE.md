# 🤖 Guia de Automação Completo

Como automatizar criação e upload de vídeos LOFI para o YouTube.

## 🎯 3 Passos para Automação Total

### 1️⃣ Configurar YouTube API (5 minutos)

```bash
# Passo 1: Acesse o Google Cloud Console
# https://console.cloud.google.com/

# Passo 2: Crie um projeto chamado "LOFI Bot"

# Passo 3: Ative a YouTube Data API v3
# Menu lateral > APIs e Serviços > Biblioteca > Buscar "YouTube Data API v3" > ATIVAR

# Passo 4: Crie credenciais OAuth
# APIs e Serviços > Credenciais > Criar credenciais > ID do cliente OAuth
# Tipo: Aplicativo da área de trabalho

# Passo 5: Baixe as credenciais
# Clique no download (seta para baixo) > Salve como: credentials/credentials.json
```

### 2️⃣ Testar Upload Manual

```bash
# Teste criando e fazendo upload de um vídeo
python3 automated_youtube_bot.py --upload --duration 60

# Na primeira vez, ele vai abrir o navegador para autorizar
# Clique em "Permitir" e o token será salvo
```

### 3️⃣ Automação Completa

#### Opção A: Upload Único
```bash
# Cria 1 vídeo de 1 hora e sobe para o YouTube
python3 automated_youtube_bot.py --upload --duration 3600
```

#### Opção B: Múltiplos Vídeos
```bash
# Cria 10 vídeos de 1 hora e faz upload de todos
python3 automated_youtube_bot.py --upload --multiple 10 --duration 3600
```

#### Opção C: Agendamento Automático
```bash
# Cria vídeo diariamente às 9h e faz upload
python3 automated_youtube_bot.py --upload --schedule "09:00" --duration 3600

# Deixe rodando em background:
nohup python3 automated_youtube_bot.py --upload --schedule "09:00" --duration 3600 &
```

## 📋 Comandos Completos

### Criar e Publicar
```bash
# 1 vídeo
python3 automated_youtube_bot.py --upload --duration 3600

# 5 vídeos
python3 automated_youtube_bot.py --upload --multiple 5 --duration 3600

# 10 vídeos de 30 minutos
python3 automated_youtube_bot.py --upload --multiple 10 --duration 1800
```

### Apenas Criar (sem upload)
```bash
# 1 vídeo
python3 automated_youtube_bot.py --duration 3600

# 5 vídeos
python3 automated_youtube_bot.py --multiple 5 --duration 3600
```

### Modo Agendado
```bash
# Todos os dias às 9h
python3 automated_youtube_bot.py --upload --schedule "09:00" --duration 3600

# A cada 6 horas
python3 automated_youtube_bot.py --upload --schedule "every 6 hours" --duration 3600
```

## 🐳 Com Docker

```bash
# Build da imagem
docker-compose build

# Roda com upload automático
docker-compose run --rm -v $(pwd)/credentials:/app/credentials \
    lofi-generator python3 automated_youtube_bot.py --upload --duration 3600

# Múltiplos vídeos
docker-compose run --rm lofi-generator \
    python3 automated_youtube_bot.py --upload --multiple 5
```

## ⚙️ Configurações Avançadas

### Status de Privacidade

Por padrão, vídeos são criados como **"unlisted"** (não listados).

Para publicar como público, edite `automated_youtube_bot.py` linha ~145:

```python
privacy_status="public"  # ao invés de "unlisted"
```

### Títulos e Tags

Os títulos são gerados automaticamente. Para personalizar, edite a função `_generate_video_title()`:

```python
def _generate_video_title(self, duration):
    titles = [
        f"LOFI Hip Hop Study Music - {duration} min",
        f"Chill Beats to Study - LOFI Mix {duration} min",
        # Adicione seus títulos aqui
    ]
    return random.choice(titles)
```

### Descrições

Edite a função `_generate_description()` para mudar a descrição automática.

### Tags

Edite a função `_get_default_tags()`:

```python
def _get_default_tags(self):
    return [
        "lofi", "lofi hip hop", "study music",
        "chill beats", "lo-fi", "lofi music",
        # Adicione suas tags
    ]
```

## 🔄 Automação 24/7

### Com systemd (Linux)

Crie `/etc/systemd/system/lofi-bot.service`:

```ini
[Unit]
Description=LOFI Bot YouTube

[Service]
Type=simple
User=seu-usuario
WorkingDirectory=/home/seu-usuario/Documentos/YOUTUBE
ExecStart=/usr/bin/python3 automated_youtube_bot.py --upload --schedule "09:00" --duration 3600
Restart=always

[Install]
WantedBy=multi-user.target
```

Ative:
```bash
sudo systemctl enable lofi-bot
sudo systemctl start lofi-bot
```

### Com cron (qualquer sistema)

```bash
# Edite crontab
crontab -e

# Adicione (cria vídeo todo dia às 9h e faz upload)
0 9 * * * cd /home/seu-usuario/Documentos/YOUTUBE && python3 automated_youtube_bot.py --upload --duration 3600
```

## 📊 Monitoramento

### Ver logs
```bash
# Se estiver rodando com nohup
tail -f nohup.out

# Se estiver com systemd
sudo journalctl -u lofi-bot -f
```

### Ver vídeos criados
```bash
ls -lh output/
```

### Contar vídeos
```bash
ls output/*.mp4 | wc -l
```

## 🆘 Troubleshooting

### "Arquivo de credenciais não encontrado"
```bash
# Verifique se o arquivo existe
ls credentials/credentials.json

# Se não existir, baixe do Google Cloud Console
```

### "Quota exceeded"
- Limite padrão: 10,000 unidades/dia
- Upload de vídeo: ~1,600 unidades
- Máximo: ~6 vídeos/dia
- Para aumentar: Solicite aumento no Google Cloud Console

### "Permission denied"
```bash
chmod +x automated_youtube_bot.py
chmod +x create_lofi_video.py
```

## 🎯 Exemplos Práticos

### Criar 30 vídeos para um mês
```bash
python3 automated_youtube_bot.py --upload --multiple 30 --duration 3600
```

### Canal automático
```bash
# Roda em background, cria vídeo todo dia às 8h
nohup python3 automated_youtube_bot.py --upload --schedule "08:00" --duration 3600 > bot.log 2>&1 &
```

### Teste rápido
```bash
# Cria e publica vídeo de 5 minutos
python3 automated_youtube_bot.py --upload --duration 300
```

## 📝 Checklist de Configuração

- [ ] Google Cloud Console criado
- [ ] YouTube Data API v3 ativada
- [ ] Credenciais OAuth criadas
- [ ] `credentials.json` baixado
- [ ] Token gerado (primeira autorização)
- [ ] Bot testado com `--duration 60`
- [ ] Privacidade configurada (public/unlisted)
- [ ] Títulos personalizados (opcional)
- [ ] Automação configurada (cron/systemd)

## ✅ Pronto!

Agora você tem um bot totalmente automatizado que:
- ✅ Cria vídeos LOFI únicos
- ✅ Faz upload automático para o YouTube
- ✅ Gera títulos e tags automaticamente
- ✅ Pode rodar 24/7
- ✅ É totalmente configurável

**Boa sorte com seu canal! 🎵**

