# 🩺 Sepsis Sentinel Frontend

Sistema de detecção precoce de sepse com interface web desenvolvida em Streamlit, conectando-se a uma API externa para predições em tempo real.

## 🚀 Visão Geral

O **Sepsis Sentinel** é uma ferramenta de apoio à decisão clínica que utiliza Machine Learning para identificar precocemente pacientes em risco de desenvolver sepse. O sistema analisa dados clínicos como sinais vitais, pressão arterial, dados demográficos e informações hospitalares para gerar predições de risco.

## ✨ Funcionalidades

- **🔍 Predição em Tempo Real**: Interface intuitiva para inserção de dados clínicos
- **📊 Visualização de Resultados**: Apresentação clara do risco com indicadores visuais
- **📈 Histórico de Predições**: Acompanhamento temporal dos resultados
- **🎨 Interface Moderna**: Design responsivo e acessível
- **🔗 Integração com API**: Conecta-se ao endpoint `http://sepsis-sentinel-api-develop.up.railway.app/predict`

## 🏗️ Arquitetura

```
┌─────────────────┐    HTTP/HTTPS    ┌──────────────────┐
│   Frontend      │ ◄──────────────► │   API Externa    │
│   Streamlit     │                  │   Sepsis ML      │
│                 │                  │                  │
└─────────────────┘                  └──────────────────┘
```

## 🛠️ Tecnologias

- **Frontend**: Streamlit 1.28.1
- **Linguagem**: Python 3.11+
- **Visualização**: Plotly, Pandas
- **Deploy**: Railway
- **Containerização**: Docker

## 📋 Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Conta no Railway
- Acesso ao endpoint da API: `sepsis-sentinel-api.railway.internal`

## 🚀 Deploy no Railway

### 1. Preparação do Repositório

Certifique-se de que o repositório contém todos os arquivos necessários:

```
sepsis-sentinel-front-streamlit/
├── frontend/
│   └── app.py
├── config.py
├── requirements.txt
├── Procfile
├── Dockerfile
├── env.example
└── README.md
```

### 2. Configuração no Railway

1. **Acesse o Railway**: [railway.app](https://railway.app)
2. **Crie um novo projeto** ou use um existente
3. **Conecte o repositório** GitHub/GitLab
4. **Configure as variáveis de ambiente**:

```bash
# Variáveis obrigatórias
SEPSIS_API_URL=https://sepsis-sentinel-api-develop.up.railway.app
RAILWAY_SERVICE_NAME=sepsis-sentinel-api
PORT=8501

# Variáveis opcionais
DEBUG=false
LOG_LEVEL=INFO
```

### 3. Deploy Automático

O Railway detectará automaticamente:
- **Procfile** para execução
- **requirements.txt** para dependências Python
- **Dockerfile** para containerização (opcional)

### 4. Verificação do Deploy

Após o deploy, verifique:
- Status da aplicação no dashboard do Railway
- Logs de execução
- URL pública gerada
- Conectividade com a API externa

## 🔧 Desenvolvimento Local

### Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd sepsis-sentinel-front-streamlit

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp env.example .env
# Edite o arquivo .env com suas configurações
```

### Execução Local

```bash
# Execute a aplicação
streamlit run frontend/app.py

# A aplicação estará disponível em: http://localhost:8501
```

## 🔌 Configuração da API

### Endpoint Principal
- **URL**: `https://sepsis-sentinel-api-develop.up.railway.app/predict`
- **Método**: POST
- **Formato**: JSON

### Estrutura dos Dados de Entrada

```json
{
  "hr": 80,                    // Frequência cardíaca (bpm)
  "o2sat": 98,                 // Saturação de oxigênio (%)
  "temp": 37.0,                // Temperatura corporal (°C)
  "sbp": 120,                  // Pressão sistólica (mmHg)
  "dbp": 80,                   // Pressão diastólica (mmHg)
  "map": 93.3,                 // Pressão arterial média (mmHg)
  "resp": 18,                  // Taxa respiratória (rpm)
  "age": 45,                   // Idade (anos)
  "gender": 0,                 // Gênero (0=Feminino, 1=Masculino)
  "unit1": 0,                  // Unidade 1 (0=Não, 1=Sim)
  "unit2": 0,                  // Unidade 2 (0=Não, 1=Sim)
  "hosp_adm_time": 24,         // Tempo de internação (horas)
  "iculos": 48                 // Tempo na UTI (horas)
}
```

### Estrutura da Resposta

```json
{
  "prediction": 0.75,          // Probabilidade de sepse (0.0-1.0)
  "risk_level": "Alto",        // Nível de risco (Baixo/Moderado/Alto)
  "confidence": 0.92           // Confiança da predição
}
```

## 🐳 Deploy com Docker

### Build da Imagem

```bash
docker build -t sepsis-sentinel-frontend .
```

### Execução do Container

```bash
docker run -p 8501:8501 \
  -e SEPSIS_API_URL=https://sepsis-sentinel-api-develop.up.railway.app \
  sepsis-sentinel-frontend
```

## 📊 Monitoramento e Logs

### Logs do Railway

Acesse os logs através do dashboard do Railway:
- **Build logs**: Durante o processo de build
- **Runtime logs**: Durante a execução da aplicação
- **Error logs**: Para debugging de problemas

### Verificação de Saúde da API

O sistema verifica automaticamente a conectividade com a API:
- Endpoint: `/health`
- Frequência: A cada carregamento da página
- Fallback: Mensagem de erro na interface

## 🔒 Segurança

- **HTTPS**: Todas as comunicações são feitas via HTTPS
- **Validação de Dados**: Entrada de dados validada no frontend
- **Rate Limiting**: Implementado pela infraestrutura do Railway
- **Isolamento**: Containerização para isolamento de processos

## 🚨 Troubleshooting

### Problemas Comuns

1. **API não conecta**:
   - Verifique a URL da API nas variáveis de ambiente
   - Confirme se o serviço da API está rodando
   - Verifique logs de conectividade
   - Resetar pipe do Railway

2. **Erro de build**:
   - Verifique versões das dependências no `requirements.txt`
   - Confirme compatibilidade com Python 3.11+

3. **Aplicação não inicia**:
   - Verifique logs de runtime no Railway
   - Confirme configuração da porta (variável `PORT`)

### Logs de Debug

Para ativar logs detalhados, configure:
```bash
DEBUG=true
LOG_LEVEL=DEBUG
```

## 📈 Métricas e Performance

- **Tempo de resposta**: < 2 segundos para predições
- **Disponibilidade**: 99.9% (infraestrutura Railway)
- **Escalabilidade**: Auto-scaling baseado em demanda
- **Monitoramento**: Logs em tempo real

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request



**⚠️ IMPORTANTE**: Este sistema é uma ferramenta de apoio à decisão clínica e **não substitui uma avaliação médica profissional**. Os resultados são preditivos e devem ser interpretados por um profissional de saúde.
