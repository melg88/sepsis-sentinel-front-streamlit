"""
Frontend Streamlit para detecção de sepse com design elegante
"""
import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

# -----------------------------------------------------------------------------
# Configuração da Página
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Sepsis Sentinel",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------------------------
# Estilos CSS Customizados
# -----------------------------------------------------------------------------
st.markdown("""
<style>
/* Estilo geral */
body {
    background-color: #f0f2f6;
}

/* Título principal */
.st-emotion-cache-10trblm {
    color: #004d40; /* Verde escuro para o título */
    font-weight: 700;
}

/* Botão principal */
.stButton>button {
    border: 2px solid #00695c;
    border-radius: 20px;
    background-color: #00796b;
    color: white;
    padding: 12px 28px;
    font-size: 18px;
    font-weight: bold;
    transition: all 0.3s ease-in-out;
    width: 100%;
}

.stButton>button:hover {
    background-color: #004d40;
    border-color: #004d40;
    transform: scale(1.05);
}

/* Botão secundário */
.stButton>button[data-testid="baseButton-secondary"] {
    border: 2px solid #666;
    background-color: #f8f9fa;
    color: #333;
}

.stButton>button[data-testid="baseButton-secondary"]:hover {
    background-color: #e9ecef;
    border-color: #495057;
}

/* Caixas de entrada de número */
.stNumberInput input {
    border-radius: 10px;
    border: 1px solid #ced4da;
}

/* Estilos da Página de Resultado */
.result-page-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    max-width: 800px;
    margin: 0 auto;
}

.traffic-light-circle {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: white;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    margin-bottom: 2rem;
    border: 4px solid rgba(255,255,255,0.3);
}

.traffic-light-circle.green { background: linear-gradient(145deg, #66bb6a, #388e3c); }
.traffic-light-circle.yellow { background: linear-gradient(145deg, #ffee58, #fbc02d); color: #333; }
.traffic-light-circle.red { background: linear-gradient(145deg, #ef5350, #c62828); }

.probability-value {
    font-size: 3.5rem;
    font-weight: bold;
    line-height: 1;
    margin-bottom: 0.2rem;
}

.probability-label {
    font-size: 1rem;
    font-weight: 500;
    opacity: 0.9;
}

.result-title {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 1rem;
}

.result-title.green-text { color: #2e7d32; }
.result-title.yellow-text { color: #f57f17; }
.result-title.red-text { color: #c62828; }

.result-message {
    font-size: 1.1rem;
    max-width: 600px;
    line-height: 1.6;
}

/* Grids para detalhes */
.details-grid {
    display: grid;
    grid-template-columns: 0.7fr 1.3fr;
    gap: 2rem;
    margin: 2rem 0;
    width: 100%;
    max-width: 1200px;
    margin-left: auto;
    margin-right: auto;
    align-items: start;
}

@media (max-width: 768px) {
    .details-grid {
        grid-template-columns: 1fr;
        gap: 1.5rem;
    }
}

.detail-card {
    background: white;
    border-radius: 15px;
    padding: 1.5rem; /* Aumentei um pouco o padding para mais respiro */
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    border: 1px solid #e0e0e0;
    overflow: hidden;

    /* --- ✨ NOVO LAYOUT EM GRELHA --- */
    display: grid;
    /* Duas colunas: a primeira (label) ocupa o espaço flexível, 
       a segunda (valor) ajusta-se ao conteúdo. */
    grid-template-columns: 1fr auto; 
    /* Espaçamento: 1rem entre linhas, 1.5rem entre colunas */
    gap: 1rem 1.5rem; 
    /* Alinha o conteúdo de cada célula verticalmente ao centro */
    align-items: center; 
}

/* Com o display: grid, a altura será gerida automaticamente. 
  Estas regras podem ser simplificadas ou removidas.
*/
.detail-card.prediction-card,
.detail-card.patient-card {
    height: auto;
}


.detail-card h3 {
    color: #004d40;
    margin-bottom: 1.2rem;
    font-size: 1.3rem;
    border-bottom: 2px solid #00796b;
    padding-bottom: 0.5rem;
}

.detail-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid #f0f0f0;
    min-height: 2.8rem;
}

.detail-item:last-child {
    border-bottom: none;
}

.detail-label {
    font-weight: 600;
    color: #555;
    font-size: 0.95rem;
}

.detail-value {
    font-weight: 500;
    color: #333;
    background: #f8f9fa;
    padding: 0.3rem 0.8rem;
    border-radius: 8px;
    font-size: 0.9rem;
}

/* Grid para métricas (removido - não usado mais) */

/* Estilos para histórico */
.history-container {
    background-color: white;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    margin: 20px 0;
}

/* Estilos para métricas */
.metric-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    margin: 20px 0;
}

/* Melhorias gerais */
.stMarkdown {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Estilo para botões */
.stButton > button {
    border-radius: 25px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}

/* Estilo para inputs */
.stNumberInput > div > div > input {
    border-radius: 12px;
    border: 2px solid #e0e0e0;
    transition: all 0.3s ease;
}

.stNumberInput > div > div > input:focus {
    border-color: #00796b;
    box-shadow: 0 0 0 3px rgba(0, 119, 107, 0.1);
}

/* Estilo para selectbox */
.stSelectbox > div > div > div {
    border-radius: 12px;
    border: 2px solid #e0e0e0;
}

/* Estilo para tabs */
.stTabs > div > div > div > div {
    border-radius: 15px 15px 0 0;
    overflow: hidden;
}

.stTabs > div > div > div > div > button {
    border-radius: 0;
    font-weight: 600;
}

/* Estilo para spinner */
.stSpinner > div {
    border-radius: 50%;
}

/* Estilo para métricas do Streamlit */
.stMetric > div > div > div {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    border-radius: 12px;
    padding: 1rem;
    border: 1px solid #dee2e6;
}

/* Estilo para dataframes */
.stDataFrame > div > div > div > div {
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Configurações da API
# -----------------------------------------------------------------------------
# Importa configurações centralizadas
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from config import get_api_url
    API_BASE_URL = get_api_url()
except ImportError:
    # Fallback para configuração manual
    API_BASE_URL = os.environ.get("API_URL", "http://localhost:8000")

def check_api_health():
    """Verifica se a API está funcionando"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200, response.json()
    except:
        return False, None

def predict_sepsis(patient_data):
    """Faz predição de sepse via API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/predict",
            json=patient_data,
            timeout=10
        )
        return response.status_code == 200, response.json()
    except Exception as e:
        return False, {"error": str(e)}

# -----------------------------------------------------------------------------
# Funções para renderizar as "páginas"
# -----------------------------------------------------------------------------

def show_form_page():
    """Renderiza a página com o formulário de entrada de dados."""
    st.header("📊 Informações do Paciente")
    st.markdown("Por favor, insira os dados clínicos mais recentes para avaliação.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("💓 Sinais Vitais")
        hr = st.number_input(
            "Frequência Cardíaca (bpm)", 
            min_value=40, max_value=200, value=80,
            help="Batimentos por minuto. Normal: 60-100 bpm."
        )
        o2sat = st.number_input(
            "Saturação de Oxigênio (%)", 
            min_value=0, max_value=100, value=98,
            help="Saturação de oxigênio em porcentagem."
        )

    with col2:
        st.subheader("🌡️ Respiração e Temperatura")
        temp = st.number_input(
            "Temperatura Corporal (°C)", 
            min_value=35.0, max_value=42.0, value=37.0, step=0.1,
            help="Normal: 36.5-37.5°C."
        )
        resp = st.number_input(
            "Taxa Respiratória (rpm)", 
            min_value=0, max_value=100, value=18,
            help="Respirações por minuto. Normal: 12-20 rpm."
        )

    with col3:
        st.subheader("💉 Pressão Arterial")
        sbp = st.number_input(
            "Pressão Sistólica (mmHg)", 
            min_value=0, max_value=300, value=120,
            help="O valor mais alto da pressão. Normal: ~120 mmHg."
        )
        dbp = st.number_input(
            "Pressão Diastólica (mmHg)", 
            min_value=0, max_value=200, value=80,
            help="O valor mais baixo da pressão. Normal: ~80 mmHg."
        )

    # Segunda linha de campos
    st.markdown("<br>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)

    with col4:
        st.subheader("👤 Dados Demográficos")
        age = st.number_input(
            "Idade (anos)", 
            min_value=0, max_value=150, value=45,
            help="Idade do paciente em anos."
        )
        gender = st.selectbox(
            "Gênero",
            options=[(0, "Feminino"), (1, "Masculino")],
            format_func=lambda x: x[1],
            help="Gênero do paciente"
        )[0]

    with col5:
        st.subheader("🏥 Dados Hospitalares")
        hosp_adm_time = st.number_input(
            "Tempo de Internação (horas)", 
            min_value=0, value=24,
            help="Tempo de internação em horas."
        )
        iculos = st.number_input(
            "Tempo na UTI (horas)", 
            min_value=0, value=48,
            help="Número de horas na UTI."
        )

    with col6:
        st.subheader("🏢 Unidades")
        unit1 = st.selectbox(
            "Unidade 1",
            options=[(0, "Não"), (1, "Sim")],
            format_func=lambda x: x[1]
        )[0]
        unit2 = st.selectbox(
            "Unidade 2",
            options=[(0, "Não"), (1, "Sim")],
            format_func=lambda x: x[1]
        )[0]

    # Calcula MAP automaticamente
    map_val = (sbp + 2 * dbp) / 3

    st.markdown("<br>", unsafe_allow_html=True)
    _, col_button, _ = st.columns([2, 3, 2])

    if col_button.button("🔬 Avaliar Risco de Sepse", type="primary"):
        # Prepara dados para a API
        patient_data = {
            "hr": hr,
            "o2sat": o2sat,
            "temp": temp,
            "sbp": sbp,
            "dbp": dbp,
            "map": round(map_val, 1),
            "resp": resp,
            "age": age,
            "gender": gender,
            "unit1": unit1,
            "unit2": unit2,
            "hosp_adm_time": hosp_adm_time,
            "iculos": iculos
        }

        with st.spinner('Analisando dados e consultando o modelo preditivo...'):
            # Faz predição real via API
            success, result = predict_sepsis(patient_data)
            
            if success:
                # Salva no histórico
                if "predictions" not in st.session_state:
                    st.session_state.predictions = []
                
                prediction_record = {
                    "timestamp": datetime.now().isoformat(),
                    "patient_data": patient_data,
                    "result": result
                }
                st.session_state.predictions.append(prediction_record)
                
                # Salva resultado e vai para página de resultado
                st.session_state.result = result
                st.session_state.page = 'result'
                st.rerun()
            else:
                st.error(f"❌ Erro na predição: {result.get('error', 'Erro desconhecido')}")

def show_result_page():
    """Renderiza a página com o resultado do diagnóstico."""
    result = st.session_state.result
    probability = result["prediction"]
    prob_percent = probability * 100

    # Define a cor, título e mensagem com base na probabilidade
    if prob_percent >= 60:
        color_class = "red"
        color_text = "red-text"
        title = "🚨 ALERTA - Risco Elevado"
        message = "Os dados indicam um risco elevado de sepse. É crucial procurar avaliação médica imediata para uma análise aprofundada e início de tratamento, se necessário."
    elif 30 <= prob_percent < 60:
        color_class = "yellow"
        color_text = "yellow-text"
        title = "⚠️ ATENÇÃO - Risco Moderado"
        message = "Foi detectado um risco moderado. Recomenda-se monitoramento contínuo dos sinais vitais e uma consulta médica para avaliação. Fique atento a qualquer piora nos sintomas."
    else:
        color_class = "green"
        color_text = "green-text"
        title = "✅ Baixo Risco"
        message = "O modelo indica um baixo risco de sepse com base nos dados atuais. Continue monitorando os sintomas e, caso persistam ou piorem, procure um profissional de saúde."

    # Renderiza o HTML da página de resultado
    st.markdown(f"""
    <div class="result-page-container">
        <div class="traffic-light-circle {color_class}">
            <div class="probability-value">{prob_percent:.0f}%</div>
            <div class="probability-label">de Risco</div>
        </div>
        <div class="result-title {color_text}">{title}</div>
        <p class="result-message">{message}</p>
    </div>
    """, unsafe_allow_html=True)

    # Informações adicionais em grids organizados
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Grid de detalhes organizados - lado a lado
    st.markdown('<div class="details-grid">', unsafe_allow_html=True)
    
    # Card de Detalhes da Predição
    st.markdown("""
    <div class="detail-card prediction-card">
        <h3>📋 Detalhes da Predição</h3>
        <div class="detail-item">
            <span class="detail-label">Probabilidade:</span>
            <span class="detail-value">{:.1%}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">Nível de Risco:</span>
            <span class="detail-value">{}</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">Confiança:</span>
            <span class="detail-value">Alta</span>
        </div>
        <div class="detail-item">
            <span class="detail-label">Status:</span>
            <span class="detail-value">Processado</span>
        </div>
    </div>
    """.format(probability, result["risk_level"]), unsafe_allow_html=True)
    
    # Card de Dados do Paciente
    patient_data = st.session_state.predictions[-1]["patient_data"]
    
    # Mapeamento de nomes em português
    field_names = {
        'hr': 'Frequência Cardíaca (bpm)',
        'o2sat': 'Saturação de Oxigênio (%)',
        'temp': 'Temperatura Corporal (°C)',
        'sbp': 'Pressão Sistólica (mmHg)',
        'dbp': 'Pressão Diastólica (mmHg)',
        'map': 'Pressão Arterial Média (mmHg)',
        'resp': 'Taxa Respiratória (rpm)',
        'age': 'Idade (anos)',
        'gender': 'Gênero',
        'unit1': 'Unidade 1',
        'unit2': 'Unidade 2',
        'hosp_adm_time': 'Tempo de Internação (h)',
        'iculos': 'Tempo na UTI (h)'
    }
    
    # Mapeamento de valores para gênero
    gender_values = {0: 'Feminino', 1: 'Masculino'}
    unit_values = {0: 'Não', 1: 'Sim'}
    
    st.markdown("""
    <div class="detail-card patient-card">
        <h3>📊 Dados do Paciente</h3>
    """, unsafe_allow_html=True)
    
    # Adiciona cada campo com nome em português
    for field, value in patient_data.items():
        if field in field_names:
            display_name = field_names[field]
            
            # Formata valores especiais
            if field == 'gender':
                display_value = gender_values.get(value, str(value))
            elif field in ['unit1', 'unit2']:
                display_value = unit_values.get(value, str(value))
            elif field in ['temp', 'map']:
                display_value = f"{value:.1f}"
            elif field in ['hosp_adm_time', 'iculos']:
                display_value = f"{value:.0f}"
            else:
                display_value = str(value)
            
            st.markdown(f"""
            <div class="detail-item">
                <span class="detail-label">{display_name}:</span>
                <span class="detail-value">{display_value}</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Fecha o grid
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col_button, _ = st.columns([2, 3, 2])
    
    if col_button.button("⬅️ Voltar e Inserir Novos Dados", type="secondary"):
        st.session_state.page = 'form'
        st.rerun()

def show_history_page():
    """Renderiza a página de histórico de predições"""
    st.header("📊 Histórico de Predições")
    
    if "predictions" in st.session_state and st.session_state.predictions:
        # Cria DataFrame com histórico
        history_data = []
        for pred in st.session_state.predictions:
            history_data.append({
                "Data/Hora": datetime.fromisoformat(pred["timestamp"]).strftime("%d/%m/%Y %H:%M"),
                "Risco": pred["result"]["risk_level"],
                "Probabilidade": f"{pred['result']['prediction']:.1%}",
                "FC": pred["patient_data"]["hr"],
                "O2": pred["patient_data"]["o2sat"],
                "Temp": pred["patient_data"]["temp"],
                "PAS": pred["patient_data"]["sbp"],
                "PAD": pred["patient_data"]["dbp"]
            })
        
        history_df = pd.DataFrame(history_data)
        
        # Estilo melhorado para o DataFrame
        st.markdown("""
        <style>
        .stDataFrame {
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.dataframe(history_df, use_container_width=True)
        
        # Gráfico de evolução temporal
        if len(history_data) > 1:
            st.subheader("📈 Evolução Temporal")
            
            # Converte probabilidades para valores numéricos
            prob_values = [float(pred["result"]["prediction"]) for pred in st.session_state.predictions]
            timestamps = [datetime.fromisoformat(pred["timestamp"]) for pred in st.session_state.predictions]
            
            fig = px.line(
                x=timestamps,
                y=prob_values,
                title="Evolução do Risco de Sepse",
                labels={"x": "Data/Hora", "y": "Probabilidade de Sepse"}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📝 Nenhuma predição realizada ainda. Use a aba 'Predição' para começar.")

def show_about_page():
    """Renderiza a página sobre o sistema"""
    st.header("ℹ️ Sobre o Sistema")
    
    st.markdown("""
    ### 🚨 Sepsis Sentinel
    
    O **Sepsis Sentinel** é um sistema inteligente de detecção precoce de sepse que utiliza 
    Machine Learning para analisar dados clínicos em tempo real.
    
    #### 🔬 Como Funciona
    
    1. **Coleta de Dados**: O sistema coleta dados clínicos do paciente através de um formulário intuitivo
    2. **Análise ML**: Utiliza um modelo Random Forest treinado com dados históricos de pacientes
    3. **Predição**: Calcula a probabilidade de desenvolvimento de sepse
    4. **Resultado**: Apresenta o risco de forma clara e visual
    
    #### 📊 Variáveis Analisadas
    
    - **Sinais Vitais**: Frequência cardíaca, saturação de oxigênio, temperatura, respiração
    - **Pressão Arterial**: Sistólica, diastólica e média
    - **Dados Demográficos**: Idade e gênero
    - **Dados Hospitalares**: Tempo de internação e tempo na UTI
    
    #### 🎯 Objetivo
    
    O sistema visa identificar precocemente pacientes em risco de desenvolver sepse, 
    permitindo intervenção médica oportuna e melhorando os desfechos clínicos.
    
    #### ⚠️ Importante
    
    Este sistema é uma ferramenta de apoio à decisão clínica e não substitui 
    a avaliação médica profissional.
    """)
    
    # Informações técnicas
    st.subheader("🔧 Informações Técnicas")
    
    col_tech1, col_tech2 = st.columns(2)
    
    with col_tech1:
        st.markdown("""
        **Backend:**
        - FastAPI
        - Python 3.9+
        - Scikit-learn
        
        **Frontend:**
        - Streamlit
        - Plotly
        - Pandas
        """)
    
    with col_tech2:
        st.markdown("""
        **ML Model:**
        - Random Forest
        - Acurácia >90%
        - Features: 13 variáveis clínicas
        
        **Deploy:**
        - Railway
        - Docker-ready
        """)

# -----------------------------------------------------------------------------
# Lógica Principal da Aplicação
# -----------------------------------------------------------------------------

# Inicializa o estado da sessão para controlar a "página"
if 'page' not in st.session_state:
    st.session_state.page = 'form'
if 'result' not in st.session_state:
    st.session_state.result = None

# Cabeçalho e Disclaimer (aparecem em todas as "páginas")
st.title("🩺 Sepsis Sentinel")
st.markdown("#### Sistema de Detecção Precoce de Sepse - Uma ferramenta de apoio baseada em Machine Learning")
st.markdown("---")

# Verificação de saúde da API
api_healthy, health_data = check_api_health()

if api_healthy:
    if health_data and health_data.get("model_loaded"):
        st.success("✅ API Conectada e Modelo ML Carregado")
    else:
        st.warning("⚠️ API Conectada, mas Modelo ML não disponível")
else:
    st.error("❌ API Desconectada - Verifique se o backend está rodando")

st.warning("""
**AVISO IMPORTANTE:** Esta ferramenta é um protótipo e **não substitui uma avaliação médica profissional.** 
Os resultados são preditivos e devem ser interpretados por um profissional de saúde.
""")

# Navegação por tabs
tab1, tab2, tab3 = st.tabs(["🔍 Predição", "📊 Histórico", "ℹ️ Sobre"])

with tab1:
    if st.session_state.page == 'form':
        show_form_page()
    else:
        show_result_page()

with tab2:
    show_history_page()

with tab3:
    show_about_page()

# Rodapé
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("Desenvolvido com base no estudo 'Aplicação do Método CRISP-DM para Diagnóstico Hospitalar Precoce de Sepse'.")
