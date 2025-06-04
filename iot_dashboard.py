import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from iot_manager import IoTManager

class IoTDashboard:
    def __init__(self):
        self.iot_manager = IoTManager()
    
    def show_dashboard(self):
        """Exibe dashboard IoT completo"""
        try:
            st.title("🌡️ Dashboard IoT - Sensores de Temperatura")
            
            # Verificar se o IoT Manager está funcionando
            try:
                # Testar se consegue carregar dados básicos
                devices = self.iot_manager.get_all_devices()
                readings = self.iot_manager._load_readings()
                
                # Iniciar servidor API se não estiver rodando
                try:
                    server_started = self.iot_manager.start_api_server(5001)
                    if server_started:
                        st.success("✅ Servidor IoT iniciado na porta 5001")
                    else:
                        st.info("ℹ️ Servidor IoT já está ativo na porta 5001")
                except Exception as e:
                    st.warning(f"⚠️ Aviso: {str(e)}")
                    st.info("💡 Use o script `python start_iot_api.py` para iniciar a API manualmente")
                
            except Exception as e:
                st.error(f"❌ Erro ao acessar dados IoT: {str(e)}")
                st.info("🔄 Tentando recriar o IoT Manager...")
                
                # Tentar recriar o IoT Manager
                try:
                    self.iot_manager = IoTManager()
                    devices = self.iot_manager.get_all_devices()
                    readings = self.iot_manager._load_readings()
                    st.success("✅ IoT Manager recriado com sucesso")
                except Exception as e2:
                    st.error(f"❌ Falha ao recriar IoT Manager: {str(e2)}")
                    # Mostrar dashboard básico mesmo com erro
                    self._show_basic_dashboard()
                    return
            
            # Mostrar alertas se houver
            self._show_alerts()
            
            # Tabs do dashboard
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Monitoramento", 
                "🔧 Dispositivos", 
                "📈 Histórico", 
                "⚙️ Configurações"
            ])
            
            with tab1:
                self._show_monitoring()
            
            with tab2:
                self._show_devices()
            
            with tab3:
                self._show_history()
            
            with tab4:
                self._show_settings()
                
        except Exception as e:
            st.error("❌ Erro crítico no Dashboard IoT")
            st.error(f"Detalhes: {str(e)}")
            
            # Mostrar dashboard básico de emergência
            self._show_basic_dashboard()
    
    def _show_basic_dashboard(self):
        """Mostra dashboard básico quando há erros"""
        st.warning("⚠️ Dashboard IoT em modo básico devido a erros")
        
        st.subheader("📊 Informações do Sistema")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("🔧 **Status do Sistema**")
            st.write("• Dashboard: ✅ Ativo")
            st.write("• API IoT: ❓ Verificar manualmente")
            st.write("• Dados: ❓ Indisponível")
        
        with col2:
            st.info("🚀 **Como Resolver**")
            st.write("1. Execute: `python start_iot_api.py`")
            st.write("2. Verifique a porta 5001")
            st.write("3. Recarregue esta página")
        
        st.subheader("📋 Instruções de Uso")
        
        with st.expander("🔧 Iniciar API IoT Manualmente"):
            st.code("""
# No terminal, execute:
cd /Users/Fernando/FIAP/GS-2
python start_iot_api.py

# A API deve iniciar em:
# http://127.0.0.1:5001
            """)
        
        with st.expander("📱 Testar Conexão"):
            st.code("""
# Teste a API com curl:
curl http://127.0.0.1:5001/

# Envie dados de teste:
curl -X POST http://127.0.0.1:5001/api/sensor-data \\
  -H "Content-Type: application/json" \\
  -d '{"device_id": "TEST_001", "sensor_type": "temperature", "value": 36.5}'
            """)
        
        with st.expander("🌡️ Simular Dados"):
            if st.button("🧪 Criar Dados de Teste"):
                try:
                    # Tentar criar dados de teste
                    import json
                    import os
                    from datetime import datetime
                    
                    # Criar dispositivo de teste
                    test_device = {
                        "TEST_DEVICE_001": {
                            "name": "Sensor de Teste",
                            "type": "temperature_sensor",
                            "location": "Dashboard Teste",
                            "registered_at": datetime.now().isoformat(),
                            "last_seen": datetime.now().isoformat(),
                            "status": "online",
                            "battery_level": 85,
                            "firmware_version": "1.0.0"
                        }
                    }
                    
                    # Criar leituras de teste
                    test_readings = [
                        {
                            "device_id": "TEST_DEVICE_001",
                            "sensor_type": "temperature",
                            "value": 36.5,
                            "unit": "°C",
                            "location": "Dashboard Teste",
                            "battery_level": 85,
                            "timestamp": datetime.now().isoformat(),
                            "processed": False
                        }
                    ]
                    
                    # Salvar arquivos
                    with open('iot_devices.json', 'w') as f:
                        json.dump(test_device, f, indent=2)
                    
                    with open('iot_readings.json', 'w') as f:
                        json.dump(test_readings, f, indent=2)
                    
                    st.success("✅ Dados de teste criados!")
                    st.info("🔄 Recarregue a página para ver os dados")
                    
                except Exception as e:
                    st.error(f"❌ Erro ao criar dados de teste: {str(e)}")
        
        if st.button("🔄 Tentar Recarregar Dashboard"):
            st.rerun()
    
    def _show_alerts(self):
        """Mostra alertas IoT"""
        if 'iot_alerts' in st.session_state and st.session_state['iot_alerts']:
            # Mostrar apenas alertas dos últimos 30 minutos
            recent_alerts = []
            cutoff_time = datetime.now() - timedelta(minutes=30)
            
            for alert in st.session_state['iot_alerts']:
                alert_time = datetime.fromisoformat(alert['timestamp'])
                if alert_time > cutoff_time:
                    recent_alerts.append(alert)
            
            if recent_alerts:
                st.subheader("🚨 Alertas Recentes")
                
                for alert in recent_alerts[-5:]:  # Últimos 5 alertas
                    level = alert['level']
                    message = alert['message']
                    timestamp = datetime.fromisoformat(alert['timestamp']).strftime("%H:%M:%S")
                    
                    if level == 'CRITICAL':
                        st.error(f"🚨 **{timestamp}** - {message}")
                    elif level == 'HIGH':
                        st.warning(f"⚠️ **{timestamp}** - {message}")
                    else:
                        st.info(f"ℹ️ **{timestamp}** - {message}")
                
                st.divider()
    
    def _show_monitoring(self):
        """Mostra monitoramento em tempo real"""
        st.subheader("📡 Monitoramento em Tempo Real")
        
        # Botão para atualizar dados
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔄 Atualizar", use_container_width=True):
                st.rerun()
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        devices = self.iot_manager.get_all_devices()
        readings = self.iot_manager._load_readings()
        
        # Filtrar leituras das últimas 24h
        recent_readings = [
            r for r in readings 
            if datetime.fromisoformat(r['timestamp']) > datetime.now() - timedelta(hours=24)
        ]
        
        with col1:
            online_devices = len([d for d in devices.values() if d.get('status') == 'online'])
            st.metric("Dispositivos Online", f"{online_devices}/{len(devices)}")
        
        with col2:
            st.metric("Leituras (24h)", len(recent_readings))
        
        with col3:
            fever_count = len([r for r in recent_readings if r.get('value', 0) >= 37.8])
            st.metric("Casos de Febre", fever_count, delta=None if fever_count == 0 else f"+{fever_count}")
        
        with col4:
            if recent_readings:
                avg_temp = sum(r.get('value', 0) for r in recent_readings) / len(recent_readings)
                st.metric("Temp. Média", f"{avg_temp:.1f}°C")
            else:
                st.metric("Temp. Média", "N/A")
        
        # Gráfico em tempo real
        if recent_readings:
            st.subheader("📈 Temperaturas em Tempo Real")
            
            df = pd.DataFrame(recent_readings)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            fig = px.line(
                df, 
                x='timestamp', 
                y='value',
                color='device_id',
                title="Leituras das Últimas 24 Horas",
                labels={'value': 'Temperatura (°C)', 'timestamp': 'Horário'},
                height=400
            )
            
            # Adicionar linhas de referência
            fig.add_hline(y=37.8, line_dash="dash", line_color="orange", 
                         annotation_text="Limite Febre (37.8°C)")
            fig.add_hline(y=39.0, line_dash="dash", line_color="red", 
                         annotation_text="Crítico (39.0°C)")
            fig.add_hline(y=35.0, line_dash="dash", line_color="blue", 
                         annotation_text="Baixa (35.0°C)")
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Últimas leituras
            st.subheader("🕐 Últimas Leituras")
            
            latest_readings = sorted(recent_readings, key=lambda x: x['timestamp'], reverse=True)[:10]
            
            for reading in latest_readings:
                timestamp = datetime.fromisoformat(reading['timestamp']).strftime("%H:%M:%S")
                temp = reading['value']
                device_id = reading['device_id']
                status = self.iot_manager._get_temp_status(temp)
                
                col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
                with col1:
                    st.write(f"**{timestamp}**")
                with col2:
                    st.write(f"`{device_id}`")
                with col3:
                    st.write(f"**{temp}°C**")
                with col4:
                    st.write(status)
        else:
            st.info("📊 Aguardando dados dos sensores...")
            
            # Instruções para conectar dispositivos
            with st.expander("📱 Como conectar dispositivos"):
                st.markdown("""
                **Para conectar um sensor ESP32:**
                
                1. **Configure o código no Wokwi** com o endpoint:
                   ```
                   http://localhost:5001/api/sensor-data
                   ```
                
                2. **Registre o dispositivo** na aba "Dispositivos"
                
                3. **Envie dados** no formato JSON:
                   ```json
                   {
                     "device_id": "ESP32_TEMP_001",
                     "sensor_type": "temperature",
                     "value": 36.5,
                     "unit": "°C",
                     "location": "Recepção",
                     "battery_level": 85
                   }
                   ```
                """)
        
        # Status dos dispositivos
        if devices:
            st.subheader("🔌 Status dos Dispositivos")
            
            for device_id, device_info in devices.items():
                with st.expander(f"📱 {device_info['name']} ({device_id})"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        status_color = "🟢" if device_info.get('status') == 'online' else "🔴"
                        st.write(f"**Status:** {status_color} {device_info.get('status', 'unknown').title()}")
                        st.write(f"**Localização:** {device_info.get('location', 'N/A')}")
                        st.write(f"**Tipo:** {device_info.get('type', 'N/A')}")
                    
                    with col2:
                        last_seen = device_info.get('last_seen')
                        if last_seen:
                            last_seen_dt = datetime.fromisoformat(last_seen)
                            time_diff = datetime.now() - last_seen_dt
                            minutes_ago = time_diff.total_seconds() // 60
                            st.write(f"**Última comunicação:** {int(minutes_ago)} min atrás")
                        else:
                            st.write("**Última comunicação:** Nunca")
                        
                        # Bateria
                        battery = device_info.get('battery_level')
                        if battery is not None:
                            st.write(f"**Bateria:** {battery}%")
                        
                        # Última leitura
                        latest = self.iot_manager.get_latest_reading(device_id, 'temperature')
                        if latest:
                            temp = latest['value']
                            temp_status = self.iot_manager._get_temp_status(temp)
                            st.write(f"**Última temperatura:** {temp}°C {temp_status}")
    
    def _show_devices(self):
        """Mostra gerenciamento de dispositivos"""
        st.subheader("🔧 Gerenciamento de Dispositivos")
        
        # Registrar novo dispositivo
        with st.expander("➕ Registrar Novo Dispositivo", expanded=False):
            with st.form("register_device"):
                st.write("**Cadastrar Sensor de Temperatura**")
                
                device_id = st.text_input(
                    "ID do Dispositivo", 
                    placeholder="ESP32_TEMP_001",
                    help="Identificador único do dispositivo"
                )
                device_name = st.text_input(
                    "Nome do Dispositivo", 
                    placeholder="Sensor Recepção Principal",
                    help="Nome descritivo para identificação"
                )
                device_type = st.selectbox(
                    "Tipo", 
                    ["temperature_sensor", "multi_sensor", "gateway"],
                    help="Tipo de dispositivo IoT"
                )
                location = st.text_input(
                    "Localização", 
                    placeholder="Recepção - Posto 1",
                    help="Local onde o dispositivo está instalado"
                )
                
                if st.form_submit_button("📱 Registrar Dispositivo", use_container_width=True):
                    if device_id and device_name:
                        success = self.iot_manager.register_device(device_id, device_name, device_type, location)
                        if success:
                            st.success(f"✅ Dispositivo {device_id} registrado com sucesso!")
                            st.rerun()
                    else:
                        st.error("❌ Preencha pelo menos ID e Nome do dispositivo")
        
        # Lista de dispositivos
        devices = self.iot_manager.get_all_devices()
        
        if devices:
            st.subheader("📋 Dispositivos Registrados")
            
            for device_id, device_info in devices.items():
                with st.container():
                    col1, col2, col3 = st.columns([3, 3, 1])
                    
                    with col1:
                        status_icon = "🟢" if device_info.get('status') == 'online' else "🔴"
                        st.write(f"**{status_icon} {device_info['name']}**")
                        st.write(f"ID: `{device_id}`")
                    
                    with col2:
                        st.write(f"📍 {device_info.get('location', 'N/A')}")
                        st.write(f"🔧 {device_info.get('type', 'N/A')}")
                        
                        # Mostrar última leitura
                        latest = self.iot_manager.get_latest_reading(device_id, 'temperature')
                        if latest:
                            temp = latest['value']
                            status = self.iot_manager._get_temp_status(temp)
                            st.write(f"🌡️ {temp}°C {status}")
                    
                    with col3:
                        if st.button("🗑️", key=f"delete_{device_id}", help="Remover dispositivo"):
                            st.warning("⚠️ Funcionalidade em desenvolvimento")
                
                st.divider()
        else:
            st.info("📱 Nenhum dispositivo registrado ainda")
    
    def _show_history(self):
        """Mostra histórico de leituras"""
        st.subheader("📈 Histórico de Leituras")
        
        readings = self.iot_manager._load_readings()
        
        if readings:
            # Filtros
            col1, col2, col3 = st.columns(3)
            
            with col1:
                days_back = st.selectbox("Período", [1, 7, 30, 90], index=1)
            
            with col2:
                devices = list(set(r['device_id'] for r in readings))
                selected_device = st.selectbox("Dispositivo", ["Todos"] + devices)
            
            with col3:
                temp_filter = st.selectbox("Filtro Temperatura", ["Todas", "Normal", "Febre", "Crítico"])
            
            # Filtrar dados
            filtered_readings = []
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            for reading in readings:
                reading_date = datetime.fromisoformat(reading['timestamp'])
                
                if reading_date < cutoff_date:
                    continue
                
                if selected_device != "Todos" and reading['device_id'] != selected_device:
                    continue
                
                temp = reading.get('value', 0)
                if temp_filter == "Normal" and temp >= 37.8:
                    continue
                elif temp_filter == "Febre" and (temp < 37.8 or temp >= 39.0):
                    continue
                elif temp_filter == "Crítico" and temp < 39.0:
                    continue
                
                filtered_readings.append(reading)
            
            if filtered_readings:
                # Estatísticas
                temps = [r['value'] for r in filtered_readings]
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total de Leituras", len(filtered_readings))
                with col2:
                    st.metric("Temp. Mínima", f"{min(temps):.1f}°C")
                with col3:
                    st.metric("Temp. Máxima", f"{max(temps):.1f}°C")
                with col4:
                    st.metric("Temp. Média", f"{sum(temps)/len(temps):.1f}°C")
                
                # Gráfico histórico
                df = pd.DataFrame(filtered_readings)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                
                fig = px.scatter(
                    df,
                    x='timestamp',
                    y='value',
                    color='device_id',
                    title=f"Histórico de Temperaturas - Últimos {days_back} dias",
                    labels={'value': 'Temperatura (°C)', 'timestamp': 'Data/Hora'},
                    height=500
                )
                
                fig.add_hline(y=37.8, line_dash="dash", line_color="orange")
                fig.add_hline(y=39.0, line_dash="dash", line_color="red")
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Distribuição de temperaturas
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_hist = px.histogram(
                        df, 
                        x='value', 
                        title="Distribuição de Temperaturas",
                        labels={'value': 'Temperatura (°C)', 'count': 'Frequência'},
                        nbins=20
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                with col2:
                    # Contagem por status
                    df['status'] = df['value'].apply(self.iot_manager._get_temp_status)
                    status_counts = df['status'].value_counts()
                    
                    fig_pie = px.pie(
                        values=status_counts.values,
                        names=status_counts.index,
                        title="Distribuição por Status"
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                # Tabela de dados
                st.subheader("📋 Dados Detalhados")
                df_display = df[['timestamp', 'device_id', 'value', 'unit', 'location']].copy()
                df_display['status'] = df_display['value'].apply(self.iot_manager._get_temp_status)
                df_display = df_display.sort_values('timestamp', ascending=False)
                df_display['timestamp'] = df_display['timestamp'].dt.strftime('%d/%m/%Y %H:%M:%S')
                
                st.dataframe(df_display, use_container_width=True)
                
                # Botão para exportar dados
                if st.button("📥 Exportar Dados CSV"):
                    csv = df_display.to_csv(index=False)
                    st.download_button(
                        label="⬇️ Download CSV",
                        data=csv,
                        file_name=f"temperaturas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            else:
                st.info("📊 Nenhum dado encontrado para os filtros selecionados")
        else:
            st.info("📊 Nenhuma leitura disponível")
    
    def _show_settings(self):
        """Mostra configurações do sistema IoT"""
        st.subheader("⚙️ Configurações IoT")
        
        # Configurações de alertas
        st.write("🚨 **Configurações de Alertas**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fever_threshold = st.number_input("Limite para Febre (°C)", value=37.8, step=0.1)
            critical_threshold = st.number_input("Limite Crítico (°C)", value=39.0, step=0.1)
        
        with col2:
            low_temp_threshold = st.number_input("Limite Baixo (°C)", value=35.0, step=0.1)
            reading_interval = st.number_input("Intervalo de Leitura (segundos)", value=30, step=5)
        
        # Configurações de conectividade
        st.write("🌐 **Configurações de Conectividade**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            api_port = st.number_input("Porta da API", value=5000, step=1)
            max_readings = st.number_input("Máximo de Leituras Armazenadas", value=1000, step=100)
        
        with col2:
            device_timeout = st.number_input("Timeout de Dispositivo (minutos)", value=10, step=1)
        
        if st.button("💾 Salvar Configurações", use_container_width=True):
            st.success("✅ Configurações salvas com sucesso!")
        
        # Informações do sistema
        st.write("ℹ️ **Informações do Sistema**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"**Servidor API:** http://localhost:5001")
            st.info(f"**Endpoint:** /api/sensor-data")
            st.info(f"**Health Check:** /api/health")
        
        with col2:
            st.info(f"**Método:** POST")
            st.info(f"**Formato:** JSON")
            st.info(f"**Content-Type:** application/json")
        
        # Exemplo de payload
        st.write("📝 **Exemplo de Payload JSON:**")
        
        example_payload = {
            "device_id": "ESP32_TEMP_001",
            "sensor_type": "temperature",
            "value": 36.5,
            "unit": "°C",
            "location": "Recepção - Posto 1",
            "battery_level": 85,
            "firmware_version": "1.0.0"
        }
        
        st.code(json.dumps(example_payload, indent=2), language='json')
        
        # Teste de conectividade
        st.write("🔧 **Teste de Conectividade**")
        
        if st.button("🧪 Simular Leitura de Teste"):
            import random
            test_temp = round(random.uniform(35.5, 39.5), 1)
            
            test_reading = self.iot_manager.receive_sensor_data(
                device_id="TEST_DEVICE",
                sensor_type="temperature",
                value=test_temp,
                unit="°C",
                location="Teste",
                battery_level=random.randint(70, 100)
            )
            
            st.success(f"✅ Leitura de teste criada: {test_temp}°C")
            st.json(test_reading)
    
    def get_latest_temperature_for_triagem(self):
        """Obtém última temperatura para integração com triagem"""
        return self.iot_manager.get_latest_temperature_for_triagem() 