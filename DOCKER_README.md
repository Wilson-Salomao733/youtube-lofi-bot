# 🐳 Docker - Live Bots YouTube

## ✅ O que está configurado

### Dockerfile
- ✅ Python 3.12
- ✅ **ffmpeg** (para streaming)
- ✅ **Chromium + ChromeDriver** (para automação web)
- ✅ Todas as dependências Python
- ✅ Dependências de processamento de imagem/vídeo

### docker-compose.yml
- ✅ Volumes montados (output, credentials, imagens, áudios, logs)
- ✅ Fuso horário configurado (America/Sao_Paulo)
- ✅ Executa `main.py` (ambos os bots)

## 🚀 Como usar

### 1. Construir a imagem

```bash
docker-compose build
```

### 2. Testar configuração

```bash
./testar_docker.sh
```

Isso verifica:
- ✅ ffmpeg instalado
- ✅ Chromium instalado
- ✅ Dependências Python

### 3. Iniciar os bots

```bash
# Inicia em background
docker-compose up -d

# Ver logs em tempo real
docker-compose logs -f

# Parar
docker-compose down
```

## 📋 Comandos úteis

```bash
# Ver status
docker-compose ps

# Ver logs
docker-compose logs -f live-bots

# Entrar no container
docker-compose exec live-bots bash

# Verificar ffmpeg
docker-compose exec live-bots ffmpeg -version

# Reconstruir (se mudar Dockerfile)
docker-compose build --no-cache
docker-compose up -d
```

## 🔧 Configuração

### Executar apenas um bot

Edite `docker-compose.yml`:

```yaml
# Apenas manhã
command: python3 morning_bot.py

# Apenas noite
command: python3 night_bot.py
```

### Executar workflow imediatamente

```yaml
environment:
  - EXECUTE_NOW=true
```

## 📁 Estrutura de Volumes

```
./output          → Vídeos gerados
./credentials     → Credenciais YouTube
./images           → Imagens LOFI (manhã)
./imagens noite   → Imagens noturnas
./audios          → Áudios LOFI (manhã)
./audio_noite     → Áudios noturnos
./logs            → Logs dos bots
```

## ⚙️ Variáveis de Ambiente

- `TZ=America/Sao_Paulo` → Fuso horário
- `PYTHONUNBUFFERED=1` → Logs em tempo real
- `DISPLAY=:99` → Para automação web
- `CHROME_BIN=/usr/bin/chromium` → Caminho do Chromium
- `CHROMEDRIVER_PATH=/usr/bin/chromedriver` → Caminho do ChromeDriver

## ✅ Verificação

Após iniciar, verifique:

```bash
# Status
docker-compose ps

# Logs recentes
docker-compose logs --tail=50 live-bots

# Verificar processos
docker-compose exec live-bots ps aux

# Testar streaming
docker-compose exec live-bots python3 testar_streaming_rapido.py
```

## 🐛 Troubleshooting

### Container não inicia

```bash
# Ver logs de erro
docker-compose logs live-bots

# Reconstruir
docker-compose build --no-cache
```

### ffmpeg não encontrado

```bash
# Verificar dentro do container
docker-compose exec live-bots which ffmpeg
docker-compose exec live-bots ffmpeg -version
```

### Chromium não funciona

```bash
# Verificar
docker-compose exec live-bots chromium --version
docker-compose exec live-bots which chromium
```

## 📝 Notas Importantes

1. **Credenciais**: Coloque `credentials/credentials.json` antes de iniciar
2. **Cookies**: Se usar automação web, salve cookies primeiro (fora do Docker)
3. **Recursos**: Certifique-se de ter imagens e áudios nas pastas corretas
4. **Logs**: Verifique `logs/` para debug

## 🎯 Fluxo Completo

1. Container inicia
2. Bots agendam execuções (7h manhã, 20h noite)
3. Cria vídeo automaticamente
4. Cria live no YouTube
5. Inicia streaming com **ffmpeg** (ou automação web como fallback)
6. Monitora até horário de parada (19h manhã, 3h noite)



