# 🎬 Configuração do YouTube API

Este guia explica como configurar a API do YouTube para uploads automáticos.

## 📋 Pré-requisitos

1. Conta Google com acesso ao YouTube
2. Projeto no Google Cloud Console

## 🔧 Passo a Passo

### 1. Criar Projeto no Google Cloud Console

1. Acesse: https://console.cloud.google.com/
2. Clique em **"Selecionar um projeto"** ou crie novo
3. Clique em **"Novo Projeto"**
4. Nome: "LOFI Bot YouTube"
5. Clique em **"Criar"**

### 2. Ativar YouTube Data API v3

1. No menu lateral, vá em **"APIs e Serviços"** -> **"Biblioteca"**
2. Busque por **"YouTube Data API v3"**
3. Clique e depois em **"Ativar"**

### 3. Criar Credenciais OAuth 2.0

1. Vá em **"APIs e Serviços"** -> **"Credenciais"**
2. Clique em **"Criar credenciais"** -> **"ID do cliente OAuth"**
3. Se pedir configurar OAuth, clique em **"Configurar tela de consentimento"**:
   - Tipo de usuário: **Externo**
   - Nome do app: "LOFI Bot"
   - Email do suporte: (seu email)
   - Domínios autorizados: deixe vazio
   - Informações do desenvolvedor: (seu email)
   - Clique em **"Salvar e continuar"**
   - Escopos: clique em **"Adicionar ou remover escopos"**, marque:
     - ✅ `../auth/youtube.upload`
     - ✅ `../auth/youtube.force-ssl`
   - Clique em **"Atualizar"** -> **"Salvar e continuar"**
   - Usuários de teste: adicione seu email
   - Clique em **"Salvar e continuar"** -> **"Voltar ao painel"**

4. Volte para **"Credenciais"**
5. Clique em **"Criar credenciais"** -> **"ID do cliente OAuth"**
6. Tipo de aplicativo: **"Aplicativo da área de trabalho"**
7. Nome: "LOFI Bot Desktop"
8. Clique em **"Criar"**

### 4. Baixar Credenciais

1. Depois de criar, clique no ícone de download (⬇️) ao lado das credenciais
2. Isso baixa um arquivo JSON
3. **Renomeie para:** `credentials.json`
4. **Mova para:** `credentials/credentials.json` na pasta do projeto

### 5. Estrutura de Pastas

```
YOUTUBE/
├── credentials/
│   ├── credentials.json  ← Arquivo que você baixou
│   └── token.pickle      ← Gerado automaticamente após primeira autenticação
└── output/               ← Vídeos criados
```

## ✅ Verificar Instalação

```bash
# Testar configuração
python3 youtube_uploader.py
```

Na primeira vez, você será redirecionado para o navegador para autorizar o app.

## 🎯 Uso

Depois de configurado, use o bot normalmente:

```bash
# Com Docker
docker-compose run --rm lofi-generator python3 automated_youtube_bot.py --upload

# Local
python3 automated_youtube_bot.py --upload --duration 3600
```

## 🔒 Segurança

⚠️ **IMPORTANTE**: 
- Nunca faça commit do arquivo `credentials.json` ou `token.pickle`
- Eles já estão no `.gitignore`
- Não compartilhe suas credenciais

## 📝 Upload de Vídeos

Por padrão, os vídeos são enviados como **"unlisted"** (não listados). Para publicar como público:

Edite `automated_youtube_bot.py` linha ~145:

```python
privacy_status="public"  # ao invés de "unlisted"
```

## 🎥 Live Streaming

Para criar lives:

```python
from youtube_uploader import YouTubeUploader

uploader = YouTubeUploader()
broadcast_id, stream_key = uploader.create_live_broadcast(
    title="LOFI Live - Relaxing Music",
    scheduled_start_time=datetime.now() + timedelta(hours=1)
)

print(f"🔗 Live criado! Use este stream_key no OBS: {stream_key}")
```

## 🆘 Troubleshooting

### Erro: "access_denied"
- Verifique se autorizou todos os escopos na tela de consentimento
- Adicione seu email como usuário de teste

### Erro: "invalid_client"
- Verifique se baixou as credenciais corretas
- Confirme se o arquivo está em `credentials/credentials.json`

### Erro: "quota_exceeded"
- Limite padrão: 10,000 unidades/dia
- Upload de vídeo: ~1,600 unidades
- ~6 vídeos/dia de limite
- Para aumentar: https://console.cloud.google.com/apis/api/youtube.googleapis.com/quotas

## 📚 Recursos

- [Documentação YouTube API](https://developers.google.com/youtube/v3)
- [Google Cloud Console](https://console.cloud.google.com/)
- [OAuth 2.0](https://developers.google.com/identity/protocols/oauth2)

