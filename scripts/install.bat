@echo off
chcp 65001 >nul

:: 🏥 Script de Instalação - Sistema de Triagem Médica com IoT
:: Executa: install.bat

echo 🏥 ===== SISTEMA DE TRIAGEM MÉDICA COM IoT =====
echo 🚀 Iniciando instalação automática...
echo.

:: Verificar se Python está instalado
echo 🐍 Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo 💡 Instale Python 3.8+ em: https://www.python.org/downloads/
    echo 💡 IMPORTANTE: Marque a opção "Add Python to PATH" durante a instalação
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% encontrado
echo.

:: Criar ambiente virtual
echo 📦 Criando ambiente virtual...
if exist "venv" (
    echo ⚠️ Ambiente virtual já existe, usando existente
) else (
    python -m venv venv
    echo ✅ Ambiente virtual criado
)

:: Ativar ambiente virtual
echo 🔌 Ativando ambiente virtual...
call venv\Scripts\activate.bat

:: Verificar pip
echo 📥 Verificando pip...
python -m pip install --upgrade pip

:: Instalar dependências
echo 📦 Instalando dependências...
echo    Isso pode demorar alguns minutos na primeira vez...

python -m pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo ✅ Dependências instaladas com sucesso!
) else (
    echo ❌ Erro ao instalar dependências
    echo 💡 Tente: python -m pip install -r requirements.txt
    pause
    exit /b 1
)

echo.

:: Verificar dependências críticas
echo 🔍 Verificando instalação...
python -c "import streamlit; import paho.mqtt.client; import pandas; import plotly; print('✅ Streamlit:', streamlit.__version__); print('✅ MQTT: OK'); print('✅ Pandas:', pandas.__version__); print('✅ Plotly:', plotly.__version__)"

if %errorlevel% equ 0 (
    echo ✅ Todas as dependências verificadas!
) else (
    echo ❌ Erro na verificação das dependências
    pause
    exit /b 1
)

echo.
echo 🎉 ===== INSTALAÇÃO CONCLUÍDA! =====
echo.
echo 🚀 Para executar o sistema:
echo    1. Ativar ambiente: venv\Scripts\activate
echo    2. Executar aplicação: streamlit run app.py
echo    3. Abrir navegador: http://localhost:8501
echo.
echo 👤 Credenciais padrão:
echo    admin / admin123
echo    medico / medico123
echo    enfermeiro / enfermeiro123
echo.
echo 📚 Guias disponíveis:
echo    README.md - Guia completo de instalação
echo    MQTT_SETUP_GUIDE.md - Configuração ESP32
echo.
echo 🎮 Para testar ESP32:
echo    1. Acesse: https://wokwi.com
echo    2. Use código: esp32_temperature_sensor.ino
echo    3. Configure componentes conforme MQTT_SETUP_GUIDE.md
echo.
echo 🆘 Em caso de problemas:
echo    - Verifique Python 3.8+
echo    - Reinstale: python -m pip install -r requirements.txt
echo    - Consulte seção "Solução de Problemas" no README.md
echo.
echo ✨ Sistema pronto para uso!
echo.
pause 