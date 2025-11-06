# 🕐 Como o Bot Roda Automaticamente às 7h

## 📋 Duas Formas de Funcionar

### **Opção 1: Bot Rodando 24/7 (Atual - com `schedule`)**

**Como funciona:**
1. Você inicia o bot uma vez: `./start_bot_7h.sh`
2. O bot fica rodando em background 24/7
3. A cada minuto, verifica se é 7h da manhã
4. Quando chega 7h, executa o workflow automaticamente
5. Às 19h, para a live automaticamente
6. Aguarda até o próximo dia às 7h

**Vantagens:**
- ✅ Simples de configurar
- ✅ Monitora o streaming e reinicia se cair
- ✅ Logs centralizados

**Desvantagens:**
- ⚠️ Precisa ficar rodando 24/7 (consome um pouco de memória)
- ⚠️ Se o computador reiniciar, precisa iniciar o bot novamente

**Código que faz isso:**
```python
# Em automated_live_bot.py, linha 343
schedule.every().day.at("07:00").do(
    lambda: threading.Thread(target=self.daily_workflow, daemon=True).start()
)

# Loop que verifica a cada minuto
while True:
    schedule.run_pending()  # Verifica se é hora de executar
    time.sleep(60)  # Aguarda 1 minuto
```

---

### **Opção 2: Usando Cron do Linux (Alternativa)**

**Como funciona:**
1. O sistema Linux (cron) executa o script todo dia às 7h
2. Não precisa de processo rodando 24/7
3. Mais eficiente em termos de recursos

**Vantagens:**
- ✅ Não consome recursos quando não está executando
- ✅ Mais confiável (não depende de processo Python rodando)
- ✅ Reinicia automaticamente se o sistema reiniciar

**Desvantagens:**
- ⚠️ Não monitora o streaming durante o dia (mas pode adicionar)
- ⚠️ Precisa configurar o cron manualmente

---

## 🚀 Como Usar Cada Opção

### **Opção 1: Bot 24/7 (Recomendado para monitoramento)**

```bash
# Iniciar bot
./start_bot_7h.sh

# Ver logs
tail -f automated_live.log

# Parar bot
kill $(cat automated_live.pid)
```

**O bot vai:**
- ✅ Rodar 24/7 em background
- ✅ Todo dia às 7h: criar vídeo e live
- ✅ Monitorar streaming até 19h
- ✅ Reiniciar streaming se cair

---

### **Opção 2: Cron (Mais eficiente)**

```bash
# Configurar cron (executa uma vez)
crontab -e

# Adicionar esta linha:
0 7 * * * cd /home/wilsonsalomo/Documentos/YOUTUBE && /usr/bin/python3 run_workflow_now.py >> automated_live.log 2>&1
```

**O cron vai:**
- ✅ Executar o script todo dia às 7h
- ✅ Criar vídeo e iniciar live
- ✅ Não precisa de processo rodando 24/7

**Mas atenção:**
- ⚠️ O streaming precisa continuar rodando até 19h
- ⚠️ Se o streaming cair, não reinicia automaticamente (a menos que você configure)

---

## 💡 Recomendação

**Use a Opção 1 (Bot 24/7)** se você quer:
- Monitoramento automático do streaming
- Reinício automático se o streaming cair
- Logs centralizados

**Use a Opção 2 (Cron)** se você quer:
- Economizar recursos do sistema
- Não ter processo rodando 24/7
- Confiar que o streaming não vai cair

---

## 🔍 Verificar se Está Funcionando

### **Opção 1 (Bot 24/7):**
```bash
# Ver se o processo está rodando
ps aux | grep automated_live_bot

# Ver logs
tail -f automated_live.log

# Ver PID
cat automated_live.pid
```

### **Opção 2 (Cron):**
```bash
# Ver se o cron está configurado
crontab -l

# Ver logs do último dia
grep "$(date +%Y-%m-%d)" automated_live.log
```

---

## ⚙️ Configuração Atual

**Atualmente você está usando a Opção 1** (bot rodando 24/7).

O bot está configurado para:
- ✅ Verificar a cada minuto se é 7h
- ✅ Executar workflow quando chegar 7h
- ✅ Monitorar streaming até 19h
- ✅ Reiniciar streaming se cair

**Para mudar para Cron**, você precisaria:
1. Parar o bot atual: `kill $(cat automated_live.pid)`
2. Configurar cron: `crontab -e`
3. Adicionar linha de agendamento

