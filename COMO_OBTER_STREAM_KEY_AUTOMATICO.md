# 🔑 Como Obter Stream Key Automaticamente

## ✅ Solução Implementada

O sistema agora tenta obter o `stream_key` **automaticamente** de várias formas:

### 1. **Uso do Stream Permanente Salvo**
- Se você já tem um `stream_key` salvo em `credentials/stream_config.json`, ele será usado **automaticamente**
- Não precisa obter manualmente toda vez!

### 2. **Tentativas Automáticas Após Criar Stream**
- Quando um novo stream é criado, o sistema tenta obter o `stream_key` **até 15 vezes** (5 minutos)
- Aguarda 20 segundos entre cada tentativa
- Atualiza automaticamente o arquivo de configuração quando obtém

### 3. **Tentativas Após Vincular Broadcast**
- Após vincular o broadcast ao stream, tenta obter o `stream_key` **até 20 vezes** (5 minutos)
- Aguarda 15 segundos entre cada tentativa
- Atualiza automaticamente o arquivo de configuração

### 4. **Script Manual de Obtenção**
Se mesmo assim o `stream_key` não for obtido automaticamente, você pode usar:

```bash
# Dentro do container
docker exec -it lofi-live-bot python obter_stream_key_automatico.py

# Ou localmente
python3 obter_stream_key_automatico.py
```

Este script tenta **até 30 vezes** (10 minutos) para obter o `stream_key`.

## 📋 Como Funciona

### Primeira Vez (Criar Stream Permanente)

1. Sistema cria um stream permanente
2. Tenta obter `stream_key` automaticamente (até 5 minutos)
3. Se conseguir, salva em `credentials/stream_config.json`
4. Se não conseguir, você pode:
   - Aguardar alguns minutos e tentar novamente
   - Usar o script `obter_stream_key_automatico.py`
   - Obter manualmente no YouTube Studio e salvar no arquivo

### Próximas Vezes (Reutilizar Stream)

1. Sistema carrega `stream_key` do arquivo `credentials/stream_config.json`
2. **Usa automaticamente** - não precisa obter manualmente!
3. Se a API não retornar o `stream_key`, usa o que está salvo no arquivo

## 🔧 Configuração Manual (Se Necessário)

Se mesmo assim precisar configurar manualmente:

1. **Obtenha o stream_key** do YouTube Studio:
   - Acesse: https://studio.youtube.com/
   - Vá em: Conteúdo → Transmissões
   - Encontre o stream permanente
   - Copie o Stream Key

2. **Edite o arquivo** `credentials/stream_config.json`:
```json
{
  "stream_id": "SEU_STREAM_ID",
  "stream_key": "exxa-sfyy-sy27-hvm3-58sb",
  "rtmp_url": "rtmp://a.rtmp.youtube.com/live2"
}
```

3. **Pronto!** O sistema usará esse `stream_key` automaticamente para todas as lives

## ⚙️ Melhorias Implementadas

- ✅ **15 tentativas** ao criar stream (antes: 5)
- ✅ **20 segundos** entre tentativas (antes: 10)
- ✅ **20 tentativas** após vincular broadcast (novo!)
- ✅ **Usa stream_key salvo** mesmo se API não retornar
- ✅ **Atualiza automaticamente** o arquivo quando obtém

## 💡 Dicas

- O YouTube pode levar **até 10 minutos** para disponibilizar o `stream_key` após criar o stream
- Se o `stream_key` já está salvo no arquivo, o sistema usa ele **imediatamente**
- Uma vez configurado, você **não precisa mais** obter manualmente!

## 🎯 Resultado

**Agora o sistema tenta obter o stream_key automaticamente de forma muito mais agressiva!**

- ✅ Até **5 minutos** ao criar stream
- ✅ Até **5 minutos** após vincular broadcast
- ✅ Total: até **10 minutos** de tentativas automáticas
- ✅ Usa `stream_key` salvo se API não retornar

**Você só precisa configurar manualmente UMA VEZ, depois o sistema usa automaticamente!**

