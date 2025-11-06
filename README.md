# 🎵 Bot Automatizado de Live LOFI no YouTube

Sistema automatizado que cria vídeos LOFI e inicia transmissões ao vivo no YouTube todos os dias às 7h da manhã.

## ✨ Funcionalidades

- 🎬 **Criação automática de vídeos LOFI** com animações e música
- 📺 **Transmissão ao vivo no YouTube** em loop infinito
- ⏰ **Agendamento automático** - executa todos os dias às 7h
- 🔑 **Stream Key fixo** - reutiliza a mesma key para todas as lives
- 🐳 **Dockerizado** - roda tudo dentro de containers
- 🇧🇷 **Título e descrição em português**

## 🚀 Como Usar

### Pré-requisitos

- Docker e Docker Compose instalados
- Credenciais do YouTube API configuradas em `credentials/`
- Stream key fixo configurado

### Configuração Inicial

1. **Configure as credenciais do YouTube:**
   ```bash
   mkdir -p credentials
   # Coloque seus arquivos de credenciais aqui:
   # - credentials.json
   # - token.pickle (gerado automaticamente após primeira autenticação)
   ```

2. **Configure o stream key fixo:**
   ```bash
   # Edite credentials/stream_config.json ou use o script:
   python3 configurar_stream_key_fixo.py
   ```

3. **Inicie o container:**
   ```bash
   ./docker_live_start.sh
   # ou
   docker compose -f docker-compose.live.yml up -d
   ```

### Comandos Úteis

```bash
# Ver logs
docker logs -f lofi-live-bot
# ou
tail -f logs/automated_live.log

# Parar container
./docker_live_stop.sh
# ou
docker compose -f docker-compose.live.yml down

# Status
./docker_live_status.sh
```

## 📋 Estrutura do Projeto

```
.
├── automated_live_bot.py      # Bot principal que agenda e executa workflow
├── create_lofi_video.py       # Cria vídeos LOFI com frames animados
├── lofi_generator_ultra.py   # Gera frames animados LOFI
├── youtube_uploader.py       # Gerencia API do YouTube e streams
├── Dockerfile.live           # Dockerfile para o container
├── docker-compose.live.yml    # Configuração Docker Compose
├── credentials/              # Credenciais (NÃO commitar!)
├── images/                   # Imagens para gerar vídeos
├── audios/                   # Áudios para os vídeos
├── output/                   # Vídeos gerados
└── logs/                     # Logs do sistema
```

## ⚙️ Como Funciona

1. **Todos os dias às 7h da manhã:**
   - Cria um novo vídeo LOFI (30 segundos, loop infinito)
   - Cria uma live no YouTube
   - Inicia transmissão com ffmpeg
   - Vídeo fica em loop até 19h (7 da noite)

2. **Stream Key Fixo:**
   - Usa a mesma stream key para todas as lives
   - Configurado em `credentials/stream_config.json`
   - Não precisa obter manualmente toda vez

3. **Tudo roda dentro do Docker:**
   - Container isolado
   - Timezone configurado (America/Sao_Paulo)
   - Logs persistentes

## 📝 Documentação

- `COMO_CRIAR_STREAM_KEY_FIXO.md` - Como criar e configurar stream key fixo
- `COMO_OBTER_STREAM_KEY_AUTOMATICO.md` - Como obter stream key automaticamente
- `STREAM_PERMANENTE.md` - Sobre stream permanente
- `README_DOCKER_FINAL.md` - Guia completo do Docker

## 🔒 Segurança

⚠️ **IMPORTANTE:** Nunca commite arquivos sensíveis:
- `credentials/` - Contém credenciais da API
- `*.json` - Arquivos de configuração com tokens
- `*.pickle` - Tokens de autenticação

Esses arquivos estão no `.gitignore` e não serão commitados.

## 📄 Licença

Este projeto é para uso pessoal.

## 🤝 Contribuindo

Este é um projeto pessoal, mas sugestões são bem-vindas!

---

**Desenvolvido para automatizar transmissões LOFI no YouTube** 🎵
