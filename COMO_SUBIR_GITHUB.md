# 📤 Como Subir o Projeto para o GitHub

O projeto já está commitado localmente. Agora você precisa criar um repositório no GitHub e fazer o push.

## 🚀 Opção 1: Usar o Script Automático

Execute o script que criamos:

```bash
./PUSH_TO_GITHUB.sh
```

O script vai te guiar através do processo.

## 📝 Opção 2: Manual

### Passo 1: Criar Repositório no GitHub

1. Acesse: https://github.com/new
2. Nome do repositório: `youtube-lofi-bot` (ou outro nome de sua preferência)
3. **IMPORTANTE:** NÃO marque nenhuma opção:
   - ❌ Não adicione README
   - ❌ Não adicione .gitignore
   - ❌ Não escolha uma license
4. Clique em "Create repository"

### Passo 2: Conectar e Fazer Push

**Se usar HTTPS:**
```bash
git remote add origin https://github.com/SEU_USUARIO/youtube-lofi-bot.git
git branch -M main
git push -u origin main
```

**Se usar SSH:**
```bash
git remote add origin git@github.com:SEU_USUARIO/youtube-lofi-bot.git
git branch -M main
git push -u origin main
```

Substitua `SEU_USUARIO` pelo seu nome de usuário do GitHub.

## ✅ Verificação

Após o push, acesse:
```
https://github.com/SEU_USUARIO/youtube-lofi-bot
```

Você deve ver todos os arquivos do projeto lá!

## 🔒 Segurança

⚠️ **IMPORTANTE:** Os seguintes arquivos NÃO foram commitados (estão no .gitignore):
- `credentials/` - Suas credenciais da API do YouTube
- `*.json` - Arquivos de configuração sensíveis
- `*.pickle` - Tokens de autenticação
- `logs/` - Logs do sistema
- `output/` - Vídeos gerados

Isso é **correto e seguro**! Nunca commite credenciais.

## 🔄 Próximos Commits

Depois do primeiro push, para fazer novos commits:

```bash
git add .
git commit -m "Sua mensagem de commit"
git push
```

---

**Pronto! Seu projeto está no GitHub! 🎉**

