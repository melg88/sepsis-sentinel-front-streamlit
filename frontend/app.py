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


st.set_page_config(
    page_title="Sepsis Sentinel",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
}

.traffic-light-circle {
    width: 250px;
    height: 250px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: white;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    margin-bottom: 2rem;
}

.traffic-light-circle.green { background: linear-gradient(145deg, #66bb6a, #388e3c); }
.traffic-light-circle.yellow { background: linear-gradient(145deg, #ffee58, #fbc02d); color: #333; }
.traffic-light-circle.red { background: linear-gradient(145deg, #ef5350, #c62828); }

.probability-value {
    font-size: 5rem;
    font-weight: bold;
    line-height: 1;
}

.probability-label {
    font-size: 1.2rem;
    font-weight: 500;
}

.result-title {
    font-size: 2.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
}

.result-title.green-text { color: #2e7d32; }
.result-title.yellow-text { color: #f57f17; }
.result-title.red-text { color: #c62828; }

.result-message {
    font-size: 1.2rem;
    max-width: 600px;
}

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

    # Informações adicionais
    st.markdown("<br>", unsafe_allow_html=True)

    col_info1, col_info2 = st.columns(2)

    with col_info1:
        st.subheader("📋 Detalhes da Predição")
         
        # Cria DataFrame com detalhes da predição na vertical
        prediction_data = [
            {'Campo': 'Probabilidade', 'Valor': f"{probability:.1%}"},
            {'Campo': 'Nível de Risco', 'Valor': result["risk_level"]},
            {'Campo': 'Confiança', 'Valor': 'Alta'},
            {'Campo': 'Status', 'Valor': 'Processado'}
        ]
         
        # Cria DataFrame final na vertical
        prediction_df = pd.DataFrame(prediction_data)
         
        # Exibe a tabela na vertical sem índices
        st.dataframe(prediction_df, use_container_width=True, hide_index=True)
        
    with col_info2:
        st.subheader("📊 Dados do Paciente")
         
        # Dados do paciente
        patient_data = st.session_state.predictions[-1]["patient_data"]
         
        # Mapeamento de nomes amigáveis em português
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
         
        # Mapeamento de valores para gênero e unidades
        gender_values = {0: 'Feminino', 1: 'Masculino'}
        unit_values = {0: 'Não', 1: 'Sim'}
         
        # Cria DataFrame com nomes amigáveis na vertical
        display_data = []
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
                 
                display_data.append({
                    'Campo': display_name,
                    'Valor': display_value
                })
         
        # Cria DataFrame final na vertical
        patient_df = pd.DataFrame(display_data)
         
        # Exibe a tabela na vertical sem índices
        st.dataframe(patient_df, use_container_width=True, hide_index=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col_button, _ = st.columns([2, 3, 2])

    if col_button.button("⬅️ Voltar e Inserir Novos Dados", type="secondary"):
        st.session_state.page = 'form'
        st.rerun()

def show_history_page():
    """Renderiza a página de histórico de predições"""
    st.header("📊 Histórico de Predições")

    if "predictions" in st.session_state and st.session_state.predictions:
        # Resumo executivo no topo
        st.subheader("📋 Resumo Executivo")
        
        # Calcula estatísticas gerais
        total_predictions = len(st.session_state.predictions)
        high_risk_count = sum(1 for pred in st.session_state.predictions 
                             if pred["result"]["prediction"] >= 0.6)
        moderate_risk_count = sum(1 for pred in st.session_state.predictions 
                                 if 0.3 <= pred["result"]["prediction"] < 0.6)
        low_risk_count = sum(1 for pred in st.session_state.predictions 
                            if pred["result"]["prediction"] < 0.3)
        
        # Exibe métricas em colunas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Predições", total_predictions)
        
        with col2:
            st.metric("Alto Risco", high_risk_count, delta=f"{high_risk_count/total_predictions*100:.1f}%")
        
        with col3:
            st.metric("Risco Moderado", moderate_risk_count, delta=f"{moderate_risk_count/total_predictions*100:.1f}%")
        
        with col4:
            st.metric("Baixo Risco", low_risk_count, delta=f"{low_risk_count/total_predictions*100:.1f}%")
        
        st.markdown("---")
        
        # Tabela de histórico organizada verticalmente
        st.subheader("📊 Detalhamento das Predições")
        
        # Cria DataFrame organizado verticalmente
        if st.session_state.predictions:
            # Define as métricas que serão exibidas
            metrics = [
                'Data/Hora',
                'Probabilidade',
                'Nível de Risco',
                'Freq. Cardíaca',
                'Saturação O2',
                'Temperatura',
                'Pressão Sistólica'
            ]
            
            # Cria dados para tabela vertical
            vertical_data = {}
            for i, pred in enumerate(st.session_state.predictions):
                pred_date = datetime.fromisoformat(pred["timestamp"])
                col_name = f"Predição {i + 1}"
                
                vertical_data[col_name] = [
                    pred_date.strftime("%d/%m/%Y %H:%M"),
                    f"{pred['result']['prediction']:.1%}",
                    pred["result"]["risk_level"],
                    f"{pred['patient_data']['hr']} bpm",
                    f"{pred['patient_data']['o2sat']}%",
                    f"{pred['patient_data']['temp']:.1f}°C",
                    f"{pred['patient_data']['sbp']} mmHg"
                ]
            
            # Cria DataFrame vertical
            vertical_df = pd.DataFrame(vertical_data, index=metrics)
            
                         # Exibe a tabela vertical
            st.dataframe(
                vertical_df,
                use_container_width=True,
                height=500,  # Aumentado de 400 para 500
                column_config={
                    col: st.column_config.TextColumn(col, width="medium") 
                    for col in vertical_data.keys()
                }
            )
        
        st.markdown("---")

        # Gráfico de evolução temporal das predições
        st.subheader(f"📈 Evolução das Predições ao Longo do Tempo ({len(st.session_state.predictions)} predições)")
        
        if st.session_state.predictions:
            
            # Prepara dados para o gráfico
            pred_dates = []
            pred_probabilities = []
            pred_risks = []
            
            for pred in st.session_state.predictions:
                # Converte timestamp para datetime
                pred_date = datetime.fromisoformat(pred["timestamp"])
                pred_dates.append(pred_date)
                 
                # Extrai probabilidade (mantém como decimal 0-1)
                prob = pred["result"]["prediction"]
                pred_probabilities.append(prob)  # Mantém como decimal
                
                # Mapeia nível de risco para cores - lógica mais robusta
                risk_level = pred["result"]["risk_level"]
                
                # Primeiro tenta mapear baseado na probabilidade (mais confiável)
                if prob >= 0.6:
                    pred_risks.append("Alto")
                elif prob >= 0.3:
                    pred_risks.append("Moderado")
                else:
                    pred_risks.append("Baixo")
                
                # Se risk_level for string, tenta usar ele também para validação
                if isinstance(risk_level, str):
                    risk_text = risk_level.lower()
                    if any(word in risk_text for word in ["alto", "elevado", "high", "severe"]):
                        # Se o texto indica alto risco mas a probabilidade é baixa, pode ser um erro
                        if prob < 0.3:
                            st.warning(f"⚠️ Inconsistência detectada: Probabilidade {prob:.1%} mas nível de risco '{risk_level}'")
                        pred_risks[-1] = "Alto"  # Força o nível alto
                    elif any(word in risk_text for word in ["moderado", "moderate", "médio", "medium"]):
                        if prob < 0.2 or prob > 0.7:
                            st.warning(f"⚠️ Inconsistência detectada: Probabilidade {prob:.1%} mas nível de risco '{risk_level}'")
                        pred_risks[-1] = "Moderado"
                    elif any(word in risk_text for word in ["baixo", "low", "baixo risco"]):
                        if prob > 0.5:
                            st.warning(f"⚠️ Inconsistência detectada: Probabilidade {prob:.1%} mas nível de risco '{risk_level}'")
                        pred_risks[-1] = "Baixo"
            
                         # Cria DataFrame para o gráfico
            chart_data = pd.DataFrame({
                'Data/Hora': pred_dates,
                'Probabilidade': pred_probabilities,
                'Nível de Risco': pred_risks
            })
            
                         # Gráfico de linha com pontos
            fig = px.line(
                chart_data,
                x='Data/Hora',
                y='Probabilidade',
                title="Evolução da Probabilidade de Sepse ao Longo do Tempo",
                labels={
                    "Data/Hora": "Data e Hora da Predição",
                    "Probabilidade": "Probabilidade de Sepse (0-1)"
                },
                markers=True,  # Adiciona pontos nos dados
                line_shape='linear'
            )
            
                         # Adiciona pontos coloridos por nível de risco
            fig.add_scatter(
                x=chart_data['Data/Hora'],
                y=chart_data['Probabilidade'],
                mode='markers',
                marker=dict(
                    size=10,
                    color=[{'Alto': '#ef5350', 'Moderado': '#fbc02d', 'Baixo': '#66bb6a'}[risk] for risk in pred_risks]
                ),
                name='Nível de Risco',
                showlegend=True
            )
            
            # Configurações do gráfico com escala ajustada
             # Se todos os valores forem 0, ajusta a escala para mostrar melhor os dados
            min_prob = min(pred_probabilities) if pred_probabilities else 0
            max_prob = max(pred_probabilities) if pred_probabilities else 1
             
             # Ajusta a escala do eixo Y baseado nos dados reais (0-1)
             # Sempre inclui espaço para as linhas de referência importantes
            if min_prob == 0 and max_prob == 0:
                y_range = [0, 0.1]  # Escala de 0 a 0.1 para valores muito baixos
            elif max_prob < 0.1:
                y_range = [0, max(0.1, max_prob * 1.2)]  # Escala proporcional para valores baixos
            elif max_prob < 0.3:
                y_range = [0, 0.4]  # Escala que inclui risco moderado
            elif max_prob < 0.6:
                y_range = [0, 0.7]  # Escala que inclui risco alto
            else:
                y_range = [0, 1]  # Escala padrão de 0 a 1
            
                fig.update_layout(
                height=500,
                xaxis_title="Data e Hora da Predição",
                yaxis_title="Probabilidade de Sepse (0-1)",
                yaxis=dict(range=y_range),
                hovermode='x unified',
                showlegend=True
            )
            
            # Adiciona linhas de referência para níveis de risco
            # Linha de risco moderado (sempre visível se a escala permitir)
            if y_range[1] >= 0.3:
                fig.add_hline(y=0.3, line_dash="dash", line_color="orange", 
                             annotation_text="Risco Moderado (≥0.3)", annotation_position="top right")
            elif y_range[1] >= 0.2:  # Se a escala for menor, mostra em posição ajustada
                fig.add_hline(y=0.3, line_dash="dash", line_color="orange", 
                             annotation_text="Risco Moderado (≥0.3)", annotation_position="top right")
            
            # Linha de risco alto (sempre visível se a escala permitir)
            if y_range[1] >= 0.6:
                fig.add_hline(y=0.6, line_dash="dash", line_color="red", 
                             annotation_text="Risco Alto (≥0.6)", annotation_position="top right")
            elif y_range[1] >= 0.4:  # Se a escala for menor, mostra em posição ajustada
                fig.add_hline(y=0.6, line_dash="dash", line_color="red", 
                             annotation_text="Risco Alto (≥0.6)", annotation_position="top right")
            
            # Linha de risco baixo (sempre visível)
            fig.add_hline(y=0.05, line_dash="dash", line_color="green", 
                         annotation_text="Risco Baixo (<0.05)", annotation_position="top right")
            
            # Exibe o gráfico
            st.plotly_chart(fig, use_container_width=True)
            
            # Estatísticas resumidas
            st.subheader("📊 Estatísticas das Predições")
            col_stats1, col_stats2, col_stats3 = st.columns(3)
            
            with col_stats1:
                st.metric(
                    "Total de Predições",
                    len(st.session_state.predictions),
                    help="Número total de avaliações realizadas"
                )
            
            with col_stats2:
                avg_prob = sum(pred_probabilities) / len(pred_probabilities)
                st.metric(
                    "Probabilidade Média",
                    f"{avg_prob:.1f}%",
                    help="Probabilidade média de todas as predições"
                )
            
            with col_stats3:
                high_risk_count = sum(1 for risk in pred_risks if risk == "Alto")
                st.metric(
                    "Predições de Alto Risco",
                    high_risk_count,
                    help="Número de predições com risco alto"
                )
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
st.title("🏥 Sepsis Sentinel AI")
st.markdown("#### **Sistema Inteligente de Detecção Precoce de Sepse**")
#st.markdown("*Plataforma de Apoio à Decisão Clínica com Machine Learning*")
st.markdown("---")

# Verificação de saúde da API (apenas para logs)
api_healthy, health_data = check_api_health()

# Log da verificação (não exibido na interface)
if not api_healthy:

    print("❌ API Desconectada - Verifique se o backend está rodando")

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