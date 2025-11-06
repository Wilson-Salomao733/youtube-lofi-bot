# 🎬 Novo Fluxo Atualizado

## ✅ O que foi implementado:

### 1. **Sistema usa APENAS arquivos das pastas**
   - ❌ **NÃO gera mais** imagens automaticamente
   - ❌ **NÃO gera mais** áudio automaticamente
   - ✅ **USA** imagens da pasta `images/`
   - ✅ **USA** áudios da pasta `audios/`
   - ✅ **MISTURA** tudo aleatoriamente
   - ✅ **MANTÉM** animações nas imagens

### 2. **Tratamento de áudio**
   - Se áudio > 30s: **CORTA** para 30s (não faz loop)
   - Se áudio < 30s: **FAZ LOOP** até completar 30s

### 3. **Automação diária**
   - ⏰ **7h da manhã**: Cria vídeo de 30s (imagem aleatória + áudio aleatório)
   - 📺 **7h da manhã**: Inicia live pública no YouTube
   - 🔄 Vídeo roda em **loop infinito** na live
   - 🛑 **19h (7 da noite)**: Para a live automaticamente
   - 🔁 **Repete todo dia** automaticamente

### 4. **Docker configurado**
   - Sistema já está pronto para rodar em Docker
   - Usa `docker-compose.live.yml`

## 📋 Como testar ANTES de subir:

### 1. Criar vídeo de teste:
```bash
python3 test_video_30s.py
```

Isso vai:
- Pegar uma imagem aleatória de `images/`
- Pegar um áudio aleatório de `audios/`
- Criar vídeo de 30s com animações
- Mostrar o caminho do arquivo para você ver

### 2. Ver o vídeo:
```bash
# O script mostra o caminho, mas você pode abrir assim:
xdg-open lofi_video_*.mp4
```

### 3. Se estiver bom, ativar automação:
```bash
# Com Docker (recomendado):
docker compose -f docker-compose.live.yml up -d

# Ou sem Docker:
python3 automated_live_bot.py
```

## 📁 Estrutura de pastas:

```
YOUTUBE/
├── images/          # Coloque suas imagens aqui (PNG/JPG)
├── audios/          # Coloque seus áudios aqui (MP3/WAV)
├── output/          # Vídeos gerados vão aqui
└── credentials/     # Credenciais do YouTube
```

## ⚠️ Requisitos:

1. **Imagens**: Pelo menos 1 imagem em `images/`
2. **Áudios**: Pelo menos 1 áudio em `audios/`
3. **YouTube**: Live streaming habilitado no canal

## 🎯 Fluxo completo:

```
Dia 1, 7h:
├── 📹 Cria vídeo (imagem aleatória + áudio aleatório)
├── 📺 Cria live no YouTube
├── 🔄 Inicia streaming em loop
└── ⏰ Fica no ar até 19h

Dia 2, 7h:
├── 📹 Cria NOVO vídeo (outra imagem + outro áudio)
├── 📺 Cria NOVA live
└── 🔄 Repete...

...e assim por diante!
```

## 💡 Dicas:

- Quanto mais imagens e áudios você colocar, mais variedade terá
- Cada dia terá uma combinação diferente
- O sistema escolhe **aleatoriamente** a cada dia
- Se faltar arquivo, o sistema **NÃO funciona** (não gera mais automaticamente)

