# 🕐 Como o Sistema Roda Automaticamente às 7h

## 📋 Fluxo Completo Automatizado

### ⏰ **7h da Manhã (07:00)**

O sistema executa automaticamente esta sequência:

```
1️⃣  CRIAR VÍDEO DE 30 SEGUNDOS
    ├── Escolhe uma IMAGEM aleatória de `images/`
    ├── Escolhe um ÁUDIO aleatório de `audios/`
    ├── Aplica ANIMAÇÕES na imagem (zoom, pan)
    ├── Se áudio > 30s: CORTA para 30s
    ├── Se áudio < 30s: FAZ LOOP até 30s
    └── Gera vídeo: `lofi_video_YYYYMMDD_HHMMSS.mp4`

2️⃣  CRIAR LIVE NO YOUTUBE
    ├── Conecta à API do YouTube
    ├── Cria transmissão pública
    ├── Obtém Stream Key e RTMP URL
    └── Agenda para iniciar imediatamente

3️⃣  INICIAR STREAMING
    ├── Usa FFmpeg para transmitir
    ├── Vídeo roda em LOOP INFINITO
    ├── Stream vai para YouTube Live
    └── Fica no ar até 19h (7 da noite)
```

### 🔄 **Durante o Dia (7h - 19h)**

```
├── Sistema monitora o streaming a cada minuto
├── Se o FFmpeg parar, tenta reiniciar (até 3 vezes)
├── Logs de status a cada hora
└── Continua até 19h
```

### 🛑 **19h (7 da Noite) - 19:00**

```
├── Sistema detecta que é 19h
├── Para o streaming FFmpeg
├── Encerra a live no YouTube
└── Aguarda até o próximo dia às 7h
```

### 🔁 **Repetição Diária**

```
Todo dia às 7h:
├── Novo vídeo (nova imagem + novo áudio)
├── Nova live
├── Nova combinação aleatória
└── Repete o ciclo
```

## 🐳 Como Funciona com Docker

### **Iniciar o Sistema:**

```bash
# Com Docker (recomendado - roda 24/7)
docker compose -f docker-compose.live.yml up -d

# Ou sem Docker
python3 automated_live_bot.py
```

### **O que acontece:**

1. **Container/Python inicia** e fica rodando em background
2. **Schedule library** agenda tarefa para 7h todo dia
3. **Às 7h**, executa `daily_workflow()` em thread separada
4. **Cria vídeo** usando `create_lofi_video()` com arquivos das pastas
5. **Cria live** usando `YouTubeUploader`
6. **Inicia FFmpeg** para streaming em loop
7. **Monitora** até 19h
8. **Para** automaticamente às 19h
9. **Aguarda** próximo dia às 7h

## 📁 Estrutura Necessária

```
YOUTUBE/
├── images/          # Pelo menos 1 imagem (PNG/JPG)
├── audios/          # Pelo menos 1 áudio (MP3/WAV)
├── credentials/     # Credenciais do YouTube
│   ├── credentials.json
│   └── token.pickle
└── automated_live_bot.py  # Script principal
```

## ⚙️ Configuração do Agendamento

O código usa a biblioteca `schedule`:

```python
# Em automated_live_bot.py, linha ~330
schedule.every().day.at("07:00").do(
    lambda: threading.Thread(target=self.daily_workflow, daemon=True).start()
)
```

Isso significa:
- **Todo dia** às **07:00** (7h da manhã)
- Executa `daily_workflow()` em thread separada
- Não bloqueia o loop principal

## 🔍 Verificar se Está Rodando

### **Com Docker:**

```bash
# Ver logs em tempo real
docker logs -f live-bot

# Ver status do container
docker ps | grep live-bot
```

### **Sem Docker:**

```bash
# Ver processo Python
ps aux | grep automated_live_bot

# Ver logs (se estiver usando nohup)
tail -f automated_live.log
```

## ⚠️ Requisitos

1. **Sistema ligado 24/7** (ou Docker rodando)
2. **Internet ativa**
3. **FFmpeg instalado** (no Docker já está)
4. **Credenciais YouTube válidas**
5. **Live streaming habilitado** no canal
6. **Arquivos nas pastas** (imagens e áudios)

## 🎯 Exemplo Prático

**Hoje (06/11) às 7h:**
- Escolhe: `imagem_1.jpg` + `audio_1.mp3`
- Cria vídeo de 30s
- Inicia live
- Roda até 19h

**Amanhã (07/11) às 7h:**
- Escolhe: `imagem_5.jpg` + `audio_3.mp3` (aleatório)
- Cria NOVO vídeo de 30s
- Inicia NOVA live
- Roda até 19h

**E assim por diante...**

## 💡 Dicas

- Quanto mais imagens e áudios, mais variedade
- Cada dia terá combinação diferente
- Sistema é totalmente automático após iniciar
- Não precisa fazer nada manualmente

