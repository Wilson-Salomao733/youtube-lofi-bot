# 🐳 Docker - TUDO dentro do container, NADA na máquina

## ✅ CONFIGURAÇÃO FINAL

**TUDO roda dentro do container Docker.**
**NADA roda na sua máquina.**

---

## 🚀 Como Usar

### **Iniciar (TUDO dentro do Docker):**
```bash
./docker_live_start.sh
```

Isso vai:
- ✅ Parar qualquer processo Python na máquina
- ✅ Iniciar container Docker
- ✅ TUDO roda dentro do container

### **Parar:**
```bash
./docker_live_stop.sh
```

### **Parar TUDO (máquina + Docker):**
```bash
./STOP_ALL.sh
```

### **Ver Status:**
```bash
./docker_live_status.sh
```

### **Ver Logs:**
```bash
docker logs -f lofi-live-bot
```

---

## 📋 O que acontece

1. Você executa `./docker_live_start.sh`
2. Script para qualquer processo Python na máquina
3. Inicia container Docker
4. **TUDO roda dentro do container:**
   - ✅ Bot Python
   - ✅ Verificação de horário
   - ✅ Criação de vídeo
   - ✅ Live no YouTube
   - ✅ Streaming FFmpeg
5. **NADA roda na sua máquina**

---

## ⏰ Funcionamento

- Container verifica horário **a cada 1 hora**
- Todo dia às **7h**: cria vídeo e inicia live
- Todo dia às **19h**: encerra live
- Você pode **ligar/desligar** quando quiser

---

## 📁 Volumes (pastas compartilhadas)

O Docker mapeia estas pastas:

```
Sua máquina          →    Container
─────────────────────────────────
./credentials/      →    /app/credentials
./images/           →    /app/images
./audios/           →    /app/audios
./output/           →    /app/output
./logs/             →    /app/logs
```

**Vídeos criados ficam em `./output/` na sua máquina**
**Logs ficam em `./logs/` na sua máquina**

---

## ⚠️ IMPORTANTE

- ✅ **TUDO roda dentro do Docker**
- ✅ **NADA roda na sua máquina**
- ✅ Container precisa estar **rodando** para executar às 7h
- ✅ Se parar o container, **nada executa** até iniciar novamente

---

## 🆘 Comandos Úteis

```bash
# Ver se container está rodando
docker ps | grep lofi-live-bot

# Ver logs em tempo real
docker logs -f lofi-live-bot

# Reiniciar container
docker compose -f docker-compose.live.yml restart

# Reconstruir (após mudanças no código)
docker compose -f docker-compose.live.yml build --no-cache
docker compose -f docker-compose.live.yml up -d
```

---

## ✅ Resumo

**ANTES (errado):**
- ❌ Scripts Python rodando na máquina
- ❌ Processos em background
- ❌ Consumo de recursos na máquina

**AGORA (correto):**
- ✅ TUDO dentro do Docker
- ✅ NADA na máquina
- ✅ Isolado e limpo
- ✅ Ligar/desligar quando quiser

