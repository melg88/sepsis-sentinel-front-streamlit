FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copia arquivos de dependências
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia código da aplicação
COPY . .

# Expõe porta padrão do Streamlit
EXPOSE 8501

# Define variáveis de ambiente padrão
ENV STREAMLIT_SERVER_PORT=8501
ENV PORT=8502
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Comando para executar a aplicação
CMD ["streamlit", "run", "frontend/app.py", "--server.port=$PORT", "--server.address=0.0.0.0", "--server.headless=true"]
