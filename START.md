# 🚀 Início Rápido - Bot LOFI para YouTube

Guia de 5 minutos para começar.

## ⚡ Setup em 3 Passos

### 1️⃣ Instalar Dependências

```bash
cd ~/Documentos/YOUTUBE
pip3 install -r requirements.txt
```

### 2️⃣ (Opcional) Configurar YouTube API

Só precisa se quiser upload automático.

```bash
# Siga o guia completo
cat YOUTUBE_SETUP.md
```

Resumido:
1. Acesse https://console.cloud.google.com/
2. Crie projeto
3. Ative YouTube Data API v3
4. Crie credenciais OAuth 2.0
5. Baixe JSON para `credentials/credentials.json`

### 3️⃣ Criar Seu Primeiro Vídeo

```bash
python3 create_lofi_video.py --duration 60
```

Pronto! 🎉

## 📚 Próximos Passos

### Criar vídeo profissional de 1 hora

```bash
python3 create_lofi_video.py --duration 3600
```

### Criar múltiplos vídeos

```bash
python3 automated_youtube_bot.py --multiple 5
```

### Com Docker (Recomendado)

```bash
./run_bot.sh
# Selecione a opção desejada
```

## 📂 Estrutura

```
YOUTUBE/
├── create_lofi_video.py      ← Script principal
├── automated_youtube_bot.py  ← Bot completo
├── lofi_generator_pro.py    ← Gerador profissional
├── youtube_uploader.py      ← Upload para YouTube
├── run_bot.sh               ← Script interativo
├── requirements.txt          ← Dependências
├── Dockerfile               ← Container Docker
├── docker-compose.yml       ← Orquestração
├── credentials/              ← Credenciais YouTube (não comite!)
├── output/                   ← Vídeos gerados
└── README.md                 ← Documentação completa
```

## 🎯 Casos de Uso

### 1. Canal LOFI no YouTube

```bash
# Cria 30 vídeos de 1 hora
python3 automated_youtube_bot.py --multiple 30 --duration 3600 --upload
```

### 2. Lives Automatizadas

```python
from youtube_uploader import YouTubeUploader
from datetime import datetime, timedelta

uploader = YouTubeUploader()
broadcast_id, stream_key = uploader.create_live_broadcast(
    title="LOFI Live",
    scheduled_start_time=datetime.now() + timedelta(hours=1)
)
```

### 3. Upload Diário Automático

```bash
# Roda em background, cria vídeo todo dia às 9h
docker-compose up -d
```

## 📖 Documentação Completa

- `README.md` - Visão geral e features
- `YOUTUBE_SETUP.md` - Configuração YouTube API
- `EXEMPLOS.md` - Exemplos práticos
- `START.md` - Este arquivo (início rápido)

## 🆘 Ajuda

### Erros Comuns

**FFmpeg não encontrado:**
```bash
sudo apt-get install ffmpeg
```

**Permissão negada:**
```bash
chmod +x run_bot.sh
```

**Dependências:**
```bash
pip3 install --upgrade -r requirements.txt
```

## 🎬 Pronto para Produção!

```bash
# Build da imagem Docker
docker-compose build

# Executar
docker-compose up -d

# Ver logs
docker-compose logs -f
```

## 📞 Suporte

- Issues: Crie uma issue no GitHub
- Documentação: Leia os arquivos .md
- Exemplos: Veja EXEMPLOS.md

---

**Boa sorte com seu canal LOFI! 🎵✨**

