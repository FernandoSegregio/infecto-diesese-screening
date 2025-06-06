import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import json
import time

# Importações da nova estrutura modular
from src.core import TriagemMedica
from src.auth import AuthManager, SecurityManager
from src.iot import IoTDashboard, MQTTManager
from src.utils import (
    detectar_regiao_automatica,
    detectar_febre_automatica,
    get_regiao_nomes,
    get_regiao_nomes_curtos
)

# Configuração da página
st.set_page_config(
    page_title="IA Triagem Médica - Áreas Vulneráveis",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicialização dos sistemas
@st.cache_resource
def carregar_modelo():
    return TriagemMedica()

@st.cache_resource
def carregar_auth():
    return AuthManager()

@st.cache_resource
def carregar_security():
    return SecurityManager()

@st.cache_resource
def carregar_iot():
    """Inicializa o IoT Dashboard"""
    return IoTDashboard()

@st.cache_resource
def carregar_mqtt():
    """Inicializa e inicia o cliente MQTT"""
    mqtt_manager = MQTTManager()
    # Iniciar cliente MQTT em background
    success = mqtt_manager.start()
    if success:
        print("🌡️ MQTT Manager iniciado com sucesso!")
    else:
        print("⚠️ Falha ao iniciar MQTT Manager")
    return mqtt_manager

triagem = carregar_modelo()
auth = carregar_auth()
security = carregar_security()
mqtt_manager = carregar_mqtt()
iot_dashboard = IoTDashboard(mqtt_manager=mqtt_manager)

# Verificar autenticação
if not auth.is_authenticated():
    auth.show_login_form()
    st.stop()

# Exibir informações do usuário
auth.show_user_info()

# CSS customizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .urgencia-critica {
        background-color: #dc3545;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .urgencia-alta {
        background-color: #fd7e14;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .urgencia-media {
        background-color: #ffc107;
        color: #212529;
        padding: 1rem;
        border-radius: 10px;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .urgencia-baixa {
        background-color: #28a745;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .resultado-box {
        border: 2px solid #dee2e6;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #212529;
    }
    .resultado-box h2 {
        color: #1e3c72;
        margin-bottom: 0.5rem;
    }
    .resultado-box h3 {
        color: #2a5298;
        margin-bottom: 1rem;
    }
    .resultado-box h4 {
        color: #495057;
        margin-bottom: 0.5rem;
    }
    .resultado-box p {
        color: #6c757d;
        margin-bottom: 0.25rem;
    }
    .resultado-box strong {
        color: #212529;
    }
    .medicamento-box {
        border: 2px solid #e3f2fd;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        background-color: #f8f9ff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #212529;
    }
    .medicamento-box h4 {
        color: #1976d2;
        margin-bottom: 1rem;
    }
    .medicamento-box p {
        color: #424242;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
    }
    .medicamento-box strong {
        color: #1565c0;
        font-size: 1.1rem;
    }
    .paciente-saudavel {
        border: 2px solid #4caf50;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: linear-gradient(135deg, #e8f5e8 0%, #f1f8e9 100%);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        color: #2e7d32;
        text-align: center;
    }
    .paciente-saudavel h2 {
        color: #1b5e20;
        margin-bottom: 0.5rem;
    }
    .paciente-saudavel h3 {
        color: #2e7d32;
        margin-bottom: 1rem;
    }
    .paciente-saudavel .check-icon {
        font-size: 3rem;
        color: #4caf50;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>🏥 IA para Triagem Médica em Áreas Vulneráveis</h1>
    <p>Sistema de apoio ao diagnóstico baseado em eventos climáticos e epidemiologia</p>
</div>
""", unsafe_allow_html=True)

# Sidebar para navegação
st.sidebar.title("📋 Menu de Navegação")

# Obter permissões do usuário
permissions = auth.get_user_permissions()

# Criar lista de páginas baseada nas permissões
paginas_disponiveis = []
if permissions.get('triagem', False):
    paginas_disponiveis.append("🩺 Triagem Médica")
if permissions.get('estatisticas', False):
    paginas_disponiveis.append("📊 Estatísticas")
if permissions.get('historico', False):
    paginas_disponiveis.append("📋 Histórico")
if permissions.get('audit_log', False):
    paginas_disponiveis.append("🔍 Log de Auditoria")

# Adicionar página IoT para todos os usuários autenticados
paginas_disponiveis.append("🌡️ Dashboard IoT")
paginas_disponiveis.append("💊 Gestão de Medicamentos")
paginas_disponiveis.append("ℹ️ Sobre o Sistema")

pagina = st.sidebar.selectbox(
    "Selecione uma opção:",
    paginas_disponiveis
)

if pagina == "🩺 Triagem Médica":
    auth.require_permission('triagem')
    st.header("🩺 Formulário de Triagem Médica")
    
    # Controle MQTT para solicitar medição de temperatura
    if mqtt_manager and mqtt_manager.connected:
        st.subheader("🎮 Controle Remoto do Termômetro ESP32")
        
        col_mqtt1, col_mqtt2, col_mqtt3 = st.columns([2, 1, 1])
        
        with col_mqtt1:
            st.info("🌡️ **Solicitação de medição via MQTT**")
            st.write("Use o botão abaixo para solicitar uma medição de temperatura imediata do sensor ESP32")
        
        with col_mqtt2:
            if st.button("📏 Medir Temperatura", 
                        use_container_width=True,
                        help="Solicita medição imediata via MQTT"):
                with st.spinner("🔄 Enviando comando via MQTT..."):
                    success = mqtt_manager.request_temperature_reading("ESP32_TERMOMETRO_001")
                    if success:
                        st.success("✅ Comando enviado!")
                        st.info("🕐 Aguarde alguns segundos e clique em 'Atualizar IoT' abaixo para ver o resultado")
                        st.balloons()
                    else:
                        st.error("❌ Falha no comando MQTT")
                        st.error("🔧 Verifique se o ESP32 está conectado ao MQTT")
        
        with col_mqtt3:
            mqtt_status = "🟢 Conectado" if mqtt_manager.connected else "🔴 Desconectado"
            st.metric("Status MQTT", mqtt_status)
        
        st.divider()
    
    # Verificar se há temperatura disponível do IoT (FORA do formulário)
    latest_temp = iot_dashboard.get_latest_temperature_for_triagem()
    temperatura_iot = None
    
    if latest_temp:
        st.success(f"🌡️ **Temperatura detectada:** {latest_temp['temperature']}°C "
                  f"(Dispositivo: {latest_temp['device_id']}) {latest_temp['status']}")
        
        col_iot1, col_iot2 = st.columns([3, 1])
        with col_iot1:
            st.info("💡 A temperatura do sensor IoT será usada automaticamente no formulário abaixo")
        with col_iot2:
            if st.button("🔄 Atualizar IoT", help="Buscar nova temperatura do sensor IoT"):
                st.rerun()
        
        temperatura_iot = float(latest_temp['temperature'])
        st.divider()
    else:
        st.info("💡 **Dica:** Use o controle MQTT acima ou conecte um sensor IoT para medição automática")
        
        # Botão para atualizar mesmo sem leitura
        col_update1, col_update2 = st.columns([3, 1])
        with col_update1:
            st.write("Clique em 'Atualizar IoT' para verificar se há novas leituras disponíveis")
        with col_update2:
            if st.button("🔄 Atualizar IoT", help="Verificar se há novas leituras do sensor"):
                st.rerun()
        
        # Mostrar último comando MQTT enviado se disponível
        if 'mqtt_command_history' in st.session_state and st.session_state['mqtt_command_history']:
            last_command = st.session_state['mqtt_command_history'][-1]
            st.info(f"📤 Último comando: {last_command}")
        
        st.divider()

    # Detecção automática de região
    regiao_automatica = detectar_regiao_automatica()
    
    # Seleção de Região Geográfica
    st.subheader("🌍 Região Geográfica")
    col_regiao1, col_regiao2 = st.columns([2, 1])
    
    with col_regiao1:
        regiao_nomes = get_regiao_nomes()
        st.info(f"🎯 **Região detectada automaticamente:** {regiao_nomes[regiao_automatica]}")
        
        regiao_selecionada = st.selectbox(
            "Confirme ou altere a região onde o paciente se encontra:",
            ["brasil_norte", "africa", "asia"],
            index=["brasil_norte", "africa", "asia"].index(regiao_automatica),
            format_func=lambda x: {
                "brasil_norte": "🇧🇷 Norte do Brasil (Amazônia)",
                "africa": "🌍 África Subsaariana", 
                "asia": "🌏 Ásia (Sul e Sudeste)"
            }[x]
        )
    
    with col_regiao2:
        if regiao_selecionada == "brasil_norte":
            st.info("**Doenças prevalentes:**\nLeptospirose, Malária, Dengue, Hepatite A, Leishmaniose")
        elif regiao_selecionada == "africa":
            st.info("**Doenças prevalentes:**\nCólera, Malária, Febre Amarela, Meningite, Esquistossomose")
        else:  # asia
            st.info("**Doenças prevalentes:**\nCólera, Dengue, Febre Tifoide, Hepatite E, Chikungunya")
    
    # Formulário principal
    with st.form("formulario_triagem"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📝 Dados do Paciente")
            idade = st.number_input("Idade (anos)", min_value=0, max_value=120, value=30)
            sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Não informado"])
            peso = st.number_input("Peso (kg)", min_value=0.0, max_value=200.0, value=70.0, step=0.1)
            
            st.subheader("🌡️ Sinais Vitais")
            
            # Usar temperatura IoT se disponível, senão valor padrão
            temp_default = temperatura_iot if temperatura_iot else 36.5
            temperatura = st.number_input("Temperatura (°C)", min_value=30.0, max_value=45.0, 
                                        value=temp_default, step=0.1)
            
            if temperatura_iot:
                st.success(f"✅ Usando temperatura do sensor IoT: {temperatura_iot}°C")
            
            # Detecção automática de febre
            sintomas_febre_auto = detectar_febre_automatica(temperatura)
            if sintomas_febre_auto:
                if 'febre_alta' in sintomas_febre_auto:
                    st.warning(f"🔥 **Febre alta detectada automaticamente** (≥39°C): {temperatura}°C")
                else:
                    st.info(f"🌡️ **Febre detectada automaticamente** (≥37.8°C): {temperatura}°C")
            
            pressao_sistolica = st.number_input("Pressão Sistólica (mmHg)", min_value=50, max_value=250, value=120)
            pressao_diastolica = st.number_input("Pressão Diastólica (mmHg)", min_value=30, max_value=150, value=80)
            frequencia_cardiaca = st.number_input("Frequência Cardíaca (bpm)", min_value=30, max_value=200, value=70)
        
        with col2:
            st.subheader("🤒 Sintomas Apresentados")
            
            # Mostrar sintomas de febre detectados automaticamente
            if sintomas_febre_auto:
                st.info(f"✅ **Sintomas detectados automaticamente pelos sinais vitais:**\n• {', '.join([{'febre': 'Febre', 'febre_alta': 'Febre alta'}[s] for s in sintomas_febre_auto])}")
            
            sintomas_opcoes = [
                "dor_cabeca", "dor_muscular", "dor_articular", 
                "nausea", "vomito", "diarreia", "tosse", "dificuldade_respirar", 
                "calafrios", "manchas_pele", "conjuntivite", "dor_abdominal", 
                "ictericia", "sangue_fezes", "rigidez_nuca", "confusao_mental"
            ]
            
            sintomas_labels = {
                "dor_cabeca": "Dor de cabeça",
                "dor_muscular": "Dor muscular",
                "dor_articular": "Dor nas articulações",
                "nausea": "Náusea",
                "vomito": "Vômito",
                "diarreia": "Diarreia",
                "tosse": "Tosse",
                "dificuldade_respirar": "Dificuldade para respirar",
                "calafrios": "Calafrios",
                "manchas_pele": "Manchas/erupções na pele",
                "conjuntivite": "Conjuntivite (olhos vermelhos)",
                "dor_abdominal": "Dor abdominal",
                "ictericia": "Icterícia (amarelão)",
                "sangue_fezes": "Sangue nas fezes",
                "rigidez_nuca": "Rigidez na nuca",
                "confusao_mental": "Confusão mental"
            }
            
            sintomas_selecionados = []
            
            # Adicionar sintomas de febre automaticamente
            sintomas_selecionados.extend(sintomas_febre_auto)
            
            # Checkboxes para outros sintomas
            for sintoma in sintomas_opcoes:
                if st.checkbox(sintomas_labels[sintoma], key=sintoma):
                    sintomas_selecionados.append(sintoma)
            
            st.subheader("🌦️ Contexto Ambiental")
            evento_climatico = st.selectbox(
                "Evento Climático Recente",
                ["", "enchentes", "chuvas_intensas", "secas", "ondas_calor", "frio", "umidade", 
                 "calor_umidade", "tempestades", "baixa_umidade", "aglomeracao", "baixa_ventilacao",
                 "falta_saneamento", "areas_rurais", "areas_endemicas", "habitacoes_precarias"]
            )
            
            tempo_sintomas = st.number_input("Tempo dos sintomas (dias)", min_value=1, max_value=90, value=1)
            
            st.subheader("👥 Informações Adicionais")
            populacao_vulneravel = st.selectbox(
                "População vulnerável?",
                ["Não", "Sim - Ribeirinho", "Sim - Comunidade isolada", "Sim - Área de risco", 
                 "Sim - Sem saneamento", "Sim - Habitação precária", "Sim - Área endêmica"]
            )
            
            historico_medico = st.multiselect(
                "Histórico médico relevante",
                ["diabetes", "hipertensao", "cardiopatia", "pneumopatia", "imunossupressao", 
                 "desnutricao", "hiv", "cancer", "tuberculose", "hepatite", "doenca_renal",
                 "gestante", "lactante", "vacinacao_incompleta", "contato_doente"]
            )
        
        # Botão de submissão
        submitted = st.form_submit_button("🔍 Processar Triagem", use_container_width=True)
        
        if submitted:
            # Preparar dados do paciente
            dados_paciente = {
                'idade': idade,
                'sexo': sexo,
                'peso': peso,
                'temperatura': temperatura,
                'pressao_sistolica': pressao_sistolica,
                'pressao_diastolica': pressao_diastolica,
                'frequencia_cardiaca': frequencia_cardiaca,
                'sintomas': sintomas_selecionados,  # Já inclui febre automática
                'evento_climatico': evento_climatico,
                'tempo_sintomas': tempo_sintomas,
                'historico_medico': historico_medico,
                'populacao_vulneravel': populacao_vulneravel != "Não",
                'regiao_geografica': regiao_selecionada
            }
            
            # Validar dados médicos
            validation_errors = security.validate_medical_data(dados_paciente)
            if validation_errors:
                st.error("❌ Dados inválidos:")
                for error in validation_errors:
                    st.error(f"• {error}")
                st.stop()
            
            # Log da ação
            auth._log_audit('TRIAGEM_REALIZADA', st.session_state['username'], 
                          f"Paciente: {security.hash_patient_id(dados_paciente)}")
            
            # Processar triagem
            with st.spinner("Processando triagem médica..."):
                resultado = triagem.processar_triagem(dados_paciente)
            
            # Exibir resultados
            st.success("✅ Triagem processada com sucesso!")
            
            # Mostrar informações sobre detecção automática
            if sintomas_febre_auto:
                regiao_nomes_curtos = {
                    'brasil_norte': 'Norte do Brasil', 
                    'africa': 'África', 
                    'asia': 'Ásia'
                }
                st.info(f"🤖 **Detecção automática ativada:**\n• Febre detectada pelos sinais vitais: {temperatura}°C\n• Região detectada: {regiao_nomes_curtos[regiao_selecionada]}")
            
            # Adicionar informações de segurança ao resultado
            resultado['processed_by'] = st.session_state['user_name']
            resultado['processed_at'] = datetime.now().isoformat()
            resultado['patient_hash'] = security.hash_patient_id(dados_paciente)
            
            # Verifica se é paciente saudável para exibição especial
            if "Saudável" in resultado['diagnostico_principal']:
                # Layout especial para paciente saudável
                st.markdown(f"""
                <div class="paciente-saudavel">
                    <div class="check-icon">✅</div>
                    <h2>{resultado['diagnostico_principal']}</h2>
                    <h3>Probabilidade: {resultado['probabilidade']}%</h3>
                    <p><strong>Status:</strong> Sem necessidade de medicação</p>
                    <p><strong>Urgência:</strong> {resultado['nivel_urgencia']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Observações e recomendações para paciente saudável
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📋 Observações Clínicas")
                    for obs in resultado['observacoes']:
                        st.write(f"• {obs}")
                
                with col2:
                    st.subheader("💡 Recomendações Preventivas")
                    for rec in resultado['recomendacoes']:
                        st.write(f"• {rec}")
            
            else:
                # Layout normal para diagnósticos médicos
                # Resultado principal
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="resultado-box">
                        <h3>🎯 Diagnóstico Principal</h3>
                        <h2>{resultado['diagnostico_principal']}</h2>
                        <p><strong>Probabilidade:</strong> {resultado['probabilidade']}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    urgencia_class = f"urgencia-{resultado['nivel_urgencia'].lower()}"
                    st.markdown(f"""
                    <div class="{urgencia_class}">
                        <h4>⚠️ Urgência</h4>
                        <h3>{resultado['nivel_urgencia']}</h3>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    if resultado['medicamentos'] == 'Observação clínica':
                        st.markdown(f"""
                        <div class="medicamento-box">
                            <h4>👁️ Conduta</h4>
                            <p><strong>{resultado['medicamentos']}</strong></p>
                            <p><strong>Acompanhamento:</strong> Observação</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="medicamento-box">
                            <h4>💊 Medicamento</h4>
                            <p><strong>{resultado['medicamentos']}</strong></p>
                            <p><strong>Dosagem:</strong> {resultado['dosagem']}</p>
                            <p><strong>Frequência:</strong> {resultado['frequencia']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Observações e recomendações
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📋 Observações Clínicas")
                    for obs in resultado['observacoes']:
                        st.write(f"• {obs}")
                    
                    # Informações adicionais da doença
                    if 'tempo_incubacao' in resultado:
                        st.write(f"**⏱️ Tempo de incubação:** {resultado['tempo_incubacao']}")
                    if 'gravidade_doenca' in resultado:
                        st.write(f"**⚠️ Gravidade da doença:** {resultado['gravidade_doenca']}")
                
                with col2:
                    st.subheader("💡 Recomendações")
                    for rec in resultado['recomendacoes']:
                        st.write(f"• {rec}")
                
                # Diagnósticos diferenciais se existirem
                if resultado.get('diagnosticos_diferenciais') and len(resultado['diagnosticos_diferenciais']) > 0:
                    st.subheader("🔍 Diagnósticos Diferenciais")
                    st.write("*Outras possibilidades a considerar:*")
                    
                    cols = st.columns(len(resultado['diagnosticos_diferenciais']))
                    for i, diag_diff in enumerate(resultado['diagnosticos_diferenciais']):
                        with cols[i]:
                            st.markdown(f"""
                            <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; text-align: center;">
                                <strong>{diag_diff['nome']}</strong><br>
                                <span style="color: #666;">{diag_diff['probabilidade']}%</span>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Detalhes do score (para profissionais mais experientes)
                if resultado.get('detalhes_score'):
                    with st.expander("📊 Detalhes da Análise (Avançado)"):
                        detalhes = resultado['detalhes_score']
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Score Sintomas", f"{detalhes.get('sintomas', 0):.2f}")
                        with col2:
                            st.metric("Score Climático", f"{detalhes.get('climatico', 0):.2f}")
                        with col3:
                            st.metric("Score População", f"{detalhes.get('populacao', 0):.2f}")
                        with col4:
                            st.metric("Score Gravidade", f"{detalhes.get('gravidade', 0):.2f}")
                        
                        st.write("*Fórmula: (Sintomas × 45%) + (Climático × 25%) + (População × 15%) + (Gravidade × 15%)*")

elif pagina == "📊 Estatísticas":
    auth.require_permission('estatisticas')
    st.header("📊 Estatísticas Epidemiológicas")
    
    stats = triagem.obter_estatisticas()
    
    if not stats:
        st.info("📝 Nenhum atendimento registrado ainda. Realize algumas triagens para ver as estatísticas.")
    else:
        # Log da ação
        auth._log_audit('ESTATISTICAS_ACESSADAS', st.session_state['username'])
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total de Atendimentos", stats['total_atendimentos'])
        
        with col2:
            st.metric("Idade Média", f"{stats['idade_media']:.1f} anos")
        
        with col3:
            urgencia_critica = stats['urgencia_distribuicao'].get('CRÍTICA', 0)
            st.metric("Casos Críticos", urgencia_critica)
        
        with col4:
            diagnostico_freq = max(stats['diagnosticos_frequentes'].items(), key=lambda x: x[1])
            st.metric("Diagnóstico Mais Comum", diagnostico_freq[0])
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribuição de Diagnósticos")
            if stats['diagnosticos_frequentes']:
                fig_diag = px.pie(
                    values=list(stats['diagnosticos_frequentes'].values()),
                    names=list(stats['diagnosticos_frequentes'].keys()),
                    title="Diagnósticos por Frequência"
                )
                st.plotly_chart(fig_diag, use_container_width=True)
        
        with col2:
            st.subheader("Níveis de Urgência")
            if stats['urgencia_distribuicao']:
                cores_urgencia = {
                    'CRÍTICA': '#ff4444',
                    'ALTA': '#ff8800',
                    'MÉDIA': '#ffaa00',
                    'BAIXA': '#00aa00'
                }
                
                fig_urgencia = px.bar(
                    x=list(stats['urgencia_distribuicao'].keys()),
                    y=list(stats['urgencia_distribuicao'].values()),
                    title="Distribuição por Urgência",
                    color=list(stats['urgencia_distribuicao'].keys()),
                    color_discrete_map=cores_urgencia
                )
                st.plotly_chart(fig_urgencia, use_container_width=True)
        
        # Eventos climáticos
        st.subheader("Eventos Climáticos Associados")
        if stats['eventos_climaticos']:
            fig_clima = px.bar(
                x=list(stats['eventos_climaticos'].values()),
                y=list(stats['eventos_climaticos'].keys()),
                orientation='h',
                title="Frequência de Eventos Climáticos"
            )
            st.plotly_chart(fig_clima, use_container_width=True)

elif pagina == "📋 Histórico":
    auth.require_permission('historico')
    st.header("📋 Histórico de Atendimentos")
    
    # Log da ação
    auth._log_audit('HISTORICO_ACESSADO', st.session_state['username'])
    
    historico = triagem.obter_historico()
    
    if not historico:
        st.info("📝 Nenhum atendimento registrado ainda.")
    else:
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            diagnosticos_unicos = list(set([item['resultado']['diagnostico_principal'] for item in historico]))
            filtro_diagnostico = st.selectbox("Filtrar por diagnóstico", ["Todos"] + diagnosticos_unicos)
        
        with col2:
            urgencias_unicas = list(set([item['resultado']['nivel_urgencia'] for item in historico]))
            filtro_urgencia = st.selectbox("Filtrar por urgência", ["Todas"] + urgencias_unicas)
        
        with col3:
            st.write(f"**Total de registros:** {len(historico)}")
        
        # Aplicar filtros
        historico_filtrado = historico
        if filtro_diagnostico != "Todos":
            historico_filtrado = [item for item in historico_filtrado if item['resultado']['diagnostico_principal'] == filtro_diagnostico]
        if filtro_urgencia != "Todas":
            historico_filtrado = [item for item in historico_filtrado if item['resultado']['nivel_urgencia'] == filtro_urgencia]
        
        # Exibir histórico
        for i, item in enumerate(reversed(historico_filtrado[-20:])):  # Últimos 20 registros
            timestamp = datetime.fromisoformat(item['timestamp'])
            
            with st.expander(f"🏥 Atendimento {len(historico_filtrado)-i} - {timestamp.strftime('%d/%m/%Y %H:%M')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Dados do Paciente:**")
                    st.write(f"• Idade: {item['dados_paciente']['idade']} anos")
                    st.write(f"• Sexo: {item['dados_paciente']['sexo']}")
                    st.write(f"• Temperatura: {item['dados_paciente']['temperatura']}°C")
                    st.write(f"• Sintomas: {', '.join(item['dados_paciente']['sintomas'])}")
                
                with col2:
                    st.write("**Resultado:**")
                    st.write(f"• Diagnóstico: {item['resultado']['diagnostico_principal']}")
                    st.write(f"• Probabilidade: {item['resultado']['probabilidade']}%")
                    st.write(f"• Urgência: {item['resultado']['nivel_urgencia']}")
                    st.write(f"• Medicamento: {item['resultado']['medicamentos']}")
                    
                    # Mostrar informações de segurança se disponíveis
                    if 'processed_by' in item['resultado']:
                        st.write(f"• Processado por: {item['resultado']['processed_by']}")

elif pagina == "🔍 Log de Auditoria":
    auth.require_permission('audit_log')
    st.header("🔍 Log de Auditoria")
    
    # Log da ação
    auth._log_audit('AUDIT_LOG_ACESSADO', st.session_state['username'])
    
    if os.path.exists(auth.audit_file):
        try:
            with open(auth.audit_file, 'r') as f:
                audit_log = json.load(f)
            
            if audit_log:
                # Filtros
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    acoes_unicas = list(set([item['action'] for item in audit_log]))
                    filtro_acao = st.selectbox("Filtrar por ação", ["Todas"] + acoes_unicas)
                
                with col2:
                    usuarios_unicos = list(set([item['username'] for item in audit_log]))
                    filtro_usuario = st.selectbox("Filtrar por usuário", ["Todos"] + usuarios_unicos)
                
                with col3:
                    st.write(f"**Total de registros:** {len(audit_log)}")
                
                # Aplicar filtros
                audit_filtrado = audit_log
                if filtro_acao != "Todas":
                    audit_filtrado = [item for item in audit_filtrado if item['action'] == filtro_acao]
                if filtro_usuario != "Todos":
                    audit_filtrado = [item for item in audit_filtrado if item['username'] == filtro_usuario]
                
                # Exibir log
                st.subheader("Registros de Auditoria")
                
                # Criar DataFrame para melhor visualização
                df_audit = pd.DataFrame(audit_filtrado[-50:])  # Últimos 50 registros
                if not df_audit.empty:
                    df_audit['timestamp'] = pd.to_datetime(df_audit['timestamp'])
                    df_audit = df_audit.sort_values('timestamp', ascending=False)
                    
                    # Mascarar informações sensíveis
                    df_audit['details'] = df_audit['details'].apply(lambda x: security.mask_sensitive_info(str(x)))
                    
                    st.dataframe(
                        df_audit[['timestamp', 'action', 'username', 'ip_address', 'details']],
                        use_container_width=True
                    )
                    
                    # Estatísticas do log
                    st.subheader("📊 Estatísticas de Auditoria")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig_acoes = px.pie(
                            values=df_audit['action'].value_counts().values,
                            names=df_audit['action'].value_counts().index,
                            title="Distribuição de Ações"
                        )
                        st.plotly_chart(fig_acoes, use_container_width=True)
                    
                    with col2:
                        fig_usuarios = px.bar(
                            x=df_audit['username'].value_counts().values,
                            y=df_audit['username'].value_counts().index,
                            orientation='h',
                            title="Atividade por Usuário"
                        )
                        st.plotly_chart(fig_usuarios, use_container_width=True)
                else:
                    st.info("Nenhum registro encontrado com os filtros aplicados.")
            else:
                st.info("📝 Nenhum registro de auditoria encontrado.")
        except Exception as e:
            st.error(f"Erro ao carregar log de auditoria: {str(e)}")
    else:
        st.info("📝 Arquivo de auditoria não encontrado.")

elif pagina == "🌡️ Dashboard IoT":
    # Dashboard IoT disponível para todos os usuários autenticados
    st.header("🌡️ Dashboard IoT - Sensores de Temperatura")
    
    # Log da ação
    auth._log_audit('DASHBOARD_IOT_ACESSADO', st.session_state['username'])
    
    # Exibir dashboard IoT
    iot_dashboard.show_dashboard()

elif pagina == "💊 Gestão de Medicamentos":
    # Página de gestão de medicamentos disponível para todos os usuários autenticados
    st.header("💊 Gestão de Medicamentos")
    
    # Log da ação
    auth._log_audit('MEDICAMENTOS_ACESSADO', st.session_state['username'])
    
    st.markdown("""
    Esta funcionalidade analisa o histórico de triagens para calcular as necessidades de medicamentos
    e gerar listas de compras inteligentes baseadas em dados reais de atendimento.
    """)
    
    # Configurações de análise
    st.subheader("⚙️ Configurações da Análise")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        periodo_analise = st.selectbox(
            "Período para análise histórica:",
            [7, 15, 30, 60, 90],
            index=2,
            help="Quantos dias de histórico usar para calcular necessidades"
        )
    
    with col2:
        periodo_projecao = st.selectbox(
            "Período para projeção:",
            [7, 15, 30, 60, 90],
            index=2,
            help="Para quantos dias calcular as necessidades futuras"
        )
    
    with col3:
        incluir_detalhes = st.checkbox(
            "Incluir detalhes técnicos",
            value=True,
            help="Mostrar estatísticas detalhadas e metodologia"
        )
    
    # Botão para gerar análise
    if st.button("📊 Gerar Análise de Medicamentos", use_container_width=True):
        with st.spinner("Analisando histórico de triagens..."):
            lista_compras = triagem.gerar_lista_compras_medicamentos(
                periodo_dias=periodo_analise,
                projecao_dias=periodo_projecao,
                incluir_detalhes=incluir_detalhes
            )
        
        if 'erro' in lista_compras:
            st.error(f"❌ {lista_compras['erro']}")
            st.info("💡 Realize algumas triagens primeiro para gerar a análise de medicamentos")
        else:
            # Exibir resultados
            st.success("✅ Análise de medicamentos gerada com sucesso!")
            
            # Resumo executivo
            st.subheader("📋 Resumo Executivo")
            
            resumo = lista_compras['resumo']
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Medicamentos Diferentes", resumo['total_medicamentos_diferentes'])
            with col2:
                st.metric("Unidades Estimadas", resumo['total_unidades_estimadas'])
            with col3:
                st.metric("Período de Cobertura", resumo['periodo_cobertura'])
            with col4:
                st.metric("Baseado em", resumo['baseado_em'])
            
            # Informações do período
            col_info1, col_info2 = st.columns(2)
            with col_info1:
                st.info(f"📅 **Período analisado:** {lista_compras['periodo_analise']}")
            with col_info2:
                st.info(f"🎯 **Projeção para:** {lista_compras['projecao_para']}")
            
            # Lista de medicamentos por prioridade
            st.subheader("💊 Lista de Medicamentos por Prioridade")
            
            medicamentos_por_prioridade = lista_compras['medicamentos_por_prioridade']
            
            # Prioridade CRÍTICA
            if medicamentos_por_prioridade['CRÍTICA']:
                st.markdown("### 🚨 PRIORIDADE CRÍTICA")
                st.error("⚠️ Medicamentos essenciais - não podem faltar!")
                
                for med in medicamentos_por_prioridade['CRÍTICA']:
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.write(f"**{med['medicamento']}**")
                    with col2:
                        st.write(f"**{med['quantidade']} unidades**")
                    with col3:
                        st.write(f"{med['frequencia']}% dos casos")
                    with col4:
                        st.write(f"Usado {med['usado_periodo']}x")
                
                st.divider()
            
            # Prioridade ALTA
            if medicamentos_por_prioridade['ALTA']:
                st.markdown("### 🔴 PRIORIDADE ALTA")
                st.warning("Medicamentos importantes - manter estoque adequado")
                
                for med in medicamentos_por_prioridade['ALTA']:
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    with col1:
                        st.write(f"**{med['medicamento']}**")
                    with col2:
                        st.write(f"**{med['quantidade']} unidades**")
                    with col3:
                        st.write(f"{med['frequencia']}% dos casos")
                    with col4:
                        st.write(f"Usado {med['usado_periodo']}x")
                
                st.divider()
            
            # Prioridade MÉDIA
            if medicamentos_por_prioridade['MÉDIA']:
                st.markdown("### 🟡 PRIORIDADE MÉDIA")
                
                with st.expander("Ver medicamentos de prioridade média", expanded=False):
                    for med in medicamentos_por_prioridade['MÉDIA']:
                        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                        with col1:
                            st.write(f"**{med['medicamento']}**")
                        with col2:
                            st.write(f"{med['quantidade']} unidades")
                        with col3:
                            st.write(f"{med['frequencia']}% dos casos")
                        with col4:
                            st.write(f"Usado {med['usado_periodo']}x")
            
            # Prioridade BAIXA
            if medicamentos_por_prioridade['BAIXA']:
                st.markdown("### 🟢 PRIORIDADE BAIXA")
                
                with st.expander("Ver medicamentos de prioridade baixa", expanded=False):
                    for med in medicamentos_por_prioridade['BAIXA']:
                        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                        with col1:
                            st.write(f"**{med['medicamento']}**")
                        with col2:
                            st.write(f"{med['quantidade']} unidades")
                        with col3:
                            st.write(f"{med['frequencia']}% dos casos")
                        with col4:
                            st.write(f"Usado {med['usado_periodo']}x")
            
            # Lista de compras formatada
            st.subheader("📝 Lista de Compras Formatada")
            
            lista_texto = "LISTA DE COMPRAS - MEDICAMENTOS\n"
            lista_texto += f"Período: {lista_compras['periodo_analise']}\n"
            lista_texto += f"Projeção: {lista_compras['projecao_para']}\n"
            lista_texto += f"Total estimado: {resumo['total_unidades_estimadas']} unidades\n\n"
            
            for prioridade in ['CRÍTICA', 'ALTA', 'MÉDIA', 'BAIXA']:
                if medicamentos_por_prioridade[prioridade]:
                    lista_texto += f"=== PRIORIDADE {prioridade} ===\n"
                    for med in medicamentos_por_prioridade[prioridade]:
                        lista_texto += f"• {med['medicamento']}: {med['quantidade']} unidades\n"
                    lista_texto += "\n"
            
            st.text_area("Lista para copiar:", lista_texto, height=300)
            
            # Botão para download
            st.download_button(
                label="📥 Download Lista de Compras",
                data=lista_texto,
                file_name=f"lista_medicamentos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
            
            # Estatísticas detalhadas (se solicitado)
            if incluir_detalhes and lista_compras['estatisticas']:
                st.subheader("📊 Estatísticas Detalhadas")
                
                stats = lista_compras['estatisticas']
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**📈 Análise Temporal**")
                    st.write(f"• Período analisado: {stats['periodo_analise_dias']} dias")
                    st.write(f"• Total de triagens: {stats['total_triagens_periodo']}")
                    st.write(f"• Média diária: {stats['media_triagens_dia']} triagens/dia")
                    st.write(f"• Projeção: {stats['projecao_triagens']} triagens em {stats['projecao_dias']} dias")
                
                with col2:
                    st.write("**🏥 Distribuição de Urgência**")
                    for urgencia, count in stats['distribuicao_urgencia'].items():
                        percent = (count / stats['total_triagens_periodo']) * 100
                        st.write(f"• {urgencia}: {count} casos ({percent:.1f}%)")
                
                # Gráficos de análise
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**🔝 Diagnósticos Mais Comuns**")
                    if stats['diagnosticos_mais_comuns']:
                        fig_diag = px.bar(
                            x=list(stats['diagnosticos_mais_comuns'].values()),
                            y=list(stats['diagnosticos_mais_comuns'].keys()),
                            orientation='h',
                            title="Top 5 Diagnósticos"
                        )
                        st.plotly_chart(fig_diag, use_container_width=True)
                
                with col2:
                    st.write("**💊 Medicamentos Mais Usados**")
                    if stats['medicamentos_mais_usados']:
                        fig_med = px.bar(
                            x=list(stats['medicamentos_mais_usados'].values()),
                            y=list(stats['medicamentos_mais_usados'].keys()),
                            orientation='h',
                            title="Top 5 Medicamentos"
                        )
                        st.plotly_chart(fig_med, use_container_width=True)
                
                # Metodologia
                with st.expander("🔬 Metodologia de Cálculo", expanded=False):
                    st.markdown("""
                    **Como calculamos as necessidades:**
                    
                    1. **Análise Histórica**: Analisamos todas as triagens do período selecionado
                    2. **Frequência de Uso**: Calculamos quantas vezes cada medicamento foi prescrito
                    3. **Projeção Estatística**: Baseamos a projeção na média diária de triagens
                    4. **Margem de Segurança**: Adicionamos 20% extra para evitar falta de estoque
                    5. **Priorização Clínica**: Classificamos por criticidade médica e frequência de uso
                    
                    **Critérios de Prioridade:**
                    - **CRÍTICA**: Medicamentos essenciais (Artesunato, Quinina, Ceftriaxona, etc.)
                    - **ALTA**: Frequência ≥15% ou 3+ casos urgentes
                    - **MÉDIA**: Frequência ≥5% ou 1+ caso urgente  
                    - **BAIXA**: Demais medicamentos
                    
                    **Fórmula**: `Necessidade = (Frequência × Projeção) + 20% margem`
                    """)
    
    # Informações adicionais
    st.subheader("💡 Como Usar Esta Funcionalidade")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **📋 Para Gestores de Estoque:**
        - Use período de 30-60 dias para análise
        - Projete para 30 dias de cobertura
        - Foque nos medicamentos de prioridade CRÍTICA e ALTA
        - Considere sazonalidade e eventos especiais
        """)
    
    with col2:
        st.info("""
        **🏥 Para Coordenadores Médicos:**
        - Analise os diagnósticos mais comuns
        - Verifique se há mudanças no padrão epidemiológico
        - Use os dados para treinamento da equipe
        - Monitore a eficácia dos tratamentos
        """)
    
    # Alertas e recomendações
    st.subheader("⚠️ Recomendações Importantes")
    
    st.warning("""
    **🔍 Validação Necessária:**
    - Esta análise é baseada em dados históricos e deve ser validada por profissionais médicos
    - Considere fatores externos: sazonalidade, surtos, mudanças populacionais
    - Mantenha sempre um estoque mínimo de medicamentos críticos
    - Revise periodicamente as necessidades conforme novos dados
    """)
    
    st.success("""
    **✅ Benefícios da Análise:**
    - Reduz desperdício de medicamentos
    - Evita falta de estoque crítico
    - Otimiza orçamento de compras
    - Melhora planejamento logístico
    - Baseia decisões em dados reais
    """)

elif pagina == "ℹ️ Sobre o Sistema":
    st.header("ℹ️ Sobre o Sistema de Triagem Médica Regionalizado")
    
    st.markdown("""
    ## 🎯 Objetivo
    
    Este sistema foi desenvolvido para apoiar profissionais de saúde em diferentes regiões do mundo, especialmente durante desastres naturais e emergências epidemiológicas. O sistema considera as doenças endêmicas e prevalentes de cada região geográfica.
    
    ## 🌍 Regiões Contempladas
    
    ### 🇧🇷 Norte do Brasil (Amazônia)
    **Características:** Enchentes frequentes, clima tropical, áreas rurais, rios abundantes
    
    **Doenças Principais:**
    - **Leptospirose** - Muito comum durante enchentes
    - **Malária** - Endêmica na região (prevalência muito alta)
    - **Dengue, Zika, Chikungunya** - Arboviroses urbanas
    - **Hepatite A** - Água contaminada pós-enchentes
    - **Leishmaniose** - Cutânea e visceral
    - **Doença de Chagas** - Áreas rurais
    - **Febre Tifoide** - Saneamento comprometido
    - **Febre Amarela** - Áreas de mata
    
    ### 🌍 África Subsaariana
    **Características:** Epidemias frequentes, saneamento precário, desnutrição
    
    **Doenças Principais:**
    - **Cólera** - Epidemias devastadoras (prevalência muito alta)
    - **Malária** - Principal causa de morte (prevalência muito alta)
    - **Febre Amarela** - Endêmica em várias regiões
    - **Meningite Meningocócica** - Cinturão da meningite
    - **Febre do Vale do Rift** - Surtos após chuvas
    - **Esquistossomose** - Águas contaminadas
    - **Doença do Sono** - Mosca tsé-tsé
    - **Hepatite E** - Problemas hepáticos graves
    
    ### 🌏 Ásia (Sul e Sudeste)
    **Características:** Monções, alta densidade populacional, resistência medicamentosa
    
    **Doenças Principais:**
    - **Dengue** - Maiores surtos mundiais (prevalência muito alta)
    - **Cólera** - Histórico de grandes epidemias
    - **Febre Tifoide** - Endêmica no Sul da Ásia
    - **Chikungunya** - Muito comum após monções
    - **Hepatite A e E** - Água contaminada
    - **Leptospirose** - Monções e áreas urbanas
    - **Encefalite Japonesa** - Áreas rurais
    - **Influenza Aviária** - Mercados de animais
    
    ## 🧠 Como Funciona o Sistema Regionalizado
    
    ### 4 Fatores de Análise Regionalizados
    - **Sintomas clínicos** (45%) - Específicos para cada doença regional
    - **Eventos climáticos** (25%) - Contexto ambiental da região
    - **População de risco** (15%) - Grupos vulneráveis específicos
    - **Gravidade + Prevalência regional** (15%) - Considera epidemiologia local
    
    ### 🔍 Inovações do Sistema
    
    #### ✅ Diagnóstico Regionalizado
    - **Base específica por região**: Doenças endêmicas e prevalentes
    - **Medicamentos adequados**: Considerando resistência regional
    - **Dosagens pediátricas**: Adaptadas para cada doença
    - **Prevalência regional**: Modifica probabilidade diagnóstica
    
    #### ✅ Urgência Inteligente
    - **Crítica**: Cólera, Febre Amarela, Meningite, Leishmaniose Visceral
    - **Alta**: Malária, Dengue, Leptospirose, Febre Tifoide
    - **Média**: Hepatites, Chikungunya, Esquistossomose
    - **Baixa**: Zika, Leishmaniose Cutânea
    
    #### ✅ Recomendações Regionalizadas
    - **Brasil Norte**: Repelentes, águas contaminadas, vigilância epidemiológica
    - **África**: Tratamento de água, isolamento, profilaxia de contatos
    - **Ásia**: Precauções em monções, alimentos seguros, monitoramento
    
    ## 📊 Doenças por Região (Total: 37 condições)
    
    | Região | Doenças Contempladas | Prevalência Muito Alta |
    |--------|---------------------|------------------------|
    | **Brasil Norte** | 12 doenças | Malária, Leptospirose, Diarreia |
    | **África** | 10 doenças | Cólera, Malária, Meningite, Esquistossomose |
    | **Ásia** | 12 doenças | Dengue, Cólera, Febre Tifoide, Hepatite E, Chikungunya, Leptospirose |
    
    ## 🌦️ Eventos Climáticos Monitorados
    
    - **Enchentes/Chuvas intensas**: Cólera, Leptospirose, Hepatites, Febre Tifoide
    - **Monções (Ásia)**: Dengue, Chikungunya, Leptospirose, Encefalite Japonesa
    - **Secas**: Meningite, Leishmaniose Visceral
    - **Calor + umidade**: Arboviroses (Dengue, Zika, Chikungunya)
    - **Áreas rurais**: Malária, Leishmaniose, Doença de Chagas, Febre Amarela
    
    ## 🎯 Medicamentos Regionalizados
    
    ### Adaptações Importantes:
    - **Resistência à Cloroquina** (Ásia): Artemeter + Mefloquina para malária
    - **Cepas resistentes** (África): Ceftriaxona para febre tifoide
    - **Dosagens pediátricas**: Específicas para cada região e doença
    - **Disponibilidade local**: Medicamentos acessíveis em cada região
    
    ## ⚠️ Doenças Críticas por Região
    
    ### 🚨 Emergências que requerem UTI:
    - **Global**: Cólera (desidratação), Meningite (neurológica)
    - **Brasil/África**: Febre Amarela (hepato-renal)
    - **África**: Leishmaniose Visceral (hematológica)
    - **Ásia**: Encefalite Japonesa (neurológica), Influenza Aviária (respiratória)
    
    ## 💻 Características Técnicas
    
    - **Execução offline**: Funciona sem internet
    - **Base regionalizada**: 37 doenças específicas por região
    - **Algoritmo adaptativo**: Considera prevalência epidemiológica
    - **Interface intuitiva**: Seleção de região automática
    - **Integração IoT**: Sensores de temperatura via MQTT
    - **Histórico regionalizado**: Análise epidemiológica por região
    
    ## 🔧 Uso em Campo
    
    ### 1. **Selecionar Região**: Norte do Brasil, África ou Ásia
    ### 2. **Coletar Dados**: Sintomas + sinais vitais + contexto
    ### 3. **Diagnóstico**: IA regional específica
    ### 4. **Tratamento**: Medicamentos e dosagens regionais
    ### 5. **Acompanhamento**: Recomendações específicas da região
    
    ---
    
    **Desenvolvido para apoiar profissionais de saúde em emergências globais** 🌍🏥
    
    *Versão 3.0 - Sistema Regionalizado com 37 Doenças Específicas*
    
    **Ideal para:**
    - Médicos Sem Fronteiras
    - Agências humanitárias internacionais  
    - Profissionais em desastres naturais
    - Sistemas de saúde em regiões endêmicas
    """)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "🏥 Sistema de IA para Triagem Médica em Áreas Vulneráveis | "
    "Desenvolvido para apoiar profissionais de saúde em regiões remotas"
    "</div>",
    unsafe_allow_html=True
) 