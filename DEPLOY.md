# 🚀 Guia Rápido de Deploy - Railway

## ⚡ Deploy em 5 Passos

### 1. **Preparar o Repositório**
```bash
git add .
git commit -m "Preparando deploy no Railway"
git push origin main
```

### 2. **Acessar o Railway**
- Vá para [railway.app](https://railway.app)
- Faça login com sua conta GitHub/GitLab

### 3. **Criar Novo Projeto**
- Clique em "New Project"
- Selecione "Deploy from GitHub repo"
- Escolha este repositório

### 4. **Configurar Variáveis de Ambiente**
No dashboard do projeto, vá em "Variables" e adicione:

```bash
SEPSIS_API_URL=https://sepsis-sentinel-api.railway.internal
RAILWAY_SERVICE_NAME=sepsis-sentinel-api
PORT=8501
DEBUG=false
LOG_LEVEL=INFO
```

### 5. **Deploy Automático**
- O Railway detectará automaticamente o `Procfile`
- Build e deploy acontecerão automaticamente
- Aguarde a URL ser gerada

## 🔧 Deploy via CLI (Alternativo)

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
./deploy.sh
```

## ✅ Verificação

Após o deploy, verifique:
- [ ] Status "Deployed" no dashboard
- [ ] URL pública funcionando
- [ ] Conectividade com a API externa
- [ ] Logs sem erros

## 🆘 Problemas Comuns

| Problema | Solução |
|----------|---------|
| Build falha | Verificar `requirements.txt` |
| Porta não funciona | Verificar variável `PORT` |
| API não conecta | Verificar `SEPSIS_API_URL` |
| App não inicia | Verificar logs no dashboard |

## 📞 Suporte

- **Railway Docs**: [docs.railway.app](https://docs.railway.app)
- **Issues**: GitHub do projeto
- **Logs**: Dashboard do Railway

---

**🎯 Dica**: Use o dashboard do Railway para monitorar logs em tempo real durante o deploy!
