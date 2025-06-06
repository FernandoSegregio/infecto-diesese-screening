#!/usr/bin/env python3
"""
Script para iniciar um broker MQTT local para desenvolvimento
"""

import subprocess
import sys
import os
import time

def check_mosquitto_installed():
    """Verifica se o Mosquitto está instalado"""
    try:
        result = subprocess.run(['mosquitto', '--help'], 
                              capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False

def install_mosquitto_macos():
    """Instala Mosquitto no macOS via Homebrew"""
    print("📦 Instalando Mosquitto via Homebrew...")
    try:
        subprocess.run(['brew', 'install', 'mosquitto'], check=True)
        print("✅ Mosquitto instalado com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar Mosquitto")
        return False
    except FileNotFoundError:
        print("❌ Homebrew não encontrado. Instale primeiro o Homebrew.")
        return False

def start_mosquitto():
    """Inicia o broker Mosquitto"""
    print("🚀 Iniciando broker MQTT (Mosquitto)...")
    
    # Configuração básica do Mosquitto para desenvolvimento
    config_content = """
# Configuração básica para desenvolvimento
port 1883
listener 1883
allow_anonymous true
log_dest stdout
log_type all
"""
    
    # Criar arquivo de configuração temporário
    config_file = "/tmp/mosquitto_dev.conf"
    with open(config_file, 'w') as f:
        f.write(config_content)
    
    try:
        print(f"📡 Broker MQTT rodando na porta 1883")
        print(f"🔧 Configuração: {config_file}")
        print(f"🔄 Pressione Ctrl+C para parar o broker")
        
        # Iniciar Mosquitto
        process = subprocess.run([
            'mosquitto', '-c', config_file, '-v'
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Parando broker MQTT...")
    except Exception as e:
        print(f"❌ Erro ao iniciar Mosquitto: {str(e)}")

def main():
    print("🌐 === BROKER MQTT LOCAL ===")
    
    # Verificar se está no macOS
    if sys.platform == "darwin":
        print("🍎 Sistema detectado: macOS")
        
        # Verificar se Mosquitto está instalado
        if not check_mosquitto_installed():
            print("📋 Mosquitto não encontrado")
            install = input("Deseja instalar via Homebrew? (s/n): ")
            
            if install.lower() == 's':
                if install_mosquitto_macos():
                    start_mosquitto()
                else:
                    print("💡 Instale manualmente: brew install mosquitto")
            else:
                print("💡 Para instalar manualmente:")
                print("   brew install mosquitto")
        else:
            start_mosquitto()
    
    else:
        print("🐧 Sistema detectado: Linux/Outros")
        if not check_mosquitto_installed():
            print("📋 Mosquitto não encontrado")
            print("💡 Para instalar:")
            print("   Ubuntu/Debian: sudo apt-get install mosquitto")
            print("   CentOS/RHEL: sudo yum install mosquitto")
            print("   Arch: sudo pacman -S mosquitto")
        else:
            start_mosquitto()

if __name__ == "__main__":
    main() 