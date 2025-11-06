# 🤖 Bot Automatizado de Live LOFI - Guia Rápido

## 🎯 Funcionamento:

```
Todo dia às 7h → Cria vídeo 30s → Cria live → Transmite até 18h → Repete no dia seguinte
```

**100% AUTOMÁTICO - ZERO INTERVENÇÃO!**

---

## 🚀 Início Rápido:

### 1. Instalar ffmpeg:
```bash
sudo apt-get install ffmpeg  # Linux
brew install ffmpeg          # macOS
```

### 2. Configurar YouTube API:
- Credenciais em: `credentials/credentials.json`
- Autorize na primeira execução

### 3. Iniciar Bot:

**Opção A: Com Docker (Recomendado)**
```bash
docker-compose -f docker-compose.live.yml up -d
```

**Opção B: Script Simples**
```bash
./start_automated_live.sh
```

**Opção C: Manual**
```bash
python automated_live_bot.py
```

---

## 📋 O que acontece:

1. **07:00** - Bot cria vídeo de 30s automaticamente
2. **07:02** - Bot cria live pública no YouTube
3. **07:03** - Bot inicia transmissão (vídeo em loop infinito)
4. **07:03 - 17:59** - Live no ar, streaming contínuo
5. **18:00** - Bot para streaming automaticamente
6. **Próximo dia 07:00** - Repete tudo

---

## 📊 Monitorar:

```bash
# Ver logs
tail -f automated_live.log

# Com Docker
docker-compose -f docker-compose.live.yml logs -f
```

---

## ✅ Pronto!

O bot vai rodar 24/7 e fazer tudo automaticamente! 🎉

Para mais detalhes: `AUTOMATED_LIVE_SETUP.md`

