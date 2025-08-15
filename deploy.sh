#!/bin/bash


echo "🚀 Iniciando deploy do Sepsis Sentinel Frontend no Railway..."


if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI não encontrado. Instalando..."
    npm install -g @railway/cli
fi


if ! railway whoami &> /dev/null; then
    echo "🔐 Faça login no Railway..."
    railway login
fi


echo "📋 Projetos disponíveis:"
railway projects


read -p "🔍 Digite o ID do projeto para deploy: " PROJECT_ID


railway link $PROJECT_ID


echo "📊 Status atual do projeto:"
railway status


echo "🚀 Iniciando deploy..."
railway up


echo "✅ Deploy concluído! Verificando status..."
railway status

echo "🎉 Deploy concluído com sucesso!"
echo "📱 Acesse o dashboard do Railway para ver a URL da aplicação"
echo "🔗 URL: https://railway.app/dashboard"
