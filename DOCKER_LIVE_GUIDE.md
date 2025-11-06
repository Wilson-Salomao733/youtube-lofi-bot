# 🐳 Guia: Bot de Live com Docker

## 📋 Como Funciona

O bot roda em um **container Docker** que você pode ligar e desligar quando quiser.

**Funcionamento:**
- ✅ Container verifica horário **a cada 1 hora** (não a cada minuto)
- ✅ Todo dia às **7h da manhã**: cria vídeo e inicia live
- ✅ Todo dia às **19h**: encerra live automaticamente
- ✅ Você pode **ligar/desligar** o container quando quiser

---

## 🚀 Comandos Principais

### **Iniciar Container:**
```bash
./docker_live_start.sh
```

Isso vai:
1. Construir a imagem Docker (primeira vez)
2. Iniciar o container em background
3. Container fica rodando até você parar

### **Parar Container:**
```bash
./docker_live_stop.sh
```

### **Ver Status:**
```bash
./docker_live_status.sh
```

### **Ver Logs em Tempo Real:**
```bash
docker logs -f lofi-live-bot
```

---

## 📁 Estrutura de Volumes

O Docker mapeia estas pastas do seu computador para dentro do container:

```
Seu computador          →    Container
─────────────────────────────────────
./credentials/          →    /app/credentials
./images/               →    /app/images
./audios/               →    /app/audios
./output/               →    /app/output
./automated_live.log    →    /app/automated_live.log
```

**Isso significa:**
- ✅ Vídeos criados ficam em `./output/` no seu computador
- ✅ Logs ficam em `./automated_live.log` no seu computador
- ✅ Você pode adicionar imagens/áudios nas pastas e o container vê

---

## ⏰ Horários de Execução

**7h da Manhã (07:00):**
- Container verifica se é 7h (a cada 1 hora)
- Quando detecta 7h, executa:
  1. Cria vídeo de 30 segundos
  2. Salva em `output/`
  3. Cria live no YouTube
  4. Inicia streaming em loop

**19h (19:00):**
- Container detecta que é 19h
- Para o streaming automaticamente
- Aguarda até o próximo dia às 7h

---

## 🔍 Verificar se Está Funcionando

### **Ver se container está rodando:**
```bash
docker ps | grep lofi-live-bot
```

### **Ver logs:**
```bash
# Últimas 50 linhas
docker logs --tail 50 lofi-live-bot

# Em tempo real
docker logs -f lofi-live-bot
```

### **Ver logs do arquivo:**
```bash
tail -f automated_live.log
```

---

## ⚙️ Configuração

### **Requisitos:**
- ✅ Docker instalado e rodando
- ✅ `credentials/credentials.json` configurado
- ✅ Pasta `images/` com pelo menos 1 imagem
- ✅ Pasta `audios/` com pelo menos 1 áudio

### **Timezone:**
O container está configurado para `America/Sao_Paulo`.
Para mudar, edite `docker-compose.live.yml`:
```yaml
environment:
  - TZ=America/Sao_Paulo  # Mude aqui
```

---

## 🛠️ Comandos Docker Diretos

Se preferir usar comandos Docker diretamente:

```bash
# Iniciar
docker compose -f docker-compose.live.yml up -d

# Parar
docker compose -f docker-compose.live.yml down

# Ver logs
docker logs -f lofi-live-bot

# Reiniciar
docker compose -f docker-compose.live.yml restart

# Reconstruir (após mudanças no código)
docker compose -f docker-compose.live.yml build --no-cache
docker compose -f docker-compose.live.yml up -d
```

---

## 💡 Vantagens do Docker

✅ **Isolado**: Não interfere com outros programas
✅ **Portável**: Funciona igual em qualquer máquina
✅ **Fácil de gerenciar**: Ligar/desligar com um comando
✅ **Reinicia sozinho**: Se o Docker reiniciar, o container volta
✅ **Logs centralizados**: Fácil de ver o que está acontecendo

---

## 🔄 Fluxo Completo

1. **Você inicia o container**: `./docker_live_start.sh`
2. **Container fica rodando** em background
3. **A cada 1 hora**, verifica se é 7h
4. **Quando chega 7h**, executa workflow:
   - Cria vídeo
   - Inicia live
   - Streaming roda até 19h
5. **Às 19h**, para streaming
6. **Aguarda** até próximo dia às 7h
7. **Repete** o ciclo

**Você pode parar/ligar quando quiser!**

---

## ⚠️ Importante

- O container precisa estar **rodando** para executar às 7h
- Se você parar o container, ele **não executará** até você iniciar novamente
- O container verifica **a cada 1 hora**, então pode ter até 1 hora de atraso
- Se você reiniciar o computador, o Docker pode reiniciar o container automaticamente (depende da configuração)

---

## 🆘 Troubleshooting

**Container não inicia:**
```bash
# Ver erros
docker logs lofi-live-bot

# Reconstruir
docker compose -f docker-compose.live.yml build --no-cache
```

**Logs não aparecem:**
```bash
# Ver direto no container
docker exec -it lofi-live-bot tail -f /app/automated_live.log
```

**Container para sozinho:**
```bash
# Ver por que parou
docker logs lofi-live-bot

# Reiniciar
docker compose -f docker-compose.live.yml restart
```

