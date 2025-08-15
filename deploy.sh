#!/bin/bash

# Script de Deploy para o Railway
# Sepsis Sentinel Frontend

echo "🚀 Iniciando deploy do Sepsis Sentinel Frontend no Railway..."

# Verifica se o Railway CLI está instalado
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI não encontrado. Instalando..."
    npm install -g @railway/cli
fi

# Verifica se está logado no Railway
if ! railway whoami &> /dev/null; then
    echo "🔐 Faça login no Railway..."
    railway login
fi

# Lista projetos disponíveis
echo "📋 Projetos disponíveis:"
railway projects

# Solicita seleção do projeto
read -p "🔍 Digite o ID do projeto para deploy: " PROJECT_ID

# Seleciona o projeto
railway link $PROJECT_ID

# Verifica status atual
echo "📊 Status atual do projeto:"
railway status

# Faz deploy
echo "🚀 Iniciando deploy..."
railway up

# Verifica status após deploy
echo "✅ Deploy concluído! Verificando status..."
railway status

echo "🎉 Deploy concluído com sucesso!"
echo "📱 Acesse o dashboard do Railway para ver a URL da aplicação"
echo "🔗 URL: https://railway.app/dashboard"
