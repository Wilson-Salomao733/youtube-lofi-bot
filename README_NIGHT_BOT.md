# 🌙 Bot Noturno - Sons da Natureza

Bot automatizado que cria vídeos com sons da natureza e inicia lives no YouTube das **20h às 3h da manhã**.

## 📋 Funcionamento

1. **Às 20h (8h da noite):**
   - Seleciona uma categoria aleatória (Chuva, Fogueira, Fazenda, Praia, Som de pessoas)
   - Escolhe uma imagem dessa categoria
   - Escolhe um áudio da mesma categoria
   - Cria vídeo de 30 segundos com movimento na imagem
   - Cria live no YouTube
   - Inicia streaming em loop infinito

2. **Das 20h às 3h:**
   - Vídeo fica em loop na live
   - Sistema monitora e reinicia se cair

3. **Às 3h da manhã:**
   - Live é encerrada automaticamente

## 📁 Estrutura de Pastas

```
YOUTUBE/
├── imagens noite/
│   ├── Chuva/
│   │   └── *.jpg
│   ├── Fogueira/
│   │   └── *.jpg
│   ├── Fazenda/
│   │   └── *.jpg
│   ├── Praia/
│   │   └── *.jpg
│   └── Som de pessoas/
│       └── *.jpg
│
└── audio_noite/
    ├── Chuva/
    │   └── *.mp3
    ├── Fogueira/
    │   └── *.mp3
    ├── Fazenda/
    │   └── *.mp3
    ├── Praia/
    │   └── *.mp3
    └── Som de pessoas/
        └── *.mp3
```

**IMPORTANTE:** A imagem e o áudio devem estar na mesma categoria!

## 🚀 Como Usar

### Opção 1: Docker (Recomendado)

```bash
# Inicia ambos os bots (LOFI + Noturno)
docker compose -f docker-compose.live.yml up -d

# Ver logs do bot noturno
docker logs -f night-live-bot

# Parar
docker compose -f docker-compose.live.yml down
```

### Opção 2: Manual

```bash
# Executa o bot
./start_night_bot.sh

# Ou diretamente
python3 automated_night_bot.py
```

### Opção 3: Testar Criação de Vídeo

```bash
# Testa criação de vídeo (10 segundos)
python3 test_night_video.py
```

## ⚙️ Configuração

O bot usa as mesmas credenciais do bot LOFI (`credentials/`).

## 📊 Logs

Logs são salvos em: `logs/automated_night.log`

```bash
# Ver logs em tempo real
tail -f logs/automated_night.log
```

## 🎯 Categorias Disponíveis

- **Chuva**: Sons de chuva + imagens de chuva
- **Fogueira**: Sons de fogueira + imagens de fogueira
- **Fazenda**: Sons da fazenda + imagens da fazenda
- **Praia**: Ondas do mar + imagens de praia
- **Som de pessoas**: Ambiente com pessoas + imagens relacionadas

## ⏰ Horários

- **Início**: 20h (8h da noite)
- **Fim**: 3h da manhã
- **Duração**: ~7 horas

## 🔄 Diferenças do Bot LOFI

| Aspecto | Bot LOFI | Bot Noturno |
|---------|----------|-------------|
| Horário | 7h-19h | 20h-3h |
| Conteúdo | Música LOFI | Sons da Natureza |
| Categorias | Aleatório | Categoria específica (imagem + áudio) |
| Público | Estudo/Trabalho | Sono/Relaxamento |

## 🐛 Troubleshooting

### Erro: "Nenhuma categoria encontrada"
- Verifique se as pastas `imagens noite` e `audio_noite` existem
- Verifique se há subpastas dentro delas

### Erro: "Nenhuma imagem encontrada"
- Verifique se há arquivos .jpg/.png na categoria selecionada

### Erro: "Nenhum áudio encontrado"
- Verifique se há arquivos .mp3/.wav na categoria selecionada

### Live não inicia
- Verifique as credenciais do YouTube em `credentials/`
- Verifique se o stream_key está configurado

---

**Desenvolvido para automatizar lives noturnas com sons da natureza** 🌙

