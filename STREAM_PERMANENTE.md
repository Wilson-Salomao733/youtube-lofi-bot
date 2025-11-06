# ♻️ Stream Permanente - Mesmo Stream Key para Todas as Lives

## ✅ Solução Implementada

Agora o sistema usa um **stream permanente** que é reutilizado para **TODAS as lives**. Isso significa:

- ✅ **Mesmo stream_key** para todas as lives
- ✅ **Não precisa criar novo stream** a cada live
- ✅ **Stream_key salvo** em `credentials/stream_config.json`
- ✅ **Reutilização automática** - o sistema verifica se já existe e usa

## 🔧 Como Funciona

1. **Primeira vez**: Cria um stream permanente e salva o stream_key
2. **Próximas vezes**: Reutiliza o mesmo stream_key salvo
3. **Todas as lives**: Usam o mesmo stream_key

## 📋 Arquivo de Configuração

O stream permanente é salvo em:
```
credentials/stream_config.json
```

Formato:
```json
{
  "stream_id": "SEU_STREAM_ID",
  "stream_key": "SEU_STREAM_KEY",
  "rtmp_url": "rtmp://a.rtmp.youtube.com/live2",
  "created_at": "2025-11-06T12:00:00"
}
```

## 🛠️ Criar Stream Permanente Manualmente

Se quiser criar o stream permanente manualmente antes de criar lives:

```bash
# Dentro do container
docker exec lofi-live-bot python criar_stream_permanente.py

# Ou localmente
python3 criar_stream_permanente.py
```

## 🔑 Configurar Stream Key Manualmente

Se o stream_key não foi obtido automaticamente, você pode configurá-lo manualmente:

1. **Obtenha o stream_key** do YouTube Studio:
   - Acesse: https://studio.youtube.com/
   - Vá em: Conteúdo → Transmissões
   - Encontre o stream permanente criado
   - Copie o Stream Key

2. **Crie/edite o arquivo** `credentials/stream_config.json`:
```json
{
  "stream_id": "SEU_STREAM_ID",
  "stream_key": "exxa-sfyy-sy27-hvm3-58sb",
  "rtmp_url": "rtmp://a.rtmp.youtube.com/live2"
}
```

3. **Use uma das 3 keys que você já tem**:
   - `exxa-sfyy-sy27-hvm3-58sb`
   - `45ud-7dwd-dqfe-urcc-er5f`
   - `j2ej-v13s-tbbz-zy7w-e7wk`

   **Escolha UMA e use para todas as lives!**

## ⚙️ Como o Sistema Funciona Agora

1. **Ao criar uma live**:
   - Verifica se existe `credentials/stream_config.json`
   - Se existe, usa o stream_key salvo
   - Se não existe, cria um novo stream permanente
   - Salva o stream_key no arquivo

2. **Todas as lives criadas**:
   - Usam o **mesmo stream_key**
   - Não criam novos streams
   - Reutilizam o stream permanente

## 🎯 Vantagens

- ✅ **Mesmo stream_key** para todas as lives
- ✅ **Não precisa configurar manualmente** a cada live
- ✅ **Stream_key persistente** - salvo no arquivo
- ✅ **Funciona automaticamente** - sem intervenção manual

## 📝 Notas Importantes

- O stream_key **não muda** a menos que você delete o stream permanente
- Se você deletar o stream permanente no YouTube, precisará criar um novo
- O arquivo `stream_config.json` é criado automaticamente na primeira execução
- O stream_key pode levar alguns minutos para ficar disponível após criar o stream

## 🔄 Resetar Stream Permanente

Se quiser criar um novo stream permanente (novo stream_key):

```bash
# Delete o arquivo de configuração
rm credentials/stream_config.json

# Na próxima execução, um novo stream será criado
```

