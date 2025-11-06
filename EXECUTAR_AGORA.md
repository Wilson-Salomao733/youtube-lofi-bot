# 🚀 Executar Workflow Agora

## Para executar o workflow completo AGORA mesmo:

```bash
./run_workflow_now.sh
```

ou

```bash
python3 run_workflow_now.py
```

Isso vai:
1. ✅ Criar um vídeo de 30 segundos
2. ✅ Salvar o vídeo na pasta `output/`
3. ✅ Criar a live no YouTube
4. ✅ Iniciar a transmissão em loop até 19h

---

## 🤖 Configurar Bot Automático (7h da manhã)

Para que o bot rode automaticamente todo dia às 7h:

```bash
./start_bot_7h.sh
```

O bot vai:
- ✅ Rodar 24/7 em background
- ✅ Todo dia às 7h: criar vídeo e iniciar live
- ✅ Todo dia às 19h: encerrar live automaticamente

**Ver logs:**
```bash
tail -f automated_live.log
```

**Parar bot:**
```bash
kill $(cat automated_live.pid)
```

---

## 📁 Pasta Output

Todos os vídeos criados são salvos automaticamente na pasta `output/`:
- `output/lofi_video_YYYYMMDD_HHMMSS.mp4`

---

## ⚙️ Configuração

Certifique-se de ter:
- ✅ `credentials/credentials.json` configurado
- ✅ `ffmpeg` instalado
- ✅ Pasta `images/` com imagens
- ✅ Pasta `audios/` com áudios

