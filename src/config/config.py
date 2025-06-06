"""
Configurações do Sistema de Triagem Médica IoT
"""

import os
import streamlit as st
from datetime import datetime

class Config:
    """Configurações da aplicação"""
    
    # Ambiente
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    # Portas
    STREAMLIT_PORT = int(os.getenv('STREAMLIT_SERVER_PORT', '8501'))
    IOT_API_PORT = int(os.getenv('IOT_API_PORT', '5002'))
    
    # Configurações de segurança
    SECRET_KEY = os.getenv('SECRET_KEY', 'triagem-medica-local-2024-secure-key')
    
    # Configurações de dados
    DATA_DIR = os.getenv('DATA_DIR', './data')
    
    # Configurações do Streamlit
    STREAMLIT_CONFIG = {
        'server.port': STREAMLIT_PORT,
        'server.address': 'localhost',
        'server.headless': False,
        'server.enableCORS': True,
        'server.enableXsrfProtection': True,
        'server.maxUploadSize': 10,
        'browser.gatherUsageStats': False,
        'theme.primaryColor': '#1f77b4',
        'theme.backgroundColor': '#ffffff',
        'theme.secondaryBackgroundColor': '#f0f2f6',
        'theme.textColor': '#262730'
    }
    
    # Configurações IoT e Webhook
    WEBHOOK_ENDPOINT = "/webhook"
    ESP32_DEVICE_PREFIX = "ESP32_TERMOMETRO_"

    # URLs para teste do webhook
    WEBHOOK_TEST_URLS = [
        f"http://localhost:{IOT_API_PORT}/webhook",
        f"http://localhost:{IOT_API_PORT}/",
        f"http://127.0.0.1:{IOT_API_PORT}/webhook"
    ]

    # Configurações de temperatura para alertas
    TEMPERATURE_THRESHOLDS = {
        'NORMAL_MIN': 35.1,
        'NORMAL_MAX': 37.7,
        'FEVER_MIN': 37.8,
        'FEVER_MAX': 38.9,
        'CRITICAL_MIN': 39.0
    }
    
    @staticmethod
    def init_app():
        """Inicializa configurações da aplicação"""
        try:
            # Configurações da página
            st.set_page_config(
                page_title="Sistema de Triagem Médica IoT",
                page_icon="🏥",
                layout="wide",
                initial_sidebar_state="expanded",
                menu_items={
                    'Get Help': 'https://github.com/seu-usuario/triagem-medica',
                    'Report a bug': 'https://github.com/seu-usuario/triagem-medica/issues',
                    'About': """
                    # Sistema de Triagem Médica IoT
                    
                    Sistema de IA para apoio ao diagnóstico médico em áreas vulneráveis.
                    
                    **Versão:** 2.0  
                    **Ambiente:** Local  
                    **Desenvolvido para:** Médicos Sem Fronteiras e áreas remotas
                    """
                }
            )
            
            # Criar diretórios necessários
            os.makedirs(Config.DATA_DIR, exist_ok=True)
            
            # Log de inicialização
            print(f"🏥 Sistema de Triagem Médica IoT")
            print(f"🌍 Ambiente: {Config.ENVIRONMENT}")
            print(f"🔧 Debug: {Config.DEBUG}")
            print(f"📡 Porta Streamlit: {Config.STREAMLIT_PORT}")
            print(f"🌡️ Porta API IoT: {Config.IOT_API_PORT}")
            print(f"📂 Diretório de dados: {Config.DATA_DIR}")
            print(f"🕐 Inicializado em: {datetime.now().isoformat()}")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao inicializar configurações: {str(e)}")
            return False
    
    @staticmethod
    def get_database_url():
        """Retorna URL do banco de dados local"""
        return os.getenv('DATABASE_URL', 'sqlite:///triagem.db')
    
    @staticmethod
    def is_production():
        """Verifica se está em produção"""
        return Config.ENVIRONMENT == 'production'
    
    @staticmethod
    def get_version():
        """Retorna versão da aplicação"""
        return "2.0.0-local"

# Inicializar configurações ao importar
if __name__ != "__main__":
    Config.init_app() 