import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from triagem_model import TriagemMedica
from auth import AuthManager
from security import SecurityManager
from iot_dashboard import IoTDashboard
import os
import json

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
    return IoTDashboard()

triagem = carregar_modelo()
auth = carregar_auth()
security = carregar_security()
iot_dashboard = carregar_iot()

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
paginas_disponiveis.append("ℹ️ Sobre o Sistema")

pagina = st.sidebar.selectbox(
    "Selecione uma opção:",
    paginas_disponiveis
)

if pagina == "🩺 Triagem Médica":
    auth.require_permission('triagem')
    st.header("🩺 Formulário de Triagem Médica")
    
    # Verificar se há temperatura disponível do IoT (FORA do formulário)
    latest_temp = iot_dashboard.get_latest_temperature_for_triagem()
    temperatura_iot = None
    
    if latest_temp:
        st.success(f"🌡️ **Temperatura detectada automaticamente:** {latest_temp['temperature']}°C "
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
        st.info("💡 **Dica:** Conecte um sensor IoT para medição automática de temperatura")
        st.divider()
    
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
            
            pressao_sistolica = st.number_input("Pressão Sistólica (mmHg)", min_value=50, max_value=250, value=120)
            pressao_diastolica = st.number_input("Pressão Diastólica (mmHg)", min_value=30, max_value=150, value=80)
            frequencia_cardiaca = st.number_input("Frequência Cardíaca (bpm)", min_value=30, max_value=200, value=70)
        
        with col2:
            st.subheader("🤒 Sintomas Apresentados")
            sintomas_opcoes = [
                "febre", "febre_baixa", "febre_alta", "febre_prolongada", "dor_cabeca", "dor_cabeca_intensa", 
                "dor_muscular", "dor_articular", "dor_articular_intensa", "nausea", "vomito",
                "diarreia", "tosse", "tosse_seca", "tosse_persistente", "dificuldade_respirar", "dor_peito",
                "calafrios", "sudorese", "sudorese_noturna", "fadiga", "manchas_pele", "conjuntivite",
                "dor_abdominal", "desidratacao", "convulsoes", "ictericia", "sangue_fezes", "urina_escura",
                "expectoracao", "expectoracao_sangue", "perda_peso", "perda_olfato", "perda_paladar",
                "rigidez_nuca", "confusao_mental", "aumento_baço", "aumento_figado", "anemia",
                "dor_retro_orbital", "hemorragia", "oliguria"
            ]
            
            sintomas_labels = {
                "febre": "Febre",
                "febre_baixa": "Febre baixa (até 38°C)",
                "febre_alta": "Febre alta (>39°C)",
                "febre_prolongada": "Febre prolongada (>7 dias)",
                "dor_cabeca": "Dor de cabeça",
                "dor_cabeca_intensa": "Dor de cabeça intensa",
                "dor_muscular": "Dor muscular",
                "dor_articular": "Dor articular",
                "dor_articular_intensa": "Dor articular intensa",
                "nausea": "Náusea",
                "vomito": "Vômito",
                "diarreia": "Diarreia",
                "tosse": "Tosse",
                "tosse_seca": "Tosse seca",
                "tosse_persistente": "Tosse persistente (>3 semanas)",
                "dificuldade_respirar": "Dificuldade para respirar",
                "dor_peito": "Dor no peito",
                "calafrios": "Calafrios",
                "sudorese": "Sudorese",
                "sudorese_noturna": "Sudorese noturna",
                "fadiga": "Fadiga/Cansaço",
                "manchas_pele": "Manchas na pele",
                "conjuntivite": "Conjuntivite",
                "dor_abdominal": "Dor abdominal",
                "desidratacao": "Desidratação",
                "convulsoes": "Convulsões",
                "ictericia": "Icterícia (amarelão)",
                "sangue_fezes": "Sangue nas fezes",
                "urina_escura": "Urina escura",
                "expectoracao": "Expectoração",
                "expectoracao_sangue": "Expectoração com sangue",
                "perda_peso": "Perda de peso",
                "perda_olfato": "Perda do olfato",
                "perda_paladar": "Perda do paladar",
                "rigidez_nuca": "Rigidez na nuca",
                "confusao_mental": "Confusão mental",
                "aumento_baço": "Aumento do baço",
                "aumento_figado": "Aumento do fígado",
                "anemia": "Anemia",
                "dor_retro_orbital": "Dor atrás dos olhos",
                "hemorragia": "Hemorragia",
                "oliguria": "Diminuição da urina"
            }
            
            sintomas_selecionados = []
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
                'sintomas': sintomas_selecionados,
                'evento_climatico': evento_climatico,
                'tempo_sintomas': tempo_sintomas,
                'historico_medico': historico_medico,
                'populacao_vulneravel': populacao_vulneravel != "Não"
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

elif pagina == "ℹ️ Sobre o Sistema":
    st.header("ℹ️ Sobre o Sistema de Triagem Médica")
    
    st.markdown("""
    ## 🎯 Objetivo
    
    Este sistema foi desenvolvido para apoiar profissionais de saúde em áreas vulneráveis, especialmente em contextos de:
    - **Desastres naturais**
    - **Regiões remotas**
    - **Crises humanitárias**
    - **Médicos Sem Fronteiras**
    
    ## 🧠 Como Funciona
    
    O sistema utiliza um modelo de IA que considera:
    
    ### 4 Fatores de Análise (Nova Fórmula Aprimorada)
    - **Sintomas clínicos** (peso: 45%)
    - **Eventos climáticos** (peso: 25%)
    - **População de risco** (peso: 15%)
    - **Gravidade da doença** (peso: 15%)
    
    ### 🌦️ Eventos Climáticos Monitorados
    - **Enchentes/Chuvas intensas**: Leptospirose, Hepatite A, Dengue, Diarreia, Esquistossomose
    - **Ondas de calor**: Infecções respiratórias, Diarreias, Dermatites
    - **Secas prolongadas**: Desnutrição, Diarreia, Meningite, Leishmaniose
    - **Calor + umidade**: Malária, Dengue, Zika, Febre amarela, Chikungunya
    - **Aglomeração**: COVID-19, Tuberculose, Meningite
    - **Áreas rurais**: Doença de Chagas, Leishmaniose, Febre amarela
    
    ### 🏥 Doenças Contempladas (15 condições)
    
    | Doença | Incidência | Gravidade | Medicação Principal |
    |--------|------------|-----------|-------------------|
    | **Arboviroses** | | | |
    | Dengue | até 20% | Alta | Paracetamol + Hidratação |
    | Zika | até 10% | Baixa | Paracetamol + Hidratação |
    | Chikungunya | até 15% | Média | Paracetamol + Anti-inflamatório |
    | Febre Amarela | até 1% | **Crítica** | Suporte clínico |
    | **Doenças Transmitidas por Água** | | | |
    | Leptospirose | até 2% | Alta | Doxiciclina/Amoxicilina |
    | Diarreia Infecciosa | 5-15% | Média | Sais de reidratação + Zinco |
    | Hepatite A | até 8% | Média | Suporte clínico + Repouso |
    | Esquistossomose | até 6% | Média | Praziquantel |
    | **Doenças Respiratórias** | | | |
    | Infecção Respiratória | 10-30% | Média | Amoxicilina/Azitromicina |
    | Tuberculose | até 5% | Alta | RIPE (4 drogas) |
    | COVID-19 | até 25% | Alta | Suporte clínico + Isolamento |
    | **Doenças Parasitárias** | | | |
    | Malária | 2-5% | Alta | Cloroquina/Artesunato |
    | Leishmaniose Visceral | até 2% | **Crítica** | Anfotericina B |
    | Doença de Chagas | até 3% | Alta | Benznidazol |
    | **Emergências** | | | |
    | Meningite Bacteriana | até 1% | **Crítica** | Ceftriaxona EV |
    
    ## 🆕 Melhorias Implementadas
    
    ### ✅ Diagnóstico Mais Assertivo
    - **Sintomas específicos**: Bonus para sintomas patognomônicos
    - **Diagnósticos diferenciais**: Top 3 possibilidades alternativas
    - **Score detalhado**: Transparência no processo de decisão
    - **Penalização**: Redução de score para sintomas não relacionados
    
    ### ✅ Segurança Médica Aprimorada
    - **Verificação de febre**: Temperatura ≥38°C sempre adiciona "febre" aos sintomas
    - **Detecção rigorosa de paciente saudável**: Apenas com sinais vitais completamente normais
    - **Classificação de urgência**: Baseada em sinais vitais e sintomas graves
    
    ### ✅ Contexto Epidemiológico
    - **15 doenças** relevantes para áreas vulneráveis
    - **Eventos climáticos expandidos**: 16 tipos de contextos ambientais
    - **Histórico médico detalhado**: 14 condições de risco
    - **População específica**: Gestantes, lactantes, imunodeprimidos
    
    ## ⚠️ Importante
    
    - Este sistema é uma **ferramenta de apoio** ao diagnóstico
    - **NÃO substitui** a avaliação médica profissional
    - Sempre considere o contexto clínico completo
    - Em casos de urgência, procure atendimento médico imediato
    - **Casos críticos** (Febre amarela, Leishmaniose, Meningite) requerem encaminhamento URGENTE
    
    ## 🔧 Características Técnicas
    
    - **Execução offline**: Funciona sem internet
    - **Interface intuitiva**: Fácil uso em campo
    - **Histórico completo**: Rastreamento de atendimentos
    - **Estatísticas epidemiológicas**: Análise de tendências
    - **40+ sintomas**: Cobertura abrangente de manifestações clínicas
    - **Algoritmo ponderado**: Fórmula otimizada para precisão
    
    ---
    
    **Desenvolvido para apoiar a saúde em áreas vulneráveis** 🌍❤️
    
    *Versão 2.0 - Sistema Expandido com 15 Doenças e Diagnóstico Assertivo*
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