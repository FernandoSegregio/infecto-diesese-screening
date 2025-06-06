#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.iot.iot_manager import IoTManager
from src.config.config import Config
from flask import Flask, request, jsonify
import json
import time

def main():
    print("🚀 Iniciando API IoT...")
    print(f"📡 Configurada para porta: {Config.IOT_API_PORT}")
    
    # Criar instância do IoT Manager
    iot_manager = IoTManager()
    
    # Usar porta do config
    port = Config.IOT_API_PORT
    
    # Iniciar servidor API
    success = iot_manager.start_api_server(port=port)
    
    if success:
        print("✅ API IoT iniciada com sucesso!")
        print(f"📡 Servidor rodando em: http://127.0.0.1:{port}")
        print("📋 Endpoints disponíveis:")
        print("   GET  /                     - Informações da API")
        print("   POST /webhook             - Webhook para ESP32")
        print("   POST /api/sensor-data     - Receber dados de sensores")
        print("   GET  /api/health          - Health check")
        print("   GET  /api/device-status/<id> - Status do dispositivo")
        print(f"\n🌡️ Para o ESP32, configure a URL:")
        print(f"   http://localhost:{port}/webhook")
        print(f"   ou")
        print(f"   http://127.0.0.1:{port}/webhook")
        print(f"\n🔄 Pressione Ctrl+C para parar o servidor")
        
        try:
            # Manter o script rodando
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Parando servidor API IoT...")
    else:
        print("❌ Erro ao iniciar API IoT")
        print("💡 Verifique se a porta não está em uso")

if __name__ == "__main__":
    main() 