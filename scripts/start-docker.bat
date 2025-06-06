@echo off
chcp 65001 >nul

:: 🐳 Script de Inicialização Docker - Sistema de Triagem Médica com IoT
:: Executa: start-docker.bat

echo 🐳 ===== SISTEMA DE TRIAGEM MÉDICA COM IoT - DOCKER =====
echo 🚀 Iniciando sistema via Docker...
echo.

:: Verificar se Docker está instalado
echo 🔍 Verificando Docker...
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker não encontrado ou não está rodando!
    echo 💡 Instale Docker Desktop: https://docs.docker.com/get-docker/
    echo 💡 Certifique-se que Docker Desktop está iniciado
    pause
    exit /b 1
)

echo ✅ Docker encontrado

:: Verificar se Docker Compose está disponível
docker compose version >nul 2>&1
if %errorlevel% neq 0 (
    docker-compose version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Docker Compose não encontrado!
        echo 💡 Use uma versão mais recente do Docker Desktop
        pause
        exit /b 1
    )
)

echo ✅ Docker Compose encontrado
echo.

:: Parar containers existentes se houver
echo 🛑 Parando containers existentes...
docker compose down >nul 2>&1
if %errorlevel% neq 0 (
    docker-compose down >nul 2>&1
)

:: Criar diretórios para dados persistentes
echo 📁 Criando diretórios de dados...
if not exist "data" mkdir data
if not exist "logs" mkdir logs

:: Verificar se Dockerfile existe
if not exist "Dockerfile" (
    echo ❌ Dockerfile não encontrado!
    echo 💡 Certifique-se de estar no diretório correto do projeto
    pause
    exit /b 1
)

:: Construir e iniciar containers
echo 🔨 Construindo imagem Docker...
echo    Isso pode demorar alguns minutos na primeira vez...

:: Tentar docker compose primeiro, depois docker-compose
docker compose up --build -d >nul 2>&1
if %errorlevel% neq 0 (
    docker-compose up --build -d
)

if %errorlevel% equ 0 (
    echo.
    echo 🎉 ===== SISTEMA DOCKER INICIADO COM SUCESSO! =====
    echo.
    echo 🌐 Acessar aplicação:
    echo    URL: http://localhost:8501
    echo    Aguarde 30-60 segundos para carregar completamente
    echo.
    echo 👤 Credenciais padrão:
    echo    admin / admin123
    echo    medico / medico123
    echo    enfermeiro / enfermeiro123
    echo.
    echo 🔧 Comandos úteis:
    echo    Ver logs: docker-compose logs -f
    echo    Parar: docker-compose down
    echo    Reiniciar: docker-compose restart
    echo    Status: docker-compose ps
    echo.
    echo 🎮 Para testar ESP32:
    echo    1. Acesse: https://wokwi.com
    echo    2. Use código: esp32_temperature_sensor.ino
    echo    3. Sistema MQTT já configurado no container
    echo.
    echo 📊 Verificar status do container:
    echo    docker-compose ps
    echo.
    echo ✨ Sistema rodando via Docker!
    echo.
    
    :: Mostrar status dos containers
    echo 📋 Status dos containers:
    docker compose ps 2>nul
    if %errorlevel% neq 0 (
        docker-compose ps
    )
    
) else (
    echo.
    echo ❌ Erro ao iniciar o sistema Docker
    echo.
    echo 🆘 Solução de problemas:
    echo    1. Verificar se Docker está rodando:
    echo       docker version
    echo.
    echo    2. Verificar logs de erro:
    echo       docker-compose logs
    echo.
    echo    3. Tentar construir manualmente:
    echo       docker build -t triagem-medica .
    echo       docker run -p 8501:8501 triagem-medica
    echo.
    echo    4. Verificar se porta 8501 está livre
    echo.
    pause
    exit /b 1
)

echo.
pause 