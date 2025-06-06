#!/usr/bin/env python3
"""
Script para iniciar o cliente MQTT que recebe dados dos sensores termômetro
"""

from mqtt_manager import MQTTManager
import time
import sys

def main():
    print("🌡️ === CLIENTE MQTT TERMÔMETRO ===")
    
    # Configurações MQTT - HiveMQ Cloud
    print("🌐 Conectando ao HiveMQ Cloud...")
    print("📋 Credenciais: FARM_TECH")
    
    # Criar e iniciar cliente MQTT
    mqtt_client = MQTTManager()  # Usa configurações padrão do HiveMQ Cloud
    
    # Iniciar cliente
    if mqtt_client.start():
        print("✅ Cliente MQTT iniciado com sucesso!")
        print("\n📡 Broker: HiveMQ Cloud (TLS/SSL)")
        print("👤 Usuário: FARM_TECH")
        print("\n📋 Tópicos monitorados:")
        for name, topic in mqtt_client.topics.items():
            print(f"   {name}: {topic}")
        
        print(f"\n🌡️ Aguardando dados do termômetro ESP32...")
        print(f"📱 Device ID esperado: ESP32_TERMOMETRO_001")
        print(f"📍 Local: Recepção - Posto 1")
        
        print(f"\n💡 Formato dos dados esperados:")
        print(f"""
🌡️ Temperatura:
   Tópico: termometro/temperatura
   {{
     "device_id": "ESP32_TERMOMETRO_001",
     "sensor_type": "temperature",
     "value": 36.5,
     "unit": "°C",
     "location": "Recepção - Posto 1",
     "battery_level": 85,
     "timestamp": 1234567890
   }}
   
📊 Status:
   Tópico: termometro/status
   {{
     "device_id": "ESP32_TERMOMETRO_001",
     "status": "NORMAL",
     "temperature": 36.5,
     "location": "Recepção - Posto 1",
     "timestamp": 1234567890
   }}
   
🚨 Alertas:
   Tópico: termometro/alerta
   {{
     "device_id": "ESP32_TERMOMETRO_001",
     "alert_type": "FEBRE",
     "temperature": 38.2,
     "location": "Recepção - Posto 1",
     "priority": "HIGH",
     "timestamp": 1234567890
   }}
        """)
        
        print(f"\n🔄 Aguardando mensagens... (Ctrl+C para parar)")
        
        try:
            # Aguardar conexão
            print("⏳ Estabelecendo conexão...")
            time.sleep(3)
            
            # Enviar mensagem de teste se solicitado
            if len(sys.argv) > 1 and sys.argv[1] == "--test":
                print("\n🧪 Enviando mensagem de teste...")
                mqtt_client.publish_test_message()
            
            # Verificar se conectou
            status = mqtt_client.get_connection_status()
            if status['connected']:
                print("✅ Conectado e pronto para receber dados!")
            else:
                print("⚠️ Problema na conexão, mas tentando...")
            
            # Manter cliente rodando
            while True:
                time.sleep(10)
                
                # Mostrar status a cada 30 segundos
                if int(time.time()) % 30 == 0:
                    status = mqtt_client.get_connection_status()
                    if status['connected']:
                        print(f"💚 Sistema ativo - {time.strftime('%H:%M:%S')}")
                        
                        # Mostrar estatísticas
                        devices = mqtt_client.get_devices()
                        readings = mqtt_client.get_latest_readings()
                        
                        print(f"   📱 Dispositivos: {len(devices)}")
                        print(f"   📊 Leituras: {len(readings)}")
                        
                        if readings:
                            latest = readings[-1]
                            print(f"   🌡️ Última: {latest.get('value')}°C ({latest.get('device_id')})")
                    else:
                        print(f"❤️ Reconectando... - {time.strftime('%H:%M:%S')}")
                
        except KeyboardInterrupt:
            print("\n🛑 Parando cliente MQTT...")
            mqtt_client.stop()
            
            # Mostrar estatísticas finais
            devices = mqtt_client.get_devices()
            readings = mqtt_client.get_latest_readings()
            
            print(f"\n📊 Estatísticas da sessão:")
            print(f"   📱 Dispositivos registrados: {len(devices)}")
            print(f"   📋 Total de leituras: {len(readings)}")
            
            if readings:
                print(f"\n🌡️ Últimas 3 leituras:")
                for reading in readings[-3:]:
                    timestamp = reading.get('timestamp', 'N/A')
                    device_id = reading.get('device_id', 'N/A')
                    value = reading.get('value', 'N/A')
                    unit = reading.get('unit', '')
                    print(f"   • {device_id}: {value}{unit} - {timestamp}")
    
    else:
        print("❌ Falha ao iniciar cliente MQTT")
        print("\n🔧 Possíveis problemas:")
        print("   • Conexão com internet")
        print("   • Credenciais incorretas")
        print("   • Firewall bloqueando porta 8883")
        print("   • Certificados SSL/TLS")
        
        print("\n💡 Para debug:")
        print("   1. Teste sua conexão: ping 91c5f1ea0f494ccebe45208ea8ffceff.s1.eu.hivemq.cloud")
        print("   2. Verifique se a porta 8883 está aberta")
        print("   3. Confirme as credenciais no código ESP32")

if __name__ == "__main__":
    main() 