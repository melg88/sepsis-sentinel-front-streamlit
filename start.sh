#!/bin/bash

# Script de inicialização para o Railway
# Sepsis Sentinel Frontend

echo "🚀 Iniciando Sepsis Sentinel Frontend..."

# Define porta padrão se não estiver definida
#export PORT=${PORT:-8502}
export PORT=8502

echo "📡 Porta configurada: $PORT"

# Verifica se o diretório frontend existe
if [ ! -d "frontend" ]; then
    echo "❌ Diretório frontend não encontrado!"
    exit 1
fi

# Verifica se o arquivo app.py existe
if [ ! -f "frontend/app.py" ]; then
    echo "❌ Arquivo frontend/app.py não encontrado!"
    exit 1
fi

echo "✅ Arquivos verificados com sucesso"

# Inicia a aplicação Streamlit
echo "🌐 Iniciando Streamlit na porta $PORT..."
exec streamlit run frontend/app.py \
    --server.port = 8502\
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.enableCORS=false \
    --server.enableXsrfProtection=false
