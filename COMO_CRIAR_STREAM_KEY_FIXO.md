# 🔑 Como Criar e Configurar Stream Key Fixo

## ✅ Use RTMP (Recomendado)

**Escolha RTMP** ao criar a chave de transmissão porque:
- ✅ É o padrão do YouTube
- ✅ Funciona perfeitamente com ffmpeg
- ✅ Menor latência
- ✅ Mais estável para streams longos (até 19h)
- ✅ Suportado nativamente pelo sistema

## 📋 Passo a Passo

### 1. Criar Chave de Transmissão no YouTube Studio

1. Acesse: https://studio.youtube.com/
2. Vá em: **Conteúdo → Transmissões**
3. Clique em: **Criar nova chave de transmissão**
4. Preencha:
   - **Nome**: `LOFI Live - Stream Permanente` (ou qualquer nome)
   - **Protocolo**: **RTMP** (padrão) ✅
   - **Resolução**: Deixe automático ou escolha 1080p
5. Clique em: **Criar**

### 2. Copiar Informações

Após criar, você verá:
- **Stream Key**: `exxa-sfyy-sy27-hvm3-58sb` (exemplo)
- **RTMP URL**: `rtmp://a.rtmp.youtube.com/live2`
- **Stream ID**: Aparece na URL ou nos detalhes

### 3. Configurar no Sistema

Execute o script de configuração:

```bash
# Dentro do container
docker exec -it lofi-live-bot python configurar_stream_key_fixo.py

# Ou localmente
python3 configurar_stream_key_fixo.py
```

O script vai:
1. Mostrar suas 3 keys
2. Você escolhe qual usar (1, 2 ou 3)
3. Pede o Stream ID (ou usa o atual)
4. Salva tudo em `credentials/stream_config.json`

### 4. Pronto!

Agora o sistema usará essa key fixa para **TODAS as lives** automaticamente!

## 🎯 Suas 3 Keys Fixas

Você tem estas 3 keys que podem ser usadas:

1. **exxa-sfyy-sy27-hvm3-58sb**
2. **45ud-7dwd-dqfe-urcc-er5f**
3. **j2ej-v13s-tbbz-zy7w-e7wk**

**Escolha UMA e use para sempre!**

## ⚙️ Configuração Manual (Alternativa)

Se preferir configurar manualmente, edite o arquivo:

```bash
nano credentials/stream_config.json
```

E coloque:

```json
{
  "stream_id": "SEU_STREAM_ID_AQUI",
  "stream_key": "exxa-sfyy-sy27-hvm3-58sb",
  "rtmp_url": "rtmp://a.rtmp.youtube.com/live2",
  "is_fixed_key": true
}
```

## ✅ Vantagens do Stream Key Fixo

- ✅ **Mesma key para todas as lives** - não precisa criar nova toda vez
- ✅ **Funciona imediatamente** - não precisa esperar API
- ✅ **Mais confiável** - não depende da API do YouTube
- ✅ **Configuração única** - configure uma vez e esqueça!

## 🔄 Como o Sistema Usa

1. Sistema carrega `stream_key` do arquivo `credentials/stream_config.json`
2. **Usa automaticamente** para criar a live
3. Não precisa esperar API retornar o key
4. Funciona imediatamente!

## 💡 Dica

**Use a mesma key fixa para sempre!** Não precisa criar nova chave a cada live. Uma vez configurada, o sistema usa automaticamente.

