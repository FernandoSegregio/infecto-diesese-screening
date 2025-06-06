import json
import paho.mqtt.client as mqtt
import threading
import time
import ssl
import os
from datetime import datetime, timedelta
from .iot_manager import IoTManager
import streamlit as st

class MQTTManager:
    def __init__(self, broker_host="91c5f1ea0f494ccebe45208ea8ffceff.s1.eu.hivemq.cloud", 
                 broker_port=8883, username="FARM_TECH", password="Pato1234"):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.username = username
        self.password = password
        self.client = None
        self.connected = False
        self.iot_manager = IoTManager()
        self.running = False
        self.is_docker = self._detect_docker_environment()
        
        # Tópicos MQTT do termômetro ESP32
        self.topics = {
            'temperature': 'termometro/temperatura',
            'status': 'termometro/status',
            'alert': 'termometro/alerta',
            'device': 'termometro/device',
            'command': 'termometro/comando'  # Novo tópico para comandos
        }
        
        # Log de ambiente
        if self.is_docker:
            print("🐳 MQTT Manager rodando no Docker")
        else:
            print("💻 MQTT Manager rodando localmente")
    
    def _detect_docker_environment(self):
        """Detecta se está rodando dentro do Docker"""
        try:
            # Verifica se existe o arquivo .dockerenv
            if os.path.exists('/.dockerenv'):
                return True
            
            # Verifica se está no cgroup do Docker
            with open('/proc/1/cgroup', 'r') as f:
                return 'docker' in f.read()
        except:
            return False
    
    def on_connect(self, client, userdata, flags, rc):
        """Callback quando conecta ao broker MQTT"""
        if rc == 0:
            print("✅ Conectado ao broker HiveMQ Cloud")
            if self.is_docker:
                print("🐳 Conexão MQTT estabelecida dentro do container Docker")
            self.connected = True
            
            # Subscrever aos tópicos do termômetro
            for topic_name, topic in self.topics.items():
                client.subscribe(topic)
                print(f"📡 Subscrito ao tópico: {topic}")
                
        else:
            print(f"❌ Falha na conexão MQTT. Código: {rc}")
            print("💡 Códigos de erro:")
            print("   1: Versão de protocolo incorreta")
            print("   2: Identificador de cliente inválido")
            print("   3: Servidor indisponível")
            print("   4: Usuário/senha incorretos")
            print("   5: Não autorizado")
            
            if self.is_docker:
                print("🐳 Erro de conexão no ambiente Docker - verificar:")
                print("   • Conectividade de rede do container")
                print("   • Resolução DNS")
                print("   • Portas expostas")
            
            self.connected = False
    
    def on_disconnect(self, client, userdata, rc):
        """Callback quando desconecta do broker"""
        print("⚠️ Desconectado do broker MQTT")
        if self.is_docker:
            print("🐳 Desconexão MQTT no container Docker")
        self.connected = False
    
    def on_message(self, client, userdata, msg):
        """Callback quando recebe uma mensagem"""
        try:
            topic = msg.topic
            payload_str = msg.payload.decode()
            payload = json.loads(payload_str)
            
            print(f"📨 Mensagem MQTT recebida:")
            print(f"   Tópico: {topic}")
            print(f"   Payload: {payload}")
            
            if self.is_docker:
                print(f"🐳 Processando mensagem no container Docker")
            
            # Processar baseado no tópico
            if topic == self.topics['temperature']:
                self._process_temperature_data(payload)
            elif topic == self.topics['status']:
                self._process_status_data(payload)
            elif topic == self.topics['alert']:
                self._process_alert_data(payload)
            elif topic == self.topics['device']:
                self._process_device_data(payload)
                    
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao decodificar JSON: {str(e)}")
            print(f"   Payload raw: {msg.payload.decode()}")
        except Exception as e:
            print(f"❌ Erro ao processar mensagem MQTT: {str(e)}")
    
    def _process_temperature_data(self, payload):
        """Processa dados de temperatura do termômetro"""
        try:
            device_id = payload.get('device_id', 'ESP32_TERMOMETRO_001')
            temperature = payload.get('value')
            unit = payload.get('unit', '°C')
            location = payload.get('location', 'ESP32 Sensor')
            battery_level = payload.get('battery_level')
            
            if temperature is not None:
                # Salvar leitura usando o IoTManager
                reading = self.iot_manager.receive_sensor_data(
                    device_id=device_id,
                    sensor_type='temperature',
                    value=float(temperature),
                    unit=unit,
                    location=location,
                    battery_level=battery_level,
                    firmware_version="2.0.0"
                )
                
                print(f"🌡️ Temperatura processada: {temperature}{unit} de {device_id}")
                print(f"📍 Local: {location}")
                
                if self.is_docker:
                    print(f"🐳 Dados salvos no container: /app/{self.iot_manager.readings_file}")
                
                # Determinar status da temperatura
                temp_status = self._get_temperature_status(float(temperature))
                print(f"📊 Status: {temp_status}")
                
        except Exception as e:
            print(f"❌ Erro ao processar temperatura: {str(e)}")
    
    def _process_status_data(self, payload):
        """Processa dados de status do termômetro"""
        try:
            device_id = payload.get('device_id')
            status = payload.get('status')
            temperature = payload.get('temperature')
            location = payload.get('location')
            
            print(f"📊 Status do termômetro {device_id}:")
            print(f"   Status: {status}")
            print(f"   Temperatura: {temperature}°C")
            print(f"   Local: {location}")
            
        except Exception as e:
            print(f"❌ Erro ao processar status: {str(e)}")
    
    def _process_alert_data(self, payload):
        """Processa alertas do termômetro"""
        try:
            device_id = payload.get('device_id')
            alert_type = payload.get('alert_type')
            temperature = payload.get('temperature')
            location = payload.get('location')
            priority = payload.get('priority', 'MEDIUM')
            
            print(f"🚨 ALERTA RECEBIDO:")
            print(f"   Dispositivo: {device_id}")
            print(f"   Tipo: {alert_type}")
            print(f"   Temperatura: {temperature}°C")
            print(f"   Local: {location}")
            print(f"   Prioridade: {priority}")
            
            if self.is_docker:
                print(f"🐳 Alerta processado no container Docker")
            
            # Salvar alerta no sistema
            self._save_alert(device_id, alert_type, temperature, location, priority)
            
        except Exception as e:
            print(f"❌ Erro ao processar alerta: {str(e)}")
    
    def _process_device_data(self, payload):
        """Processa dados do dispositivo (registro, startup)"""
        try:
            device_id = payload.get('device_id')
            action = payload.get('action')
            location = payload.get('location')
            firmware = payload.get('firmware')
            ip = payload.get('ip')
            
            if action == 'startup':
                print(f"📱 Dispositivo iniciado:")
                print(f"   ID: {device_id}")
                print(f"   Local: {location}")
                print(f"   Firmware: {firmware}")
                print(f"   IP: {ip}")
                
                if self.is_docker:
                    print(f"🐳 Dispositivo conectado ao sistema Docker")
                
                # Auto-registrar dispositivo
                success = self.iot_manager.register_device(
                    device_id=device_id,
                    device_name=f"Termômetro {device_id}",
                    device_type='temperature',
                    location=location or "Termômetro ESP32"
                )
                
                if success:
                    print(f"✅ Dispositivo {device_id} registrado automaticamente")
                
        except Exception as e:
            print(f"❌ Erro ao processar dados do dispositivo: {str(e)}")
    
    def _get_temperature_status(self, temp):
        """Retorna status baseado na temperatura"""
        if temp >= 39.0:
            return "🔴 CRÍTICO"
        elif temp >= 37.8:
            return "🟡 FEBRE" 
        elif temp <= 35.0:
            return "🔵 BAIXA"
        else:
            return "🟢 NORMAL"
    
    def _save_alert(self, device_id, alert_type, temperature, location, priority):
        """Salva alerta no sistema"""
        try:
            # Salvar no session state do Streamlit se disponível
            alert = {
                'device_id': device_id,
                'alert_type': alert_type,
                'temperature': temperature,
                'location': location,
                'priority': priority,
                'timestamp': datetime.now().isoformat()
            }
            
            if 'iot_alerts' not in st.session_state:
                st.session_state['iot_alerts'] = []
            
            st.session_state['iot_alerts'].append(alert)
            
            # Manter apenas últimos 50 alertas
            if len(st.session_state['iot_alerts']) > 50:
                st.session_state['iot_alerts'] = st.session_state['iot_alerts'][-50:]
                
        except Exception:
            # Se não estiver no contexto do Streamlit, apenas log
            pass
    
    def start(self):
        """Inicia o cliente MQTT"""
        try:
            # Criar cliente MQTT com ID único
            client_id = f"TriagemMedica_Docker_{int(time.time())}" if self.is_docker else f"TriagemMedica_{int(time.time())}"
            self.client = mqtt.Client(client_id)
            
            print(f"🔧 Cliente MQTT ID: {client_id}")
            
            # Configurar credenciais
            self.client.username_pw_set(self.username, self.password)
            
            # Configurar TLS/SSL para HiveMQ Cloud
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            self.client.tls_set_context(context)
            
            # Configurar callbacks
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_message = self.on_message
            
            print(f"🔄 Conectando ao HiveMQ Cloud: {self.broker_host}:{self.broker_port}")
            print(f"👤 Usuário: {self.username}")
            
            if self.is_docker:
                print(f"🐳 Iniciando conexão MQTT do container Docker")
                print(f"🌐 Testando conectividade de rede...")
                # Teste básico de conectividade DNS
                import socket
                try:
                    socket.gethostbyname(self.broker_host)
                    print(f"✅ DNS resolvido: {self.broker_host}")
                except socket.gaierror as e:
                    print(f"❌ Erro de DNS: {e}")
                    return False
            
            # Conectar ao broker
            self.client.connect(self.broker_host, self.broker_port, 60)
            
            # Iniciar loop em thread separada
            self.running = True
            mqtt_thread = threading.Thread(target=self._mqtt_loop)
            mqtt_thread.daemon = True
            mqtt_thread.start()
            
            print(f"🚀 Thread MQTT iniciada (daemon=True)")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao iniciar MQTT: {str(e)}")
            if self.is_docker:
                print(f"🐳 Erro específico do Docker - verificar:")
                print(f"   • Network: bridge/host")
                print(f"   • Porta 8883 liberada")
                print(f"   • Resolução DNS")
            return False
    
    def _mqtt_loop(self):
        """Loop MQTT em thread separada"""
        try:
            print(f"🔄 Iniciando loop MQTT...")
            self.client.loop_forever()
        except Exception as e:
            print(f"❌ Erro no loop MQTT: {str(e)}")
            self.running = False
    
    def stop(self):
        """Para o cliente MQTT"""
        self.running = False
        if self.client:
            self.client.disconnect()
            print("🛑 Cliente MQTT parado")
    
    def publish_test_message(self, device_id="ESP32_TERMOMETRO_TEST"):
        """Publica mensagem de teste no formato do termômetro"""
        try:
            # Teste de temperatura
            test_temp_data = {
                'device_id': device_id,
                'sensor_type': 'temperature',
                'value': 37.2,
                'unit': '°C',
                'location': 'Teste Sistema Docker' if self.is_docker else 'Teste Sistema',
                'battery_level': 85,
                'timestamp': int(time.time() * 1000)
            }
            
            self.client.publish(self.topics['temperature'], json.dumps(test_temp_data))
            print(f"✅ Teste de temperatura enviado: {test_temp_data}")
            
            # Teste de status
            test_status_data = {
                'device_id': device_id,
                'status': 'NORMAL',
                'temperature': 37.2,
                'location': 'Teste Sistema Docker' if self.is_docker else 'Teste Sistema',
                'timestamp': int(time.time() * 1000)
            }
            
            self.client.publish(self.topics['status'], json.dumps(test_status_data))
            print(f"✅ Teste de status enviado: {test_status_data}")
            
        except Exception as e:
            print(f"❌ Erro ao enviar teste: {str(e)}")
    
    def publish_command(self, command, device_id=None, target_device="ESP32_TERMOMETRO_001"):
        """Envia comando MQTT para ESP32"""
        try:
            if not self.connected:
                print("❌ MQTT não conectado - não é possível enviar comando")
                return False
            
            command_data = {
                'command': command,
                'device_id': device_id or target_device,
                'timestamp': int(time.time() * 1000),
                'source': 'TriagemMedica_Dashboard'
            }
            
            # Adicionar parâmetros específicos baseado no comando
            if command == 'measure_temperature':
                command_data['action'] = 'start_reading'
                command_data['priority'] = 'high'
                print(f"📤 Enviando comando para medir temperatura no {target_device}")
            elif command == 'get_status':
                command_data['action'] = 'status_report'
                print(f"📤 Solicitando status do {target_device}")
            elif command == 'test_leds':
                command_data['action'] = 'test_hardware'
                print(f"📤 Testando LEDs do {target_device}")
            
            payload = json.dumps(command_data)
            result = self.client.publish(self.topics['command'], payload)
            
            if result.rc == 0:
                print(f"✅ Comando '{command}' enviado com sucesso!")
                print(f"   Payload: {payload}")
                
                if self.is_docker:
                    print(f"🐳 Comando enviado do container Docker")
                
                # Adicionar ao histórico de comandos no Streamlit
                self._add_command_to_history(command, target_device)
                
                return True
            else:
                print(f"❌ Falha ao enviar comando. Código: {result.rc}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar comando MQTT: {str(e)}")
            return False
    
    def _add_command_to_history(self, command, device_id):
        """Adiciona comando ao histórico do Streamlit"""
        try:
            if 'mqtt_command_history' not in st.session_state:
                st.session_state['mqtt_command_history'] = []
            
            command_entry = f"{datetime.now().strftime('%H:%M:%S')} - {command} → {device_id}"
            st.session_state['mqtt_command_history'].append(command_entry)
            
            # Manter apenas últimos 20 comandos
            if len(st.session_state['mqtt_command_history']) > 20:
                st.session_state['mqtt_command_history'] = st.session_state['mqtt_command_history'][-20:]
                
        except Exception:
            # Se não estiver no contexto do Streamlit, apenas ignora
            pass
    
    def request_temperature_reading(self, device_id="ESP32_TERMOMETRO_001"):
        """Solicita leitura de temperatura imediata"""
        print(f"📤 Enviando comando para medir temperatura no {device_id}")
        success = self.publish_command("measure_temperature", device_id, device_id)
        
        if success:
            self._add_command_to_history(f"📏 Medição de temperatura solicitada para {device_id}", device_id)
        
        return success
    
    def request_device_status(self, device_id="ESP32_TERMOMETRO_001"):
        """Solicita status do dispositivo via MQTT"""
        print(f"📊 Solicitando status do dispositivo {device_id}")
        return self.publish_command('get_status', target_device=device_id)
    
    def test_device_hardware(self, device_id="ESP32_TERMOMETRO_001"):
        """Testa hardware do dispositivo (LEDs, buzzer) via MQTT"""
        print(f"🔧 Testando hardware do dispositivo {device_id}")
        return self.publish_command('test_leds', target_device=device_id)
    
    def get_connection_status(self):
        """Retorna status da conexão"""
        return {
            'connected': self.connected,
            'broker': f"{self.broker_host}:{self.broker_port}",
            'username': self.username,
            'topics': self.topics,
            'running': self.running,
            'docker': self.is_docker,
            'client_id': getattr(self.client, '_client_id', 'N/A') if self.client else 'N/A',
            'command_topic': self.topics['command']  # Incluir tópico de comando no status
        }
    
    def get_latest_readings(self):
        """Obtém últimas leituras via IoTManager"""
        return self.iot_manager._load_readings()
    
    def get_devices(self):
        """Obtém dispositivos registrados"""
        return self.iot_manager.get_all_devices() 