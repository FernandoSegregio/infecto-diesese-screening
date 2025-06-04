import json
import os
import requests
from datetime import datetime, timedelta
import streamlit as st
from flask import Flask, request, jsonify
import threading
import time

class IoTManager:
    def __init__(self):
        self.devices_file = 'iot_devices.json'
        self.readings_file = 'iot_readings.json'
        self.flask_app = None
        self.flask_thread = None
        self._init_files()
    
    def _init_files(self):
        """Inicializa arquivos de dados IoT"""
        if not os.path.exists(self.devices_file):
            with open(self.devices_file, 'w') as f:
                json.dump({}, f, indent=2)
        
        if not os.path.exists(self.readings_file):
            with open(self.readings_file, 'w') as f:
                json.dump([], f, indent=2)
    
    def register_device(self, device_id, device_name, device_type, location):
        """Registra um novo dispositivo IoT"""
        devices = self._load_devices()
        
        devices[device_id] = {
            'name': device_name,
            'type': device_type,
            'location': location,
            'registered_at': datetime.now().isoformat(),
            'last_seen': None,
            'status': 'offline',
            'battery_level': None,
            'firmware_version': None
        }
        
        self._save_devices(devices)
        return True
    
    def _load_devices(self):
        """Carrega dispositivos registrados"""
        try:
            with open(self.devices_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_devices(self, devices):
        """Salva dispositivos"""
        with open(self.devices_file, 'w') as f:
            json.dump(devices, f, indent=2)
    
    def _load_readings(self):
        """Carrega leituras dos sensores"""
        try:
            with open(self.readings_file, 'r') as f:
                return json.load(f)
        except:
            return []
    
    def _save_readings(self, readings):
        """Salva leituras dos sensores"""
        with open(self.readings_file, 'w') as f:
            json.dump(readings, f, indent=2)
    
    def receive_sensor_data(self, device_id, sensor_type, value, unit='°C', location=None, battery_level=None, firmware_version=None):
        """Recebe dados de sensores"""
        readings = self._load_readings()
        devices = self._load_devices()
        
        # Atualizar status do dispositivo
        if device_id in devices:
            devices[device_id]['last_seen'] = datetime.now().isoformat()
            devices[device_id]['status'] = 'online'
            if battery_level is not None:
                devices[device_id]['battery_level'] = battery_level
            if firmware_version is not None:
                devices[device_id]['firmware_version'] = firmware_version
            self._save_devices(devices)
        
        # Salvar leitura
        reading = {
            'device_id': device_id,
            'sensor_type': sensor_type,
            'value': float(value),
            'unit': unit,
            'location': location,
            'battery_level': battery_level,
            'timestamp': datetime.now().isoformat(),
            'processed': False
        }
        
        readings.append(reading)
        
        # Manter apenas últimas 1000 leituras
        if len(readings) > 1000:
            readings = readings[-1000:]
        
        self._save_readings(readings)
        
        # Verificar alertas
        self._check_alerts(reading)
        
        return reading
    
    def _check_alerts(self, reading):
        """Verifica se a leitura requer alertas"""
        if reading['sensor_type'] == 'temperature' and reading['unit'] == '°C':
            temp = reading['value']
            device_id = reading['device_id']
            
            if temp >= 39.0:
                self._send_alert('CRITICAL', f"🚨 Temperatura crítica detectada: {temp}°C no dispositivo {device_id}", reading)
            elif temp >= 37.8:
                self._send_alert('HIGH', f"⚠️ Febre detectada: {temp}°C no dispositivo {device_id}", reading)
            elif temp <= 35.0:
                self._send_alert('LOW', f"🔵 Temperatura baixa detectada: {temp}°C no dispositivo {device_id}", reading)
    
    def _send_alert(self, level, message, reading):
        """Envia alertas"""
        alert = {
            'level': level,
            'message': message,
            'reading': reading,
            'timestamp': datetime.now().isoformat()
        }
        
        # Salvar alerta no session state para exibir no Streamlit (se disponível)
        try:
            if 'iot_alerts' not in st.session_state:
                st.session_state['iot_alerts'] = []
            
            st.session_state['iot_alerts'].append(alert)
            
            # Manter apenas últimos 50 alertas
            if len(st.session_state['iot_alerts']) > 50:
                st.session_state['iot_alerts'] = st.session_state['iot_alerts'][-50:]
        except Exception:
            # Se não estiver no contexto do Streamlit, apenas imprimir
            pass
        
        print(f"🚨 ALERTA {level}: {message}")
    
    def get_latest_reading(self, device_id, sensor_type):
        """Obtém a leitura mais recente de um sensor"""
        readings = self._load_readings()
        
        device_readings = [
            r for r in readings 
            if r['device_id'] == device_id and r['sensor_type'] == sensor_type
        ]
        
        if device_readings:
            return sorted(device_readings, key=lambda x: x['timestamp'])[-1]
        return None
    
    def get_device_status(self, device_id):
        """Obtém status de um dispositivo"""
        devices = self._load_devices()
        return devices.get(device_id, None)
    
    def get_all_devices(self):
        """Obtém todos os dispositivos"""
        return self._load_devices()
    
    def get_latest_temperature_for_triagem(self):
        """Obtém última temperatura para integração com triagem"""
        readings = self._load_readings()
        
        if readings:
            # Filtrar apenas leituras de temperatura dos últimos 5 minutos
            recent_readings = []
            cutoff_time = datetime.now() - timedelta(minutes=5)
            
            for reading in readings:
                if reading['sensor_type'] == 'temperature':
                    reading_time = datetime.fromisoformat(reading['timestamp'])
                    if reading_time > cutoff_time:
                        recent_readings.append(reading)
            
            if recent_readings:
                # Pegar a mais recente
                latest = sorted(recent_readings, key=lambda x: x['timestamp'])[-1]
                
                return {
                    'temperature': latest['value'],
                    'device_id': latest['device_id'],
                    'timestamp': latest['timestamp'],
                    'location': latest.get('location', 'N/A'),
                    'status': self._get_temp_status(latest['value'])
                }
        
        return None
    
    def _get_temp_status(self, temp):
        """Retorna status baseado na temperatura"""
        if temp >= 39.0:
            return "🔴 Crítico"
        elif temp >= 37.8:
            return "🟡 Febre"
        elif temp <= 35.0:
            return "🔵 Baixa"
        else:
            return "🟢 Normal"
    
    def start_api_server(self, port=5001):
        """Inicia servidor Flask para receber dados IoT"""
        if self.flask_app is None:
            self.flask_app = Flask(__name__)
            
            @self.flask_app.route('/', methods=['GET'])
            def home():
                return jsonify({
                    'message': 'Sistema IoT - API de Sensores',
                    'version': '1.0.0',
                    'status': 'online',
                    'timestamp': datetime.now().isoformat(),
                    'endpoints': {
                        'POST /api/sensor-data': 'Receber dados de sensores',
                        'GET /api/device-status/<device_id>': 'Status do dispositivo',
                        'GET /api/health': 'Health check da API'
                    },
                    'devices_count': len(self.get_all_devices()),
                    'readings_count': len(self._load_readings())
                })
            
            @self.flask_app.route('/api/sensor-data', methods=['POST'])
            def receive_data():
                try:
                    data = request.json
                    device_id = data.get('device_id')
                    sensor_type = data.get('sensor_type')
                    value = data.get('value')
                    unit = data.get('unit', '°C')
                    location = data.get('location')
                    battery_level = data.get('battery_level')
                    firmware_version = data.get('firmware_version')
                    
                    if not all([device_id, sensor_type, value is not None]):
                        return jsonify({'error': 'Missing required fields'}), 400
                    
                    reading = self.receive_sensor_data(
                        device_id, sensor_type, value, unit, 
                        location, battery_level, firmware_version
                    )
                    
                    return jsonify({
                        'status': 'success',
                        'reading_id': len(self._load_readings()),
                        'timestamp': reading['timestamp'],
                        'message': 'Data received successfully'
                    })
                
                except Exception as e:
                    return jsonify({'error': str(e)}), 500
            
            @self.flask_app.route('/api/device-status/<device_id>', methods=['GET'])
            def get_status(device_id):
                status = self.get_device_status(device_id)
                if status:
                    return jsonify(status)
                return jsonify({'error': 'Device not found'}), 404
            
            @self.flask_app.route('/api/health', methods=['GET'])
            def health_check():
                return jsonify({
                    'status': 'healthy',
                    'timestamp': datetime.now().isoformat(),
                    'devices_count': len(self.get_all_devices()),
                    'readings_count': len(self._load_readings())
                })
        
        # Executar Flask em thread separada
        if self.flask_thread is None or not self.flask_thread.is_alive():
            self.flask_thread = threading.Thread(
                target=lambda: self.flask_app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
            )
            self.flask_thread.daemon = True
            self.flask_thread.start()
            return True
        return False 