# 🐳 Bot de Live com Docker - Guia Rápido

## 🚀 Início Rápido

### **1. Iniciar Container:**
```bash
./docker_live_start.sh
```

### **2. Parar Container:**
```bash
./docker_live_stop.sh
```

### **3. Ver Status:**
```bash
./docker_live_status.sh
```

### **4. Ver Logs:**
```bash
# Logs do container
docker logs -f lofi-live-bot

# Logs do arquivo
tail -f logs/automated_live.log
```

---

## ⏰ Como Funciona

- ✅ Container verifica horário **a cada 1 hora**
- ✅ Todo dia às **7h**: cria vídeo e inicia live
- ✅ Todo dia às **19h**: encerra live automaticamente
- ✅ Você pode **ligar/desligar** quando quiser

---

## 📁 Pastas Importantes

- `output/` - Vídeos criados ficam aqui
- `logs/` - Logs do bot ficam aqui
- `images/` - Imagens para usar nos vídeos
- `audios/` - Áudios para usar nos vídeos
- `credentials/` - Credenciais do YouTube

---

## ⚙️ Requisitos

- ✅ Docker instalado e rodando
- ✅ `credentials/credentials.json` configurado
- ✅ Pelo menos 1 imagem em `images/`
- ✅ Pelo menos 1 áudio em `audios/`

---

## 🔄 Fluxo Diário

1. **7h da manhã**: Container detecta horário
2. **Cria vídeo** de 30 segundos
3. **Salva em** `output/`
4. **Cria live** no YouTube
5. **Inicia streaming** em loop
6. **19h**: Para streaming automaticamente
7. **Aguarda** até próximo dia às 7h

---

## 💡 Dicas

- Container precisa estar **rodando** para executar às 7h
- Se parar o container, ele **não executará** até iniciar novamente
- Verifica a cada 1 hora, então pode ter até 1 hora de atraso
- Vídeos ficam salvos em `output/` mesmo após parar container

---

## 🆘 Problemas?

**Container não inicia:**
```bash
docker logs lofi-live-bot
```

**Ver se está rodando:**
```bash
docker ps | grep lofi-live-bot
```

**Reiniciar:**
```bash
docker compose -f docker-compose.live.yml restart
```

