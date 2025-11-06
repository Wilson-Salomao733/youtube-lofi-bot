# 🔑 Como Obter Stream Key Manualmente do YouTube

## 📋 Passo a Passo

### 1️⃣ Acesse o YouTube Studio
```
https://studio.youtube.com/
```

### 2️⃣ Vá em "Transmissões" (Live)
- No menu lateral esquerdo, clique em **"Conteúdo"**
- Depois clique em **"Transmissões"** (ou "Live" em inglês)

### 3️⃣ Encontre sua Live
- Procure pela live que foi criada (geralmente aparece como "Agendada" ou "Ao vivo")
- Clique na live que você quer transmitir

### 4️⃣ Obtenha o Stream Key
- Dentro da página da live, procure por **"Configuração do encoder"** ou **"Encoder settings"**
- Você verá:
  - **URL do servidor RTMP**: `rtmp://a.rtmp.youtube.com/live2`
  - **Chave de transmissão (Stream Key)**: Uma string longa (ex: `xxxx-xxxx-xxxx-xxxx`)

### 5️⃣ Use no Código
Se precisar usar manualmente, você pode:
1. Copiar o **Stream Key**
2. Copiar a **URL do servidor RTMP**
3. Executar o ffmpeg manualmente:

```bash
ffmpeg -re -stream_loop -1 -i seu_video.mp4 \
  -c:v libx264 -preset veryfast -maxrate 4000k -bufsize 8000k \
  -c:a aac -b:a 128k \
  -f flv \
  rtmp://a.rtmp.youtube.com/live2/SEU_STREAM_KEY_AQUI
```

## 🎯 Alternativa: Usar o Broadcast ID

Se você tem o **Broadcast ID** da live (que aparece nos logs), pode acessar diretamente:

```
https://studio.youtube.com/video/SEU_BROADCAST_ID/edit
```

Exemplo:
```
https://studio.youtube.com/video/27vGJLO4WeA/edit
```

## 📝 Onde Encontrar no YouTube Studio

1. **YouTube Studio** → **Conteúdo** → **Transmissões**
2. Clique na live desejada
3. Role até **"Configuração do encoder"** ou **"Encoder settings"**
4. Lá você encontrará:
   - **Servidor RTMP**: `rtmp://a.rtmp.youtube.com/live2`
   - **Chave de transmissão**: (string longa)

## ⚠️ Importante

- O **Stream Key** é sensível - não compartilhe publicamente
- Cada live tem seu próprio Stream Key único
- O Stream Key pode mudar se você criar uma nova live

## 🔧 Se o Stream Key Não Aparecer

1. Certifique-se de que a live está **agendada** ou **ativa**
2. Verifique se o canal está **habilitado para live streaming**
3. Tente aguardar alguns minutos após criar a live
4. Recarregue a página do YouTube Studio

