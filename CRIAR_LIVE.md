# 🎬 Como Criar Live Pública no YouTube (Transmitir via OBS)

## 🚀 Passo a Passo Rápido:

### 1️⃣ Atualizar Usuários de Teste (IMPORTANTE)

Primeiro, remova o email antigo e mantenha apenas `lofiwilson0@gmail.com`:

1. Acesse: https://console.cloud.google.com/apis/credentials/consent
2. Vá em **"Usuários de teste"**
3. Remova `wilsonsalomao733@gmail.com`
4. Salve as alterações

> 📋 Instruções detalhadas em: `ATUALIZAR_USUARIOS_TESTE.md`

### 2️⃣ Criar Live no YouTube

**Opção A: Usar vídeo existente de 30s**
```bash
python create_live.py --video lofi_video_20251101_234638.mp4
```

**Opção B: Criar novo vídeo de 30s automaticamente**
```bash
python create_live.py
```

> ⚠️ **IMPORTANTE**: O script **NÃO** faz upload do vídeo!
> Ele apenas **CRIA A LIVE** no YouTube e fornece as informações para você transmitir via **OBS Studio**.

### 3️⃣ Parâmetros Disponíveis

```bash
python create_live.py \
  --video VIDEO.mp4 \          # Vídeo de 30s (None = cria novo)
  --title "Meu Live LOFI" \    # Título customizado
  --description "Descrição" \  # Descrição customizada
  --scheduled 10                # Minutos até começar (padrão: 10)
```

## 📝 Exemplos:

### Live com vídeo existente
```bash
python create_live.py --video lofi_video_20251101_234638.mp4
```

### Live com título customizado
```bash
python create_live.py \
  --video lofi_video_20251101_234638.mp4 \
  --title "LOFI Hip Hop - Live 24/7 Study Mix 🎵"
```

### Criar vídeo novo e live automático
```bash
python create_live.py
```

## 🎯 O que o script faz:

1. ✅ Cria/usa vídeo de 30s
2. ✅ **Cria live público no YouTube**
3. ✅ **Gera Stream Key e RTMP URL**
4. ✅ Agenda para começar em 10 minutos (ou tempo especificado)
5. ✅ **Mostra instruções para configurar OBS**

## 📤 Próximos Passos Após Criar o Live:

### 3️⃣ Configurar OBS Studio para Transmitir

1. O script vai mostrar:
   - **Stream Key** (chave de transmissão)
   - **RTMP URL** (servidor)
   - **Link da live**

2. **Configure OBS Studio:**
   - Abra OBS Studio
   - Configurações → Transmissão
   - Serviço: YouTube / YouTube Gaming
   - Cole a **Stream Key** e **RTMP URL**
   - Adicione o vídeo de 30s como fonte
   - **Marque: "Repetir quando o arquivo terminar"**
   - Clique em "Iniciar transmissão"

3. **O vídeo vai fazer loop infinito automaticamente!**

> 📋 **Guia completo do OBS em:** `GUIA_OBS_LIVE.md`

## 🔗 Links Úteis:

- Google Cloud Console: https://console.cloud.google.com/
- OAuth Consent Screen: https://console.cloud.google.com/apis/credentials/consent
- YouTube Studio: https://studio.youtube.com/
- OBS Studio Download: https://obsproject.com/
- Guia Completo OBS: `GUIA_OBS_LIVE.md`

## 💡 Resumo:

✅ **Script cria a LIVE** → Fornece Stream Key → Você configura OBS → Transmite vídeo em loop infinito!

