# 🎬 Guia Completo: Criar Live no YouTube com OBS

## 🚀 Resumo Rápido:

1. **Criar a live no YouTube** (script faz isso)
2. **Configurar OBS Studio** para transmitir
3. **Usar vídeo de 30s em loop infinito** no OBS
4. **Iniciar transmissão** e deixar rodando

---

## 📋 Passo 1: Criar a Live no YouTube

```bash
# Usando vídeo existente
python create_live.py --video lofi_video_20251101_234638.mp4

# Ou criar vídeo novo automaticamente
python create_live.py
```

O script vai:
- ✅ Criar a live pública no YouTube
- ✅ Gerar **Stream Key** e **RTMP URL**
- ✅ Mostrar todas as informações necessárias

---

## 🎥 Passo 2: Configurar OBS Studio

### 2.1 Instalar OBS Studio
- Download: https://obsproject.com/
- Instale no seu sistema

### 2.2 Configurar Transmissão no OBS

1. **Abra OBS Studio**
2. **Vá em: Configurações → Transmissão** (ou Settings → Stream)
3. **Configure:**
   - **Serviço**: YouTube / YouTube Gaming
   - **Servidor**: Use a RTMP URL fornecida pelo script
   - **Chave de transmissão**: Use a Stream Key fornecida pelo script

   > 💡 Se não tiver a Stream Key, vá no YouTube Studio:
   > - https://studio.youtube.com/
   > - Transmissões → Transmitir agora
   > - Copie a Stream Key de lá

4. **Clique em "OK"**

### 2.3 Adicionar Vídeo como Fonte

1. **Na área de "Cenas"** (Scenes), clique com botão direito
2. **Adicionar → Fonte de Mídia** (Media Source)
3. **Configure:**
   - **Nome**: "LOFI Video Loop"
   - **Local**: Clique em "Navegar" e escolha seu vídeo de 30s
     - Exemplo: `lofi_video_20251101_234638.mp4`
   - **IMPORTANTE**: Marque ✅ **"Repetir quando o arquivo terminar"**
   - **IMPORTANTE**: Desmarque "Reproduzir quando a fonte se torna visível" (ou marque, dependendo)
   - Clique em **"OK"**

4. **Ajuste o tamanho do vídeo** se necessário:
   - Clique na fonte na cena
   - Arraste os cantos para ajustar ao tamanho da tela

### 2.4 Configurar Áudio (Opcional)

Se quiser adicionar mais áudio ou ajustar volume:
1. **Configurações → Áudio**
2. Configure os níveis de áudio desejados

### 2.5 Testar Transmissão

1. **Clique em "Iniciar transmissão"** no OBS (botão inferior direito)
2. **Verifique no YouTube Studio** se a transmissão está ativa
3. **Acesse o link da live** para ver se está funcionando

---

## 🔄 Passo 3: Loop Infinito do Vídeo

O vídeo vai fazer loop **automaticamente** porque você marcou:
- ✅ **"Repetir quando o arquivo terminar"**

O vídeo de 30 segundos vai repetir infinitamente enquanto a transmissão estiver ativa.

---

## ⚙️ Configurações Avançadas do OBS

### Qualidade da Transmissão

1. **Configurações → Vídeo**
2. **Resolução de Saída**: 1920x1080 (ou a resolução do seu vídeo)
3. **FPS**: 30 (recomendado)

### Bitrate

1. **Configurações → Transmissão → Avançado**
2. **Bitrate**: 4000-6000 Kbps (para 1080p)
   - Para internet mais lenta: 2500-4000 Kbps
   - Para internet rápida: 6000-8000 Kbps

---

## 📱 Monitorar a Live

### Durante a Transmissão:

1. **YouTube Studio**: https://studio.youtube.com/
   - Veja estatísticas em tempo real
   - Visualizações, comentários, etc.

2. **Link da Live**: `https://www.youtube.com/watch?v=SEU_BROADCAST_ID`
   - Abra em outra aba para acompanhar

---

## 🛑 Como Parar a Live

1. **No OBS**: Clique em "Parar transmissão"
2. **No YouTube Studio**: Termine a transmissão
3. **Ou**: Deixe rodando indefinidamente para uma live 24/7

---

## 🎯 Exemplo Completo:

```bash
# 1. Criar live
python create_live.py --video lofi_video_20251101_234638.mp4

# 2. O script vai mostrar:
#    - Stream Key: xxxx-xxxx-xxxx-xxxx
#    - RTMP URL: rtmp://a.rtmp.youtube.com/live2/xxxx

# 3. Configure OBS com essas informações
# 4. Adicione o vídeo como fonte com "Repetir quando terminar"
# 5. Inicie transmissão
# 6. Pronto! Live no ar com loop infinito
```

---

## ❓ Troubleshooting

### Vídeo não faz loop?
- Verifique se marcou ✅ "Repetir quando o arquivo terminar" na fonte de mídia

### Stream não inicia?
- Verifique se a Stream Key está correta
- Verifique sua conexão com internet
- Confira se o bitrate não está muito alto para sua internet

### Vídeo com qualidade ruim?
- Aumente o bitrate no OBS
- Certifique-se que o vídeo original é de boa qualidade (1080p)

### Live não aparece no YouTube?
- Aguarde alguns minutos após iniciar a transmissão
- Verifique no YouTube Studio se a transmissão está ativa
- Certifique-se que criou a live como "pública"

---

## 🎉 Dicas Finais:

- ✅ Deixe OBS rodando em segundo plano
- ✅ Monitore a live periodicamente
- ✅ Use vídeo de alta qualidade (1080p)
- ✅ Mantenha a conexão estável
- ✅ Para 24/7, deixe o computador ligado ou use VPS

