"""
Configurações centralizadas para o Sepsis Sentinel Frontend
"""
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

def get_api_url():
    """
    Retorna a URL base da API de predição de sepse.
    Prioriza variáveis de ambiente, com fallback para configuração padrão.
    """
    # Prioriza variáveis de ambiente
    api_url = os.environ.get("SEPSIS_API_URL")
    
    if api_url:
        return api_url.rstrip('/')
    
    # Fallback para Railway internal endpoint
    railway_service = os.environ.get("RAILWAY_SERVICE_NAME", "sepsis-sentinel-api")
    if railway_service:
        return f"https://{railway_service}.railway.internal"
    
    # Fallback para desenvolvimento local
    return "http://localhost:8000"

def get_api_endpoint():
    """
    Retorna o endpoint completo para predição
    """
    base_url = get_api_url()
    return f"{base_url}/predict"

def get_health_endpoint():
    """
    Retorna o endpoint para verificação de saúde da API
    """
    base_url = get_api_url()
    return f"{base_url}/health"

# Configurações adicionais
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

# Configurações do Streamlit
STREAMLIT_SERVER_PORT =8502
STREAMLIT_SERVER_ADDRESS ="0.0.0.0"
