# Sistema de Live Bots para YouTube

Sistema automatizado para criar e transmitir lives no YouTube com vídeos LOFI (manhã) e Sons da Natureza (noite).

## 📁 Estrutura do Projeto

### Módulos Principais

- **`video_creator.py`**: Módulo centralizado para criação de vídeos
  - `create_morning_video()`: Cria vídeos LOFI para o fluxo da manhã
  - `create_night_video()`: Cria vídeos noturnos com sons da natureza

- **`live_manager.py`**: Módulo centralizado para gerenciamento de lives
  - `create_live()`: Cria live no YouTube
  - `start_streaming()`: Inicia transmissão com ffmpeg
  - `publish_live()`: Publica a live
  - `stop_streaming()`: Para a transmissão

- **`morning_bot.py`**: Bot para fluxo da manhã (7h - 19h)
  - Cria vídeo LOFI às 7h
  - Inicia live e transmite até 19h

- **`night_bot.py`**: Bot para fluxo da noite (20h - 3h)
  - Cria vídeo noturno às 20h
  - Inicia live e transmite até 3h da manhã

- **`main.py`**: Script principal para executar ambos os bots

### Pastas de Recursos

- **`images/`**: Imagens para vídeos LOFI (manhã)
- **`imagens noite/``**: Imagens organizadas por categoria para vídeos noturnos
- **`audios/`**: Áudios LOFI para vídeos da manhã
- **`audio_noite/`**: Áudios organizados por categoria para vídeos noturnos
- **`output/`**: Vídeos gerados
- **`logs/`**: Logs dos bots
- **`credentials/`**: Credenciais do YouTube API

## 🚀 Como Usar

### Executar Ambos os Bots

```bash
python3 main.py
```

### Executar Apenas Bot da Manhã

```bash
python3 main.py --morning-only
```

### Executar Apenas Bot da Noite

```bash
python3 main.py --night-only
```

### Executar Workflow Imediatamente

```bash
# Executa ambos os workflows agora
python3 main.py --morning-now --night-now

# Executa apenas manhã agora
python3 main.py --morning-only --morning-now

# Executa apenas noite agora
python3 main.py --night-only --night-now
```

### Executar Bots Separadamente

```bash
# Bot da manhã
python3 morning_bot.py

# Bot da noite
python3 night_bot.py
```

## ⚙️ Configuração

### 1. Credenciais do YouTube

Coloque suas credenciais em:
- `credentials/credentials.json` (baixado do Google Cloud Console)
- `credentials/token.pickle` (gerado automaticamente após primeira autenticação)
- `credentials/stream_config.json` (gerado automaticamente com stream permanente)

### 2. Recursos (Imagens e Áudios)

**Manhã (LOFI):**
- Coloque imagens em: `images/`
- Coloque áudios em: `audios/`

**Noite (Sons da Natureza):**
- Organize imagens por categoria em: `imagens noite/Categoria/`
- Organize áudios por categoria em: `audio_noite/Categoria/`
- Exemplo:
  ```
  imagens noite/
    Chuva/
      imagem1.jpg
      imagem2.jpg
    Fogueira/
      imagem1.jpg
  audio_noite/
    Chuva/
      audio1.mp3
    Fogueira/
      audio1.mp3
  ```

## 📋 Requisitos

- Python 3.7+
- ffmpeg instalado
- Credenciais do YouTube API configuradas
- Canal do YouTube habilitado para live streaming

### Instalar Dependências

```bash
pip install -r requirements.txt
```

### Instalar ffmpeg

```bash
# Linux
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

## 🔄 Fluxo de Funcionamento

### Bot da Manhã (7h - 19h)
1. Às 7h: Cria vídeo LOFI de 30 segundos
2. Cria live no YouTube
3. Inicia transmissão em loop do vídeo
4. Monitora até 19h
5. Para transmissão às 19h

### Bot da Noite (20h - 3h)
1. Às 20h: Cria vídeo noturno de 30 segundos (categoria aleatória)
2. Cria live no YouTube
3. Inicia transmissão em loop do vídeo
4. Monitora até 3h da manhã
5. Para transmissão às 3h

## 📝 Logs

Os logs são salvos em:
- `logs/morning_bot.log` - Bot da manhã
- `logs/night_bot.log` - Bot da noite

## 🔧 Manutenção

### Limpar Arquivos Temporários

```bash
# Remove frames temporários
rm -rf lofi_temp_frames/

# Remove áudio temporário
rm -f lofi_temp_audio.wav
```

### Verificar Status

```bash
# Ver logs em tempo real
tail -f logs/morning_bot.log
tail -f logs/night_bot.log
```

## 🐛 Troubleshooting

### Erro: "ffmpeg não encontrado"
Instale o ffmpeg (veja seção Requisitos)

### Erro: "Stream Key não disponível"
O YouTube pode levar alguns minutos para disponibilizar o stream_key. Aguarde ou obtenha manualmente no YouTube Studio.

### Erro: "Canal não habilitado para live streaming"
Seu canal precisa ter pelo menos 1,000 inscritos ou ser verificado pelo YouTube.

## 📄 Licença

Este projeto é de uso pessoal.

