# 🚀 COMO FUNCIONA AGORA

## ✅ O QUE MUDOU

### 🎯 Tudo roda no Docker
- **NADA** roda na sua máquina
- Todos os processos Python foram parados
- Tudo está isolado no Docker

### 🕐 Detecção Automática de Horário
Quando o container Docker inicia, os bots **automaticamente** detectam o horário:

- **Se for entre 7h e 19h**: Executa fluxo da **MANHÃ** (LOFI)
- **Se for fora desse horário** (antes das 7h ou depois das 19h): Executa fluxo da **NOITE** (Sons da Natureza)

Depois disso, continua agendado normalmente:
- **7h**: Fluxo da manhã
- **20h**: Fluxo da noite

## 🚀 COMO INICIAR

Execute **UMA VEZ**:

```bash
./iniciar_limpo.sh
```

Este script:
1. ✅ Para todos os processos Python na máquina
2. ✅ Para containers Docker existentes
3. ✅ Reconstrói a imagem (se necessário)
4. ✅ Inicia tudo no Docker

**Pronto!** Tudo vai rodar automaticamente.

## 🔄 O QUE ACONTECE

### Quando você liga o container (qualquer horário):

1. **Bot detecta o horário atual**
2. **Se for 7h-19h**: 
   - Executa fluxo da manhã AGORA
   - Agenda para amanhã às 7h
3. **Se for fora de 7h-19h**:
   - Executa fluxo da noite AGORA
   - Agenda para hoje às 20h (ou amanhã se já passou)

### Depois disso, tudo é automático:

- **Todo dia às 7h**: Fluxo da manhã
- **Todo dia às 20h**: Fluxo da noite

## 📋 COMANDOS ÚTEIS

### Ver logs em tempo real
```bash
docker compose logs -f
```

### Ver apenas últimas 50 linhas
```bash
docker compose logs --tail=50
```

### Parar tudo
```bash
docker compose down
```

### Reiniciar
```bash
docker compose restart
```

### Ver status
```bash
docker compose ps
```

## ✅ GARANTIAS

- ✅ **Tudo no Docker**: Nada roda na sua máquina
- ✅ **Reinício automático**: Docker reinicia se parar
- ✅ **Detecção de horário**: Funciona em qualquer horário
- ✅ **Agendamento contínuo**: Sempre agendado para os próximos horários
- ✅ **Tratamento de erros**: Continua funcionando mesmo com erros

## 🎉 RESULTADO

**Você não precisa fazer NADA!**

1. Execute `./iniciar_limpo.sh` **UMA VEZ**
2. Os bots detectam o horário e executam o fluxo apropriado
3. Tudo continua automático todos os dias

**É 100% AUTOMÁTICO E ISOLADO NO DOCKER!** 🚀

