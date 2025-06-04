"""
Configurações para produção na AWS App Runner
Sistema de Triagem Médica IoT
"""

import os
import streamlit as st
from datetime import datetime

class Config:
    """Configurações para produção na AWS"""
    
    # Ambiente
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')
    
    # Portas
    STREAMLIT_PORT = int(os.getenv('STREAMLIT_SERVER_PORT', '8501'))
    IOT_API_PORT = int(os.getenv('IOT_API_PORT', '5001'))
    
    # Configurações de segurança
    SECRET_KEY = os.getenv('SECRET_KEY', 'triagem-medica-aws-2024-secure-key')
    
    # Configurações de dados
    DATA_DIR = os.getenv('DATA_DIR', '/app/data')
    
    # AWS específico
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    
    # Configurações do Streamlit
    STREAMLIT_CONFIG = {
        'server.port': STREAMLIT_PORT,
        'server.address': '0.0.0.0',
        'server.headless': True,
        'server.enableCORS': False,
        'server.enableXsrfProtection': False,
        'server.maxUploadSize': 10,
        'browser.gatherUsageStats': False,
        'theme.primaryColor': '#1f77b4',
        'theme.backgroundColor': '#ffffff',
        'theme.secondaryBackgroundColor': '#f0f2f6',
        'theme.textColor': '#262730'
    }
    
    @staticmethod
    def init_app():
        """Inicializa configurações da aplicação"""
        try:
            if Config.ENVIRONMENT == 'production':
                # Configurações específicas para produção
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
                        **Ambiente:** AWS App Runner  
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
        """Retorna URL do banco de dados (futuro)"""
        # Para futuras implementações com RDS
        return os.getenv('DATABASE_URL', 'sqlite:///triagem.db')
    
    @staticmethod
    def get_s3_config():
        """Retorna configurações do S3 (futuro)"""
        return {
            'bucket': os.getenv('S3_BUCKET_NAME', 'triagem-medica-data'),
            'region': Config.AWS_REGION,
            'access_key': os.getenv('AWS_ACCESS_KEY_ID'),
            'secret_key': os.getenv('AWS_SECRET_ACCESS_KEY')
        }
    
    @staticmethod
    def is_production():
        """Verifica se está em produção"""
        return Config.ENVIRONMENT == 'production'
    
    @staticmethod
    def get_version():
        """Retorna versão da aplicação"""
        return "2.0.0-aws"

# Configurações específicas para AWS App Runner
class AWSConfig:
    """Configurações específicas para AWS"""
    
    # CloudWatch Logs
    LOG_GROUP = '/aws/apprunner/triagem-medica'
    
    # Health Check
    HEALTH_CHECK_PATH = '/_stcore/health'
    HEALTH_CHECK_INTERVAL = 30
    
    # Auto Scaling
    MIN_INSTANCES = 1
    MAX_INSTANCES = 3
    MAX_CONCURRENCY = 10
    
    # Recursos
    CPU = '0.25 vCPU'
    MEMORY = '0.5 GB'
    
    @staticmethod
    def get_service_info():
        """Retorna informações do serviço"""
        return {
            'service_name': 'triagem-medica-iot',
            'runtime': 'python3.9',
            'framework': 'streamlit',
            'deployment_date': datetime.now().isoformat(),
            'region': Config.AWS_REGION,
            'cpu': AWSConfig.CPU,
            'memory': AWSConfig.MEMORY
        }

# Inicializar configurações ao importar
if __name__ != "__main__":
    Config.init_app() 