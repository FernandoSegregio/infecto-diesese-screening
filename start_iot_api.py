#!/usr/bin/env python3
"""
Script para iniciar a API IoT manualmente
"""

from iot_manager import IoTManager
import time

def main():
    print("🚀 Iniciando API IoT...")
    
    # Criar instância do IoT Manager
    iot_manager = IoTManager()
    
    # Iniciar servidor API
    success = iot_manager.start_api_server(port=5001)
    
    if success:
        print("✅ API IoT iniciada com sucesso!")
        print("📡 Servidor rodando em: http://127.0.0.1:5001")
        print("📋 Endpoints disponíveis:")
        print("   GET  /                     - Informações da API")
        print("   POST /api/sensor-data     - Receber dados de sensores")
        print("   GET  /api/health          - Health check")
        print("   GET  /api/device-status/<id> - Status do dispositivo")
        print("\n🔄 Pressione Ctrl+C para parar o servidor")
        
        try:
            # Manter o script rodando
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Parando servidor API IoT...")
    else:
        print("❌ Erro ao iniciar API IoT")

if __name__ == "__main__":
    main() 