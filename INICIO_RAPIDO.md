# 🚀 Início Rápido - Bot Automatizado de Live

## ✅ Setup em 3 Passos:

### 1️⃣ Instalar ffmpeg:
```bash
sudo apt-get install ffmpeg  # Linux
# ou
brew install ffmpeg  # macOS
```

### 2️⃣ Configurar YouTube API:
- Baixe `credentials.json` do Google Cloud Console
- Coloque em: `credentials/credentials.json`
- Na primeira execução, autorize no navegador

### 3️⃣ Iniciar Bot:

**Opção A: Com Docker (Melhor para 24/7)**
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

## 🎯 O que acontece automaticamente:

```
Todo dia às 7h:
├── Cria vídeo de 30s
├── Cria live pública no YouTube  
├── Inicia transmissão (vídeo em loop)
└── Para às 18h automaticamente

No dia seguinte → Repete tudo!
```

---

## 📊 Verificar Status:

```bash
# Ver logs em tempo real
tail -f automated_live.log

# Com Docker
docker-compose -f docker-compose.live.yml logs -f
```

---

## 🎉 Pronto!

O bot vai rodar **24/7** e fazer tudo automaticamente!

**ZERO INTERVENÇÃO MANUAL NECESSÁRIA!** 🚀

---

Para mais detalhes: `AUTOMATED_LIVE_SETUP.md`


