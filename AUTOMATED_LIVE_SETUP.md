# 🤖 Setup do Bot Automatizado de Live

Sistema 100% automático que cria vídeo às 7h e inicia live até 18h todos os dias.

## 🎯 O que o bot faz:

1. ✅ **Todo dia às 7h**: Cria vídeo de 30 segundos automaticamente
2. ✅ **Automaticamente**: Cria live pública no YouTube
3. ✅ **Automaticamente**: Inicia transmissão com vídeo em loop
4. ✅ **Até 18h**: Live fica no ar com loop infinito
5. ✅ **No outro dia**: Repete o processo automaticamente

**TUDO AUTOMÁTICO - ZERO INTERVENÇÃO MANUAL!**

---

## 📋 Pré-requisitos:

### 1. Instalar ffmpeg

**Linux:**
```bash
sudo apt-get update
sudo apt-get install -y ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
- Baixe de: https://ffmpeg.org/download.html
- Adicione ao PATH

### 2. Configurar YouTube API

1. Acesse: https://console.cloud.google.com/
2. Ative YouTube Data API v3
3. Crie credenciais OAuth
4. Baixe `credentials.json` em `credentials/`
5. Autorize na primeira execução

---

## 🚀 Opção 1: Executar Direto (Sem Docker)

```bash
# Executar o bot
python automated_live_bot.py
```

O bot vai:
- Rodar em background
- Criar vídeo às 7h
- Iniciar live automaticamente
- Parar às 18h
- Repetir no dia seguinte

**Para rodar em background (Linux/macOS):**
```bash
nohup python automated_live_bot.py > bot.log 2>&1 &
```

**Para ver logs:**
```bash
tail -f automated_live.log
```

---

## 🐳 Opção 2: Executar com Docker (Recomendado)

### Build e Run:

```bash
# Build da imagem
docker-compose -f docker-compose.live.yml build

# Iniciar bot
docker-compose -f docker-compose.live.yml up -d

# Ver logs
docker-compose -f docker-compose.live.yml logs -f

# Parar bot
docker-compose -f docker-compose.live.yml down
```

### Com Docker, o bot:
- ✅ Roda 24/7 automaticamente
- ✅ Reinicia automaticamente se o container parar
- ✅ Mantém logs persistentes
- ✅ Isolado do sistema

---

## 📁 Estrutura de Arquivos:

```
YOUTUBE/
├── automated_live_bot.py      # Bot principal
├── Dockerfile.live            # Dockerfile para o bot
├── docker-compose.live.yml    # Docker compose
├── credentials/               # Credenciais YouTube
│   ├── credentials.json
│   └── token.pickle
├── images/                    # Imagens para vídeos
├── output/                    # Vídeos gerados
└── automated_live.log         # Logs do bot
```

---

## ⚙️ Como Funciona:

### Fluxo Diário:

1. **07:00** - Bot acorda
2. **07:01** - Cria vídeo de 30s usando imagens de `images/`
3. **07:02** - Cria live pública no YouTube
4. **07:03** - Inicia streaming com ffmpeg (vídeo em loop)
5. **07:04 - 17:59** - Live no ar, streaming contínuo
6. **18:00** - Para streaming automaticamente
7. **Próximo dia 07:00** - Repete processo

### Tecnologias:

- **ffmpeg**: Transmite vídeo diretamente para YouTube (sem OBS)
- **schedule**: Agendamento de tarefas diárias
- **YouTube API**: Criação de lives
- **Docker**: Containerização para 24/7

---

## 🔍 Monitoramento:

### Ver Status do Bot:

```bash
# Logs em tempo real
tail -f automated_live.log

# Ou com Docker
docker-compose -f docker-compose.live.yml logs -f
```

### Verificar se está rodando:

```bash
# Ver processos Python
ps aux | grep automated_live_bot

# Ou com Docker
docker-compose -f docker-compose.live.yml ps
```

---

## 🛠️ Troubleshooting:

### Bot não cria vídeo às 7h?
- Verifique logs: `tail -f automated_live.log`
- Certifique-se que o bot está rodando
- Verifique timezone do sistema

### Streaming não inicia?
- Verifique se ffmpeg está instalado: `ffmpeg -version`
- Verifique Stream Key no YouTube Studio
- Veja logs do ffmpeg nos logs do bot

### Live para antes das 18h?
- Verifique conexão com internet
- Verifique se ffmpeg não foi encerrado
- Veja logs para erros

### Reiniciar bot manualmente:
```bash
# Parar
docker-compose -f docker-compose.live.yml down

# Reiniciar
docker-compose -f docker-compose.live.yml up -d
```

---

## 📝 Customizações:

### Mudar horário de criação:
Edite `automated_live_bot.py`:
```python
schedule.every().day.at("07:00").do(self.daily_workflow)
```

### Mudar horário de término:
Edite `automated_live_bot.py`:
```python
if now.hour == 18:  # Mude para horário desejado
```

### Duração do vídeo:
O vídeo é sempre de 30 segundos (para loop suave)

---

## ✅ Checklist Final:

- [ ] ffmpeg instalado
- [ ] YouTube API configurada
- [ ] credentials/credentials.json presente
- [ ] Imagens em images/ (opcional, mas recomendado)
- [ ] Bot testado manualmente primeiro
- [ ] Docker instalado (se usar Docker)
- [ ] Bot rodando 24/7

---

## 🎉 Pronto!

Depois de configurar, o bot vai:
- ✅ Criar vídeo automaticamente todo dia
- ✅ Iniciar live automaticamente
- ✅ Transmitir até 18h
- ✅ Repetir no próximo dia

**ZERO INTERVENÇÃO MANUAL NECESSÁRIA!** 🚀

