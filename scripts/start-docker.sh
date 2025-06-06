#!/bin/bash

# 🐳 Script de Inicialização Docker - Sistema de Triagem Médica com IoT
# Executa: bash start-docker.sh

echo "🐳 ===== SISTEMA DE TRIAGEM MÉDICA COM IoT - DOCKER ====="
echo "🚀 Iniciando sistema via Docker..."
echo ""

# Verificar se Docker está instalado
echo "🔍 Verificando Docker..."
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado!"
    echo "💡 Instale Docker em: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✅ Docker encontrado"

# Verificar se Docker Compose está disponível
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose não encontrado!"
    echo "💡 Instale Docker Compose ou use uma versão mais recente do Docker"
    exit 1
fi

echo "✅ Docker Compose encontrado"
echo ""

# Parar containers existentes se houver
echo "🛑 Parando containers existentes..."
docker-compose down 2>/dev/null || docker compose down 2>/dev/null || echo "Nenhum container rodando"

# Criar diretórios para dados persistentes
echo "📁 Criando diretórios de dados..."
mkdir -p data logs

# Verificar se Dockerfile existe
if [ ! -f "Dockerfile" ]; then
    echo "❌ Dockerfile não encontrado!"
    echo "💡 Certifique-se de estar no diretório correto do projeto"
    exit 1
fi

# Construir e iniciar containers
echo "🔨 Construindo imagem Docker..."
echo "   Isso pode demorar alguns minutos na primeira vez..."

# Tentar docker compose primeiro, depois docker-compose
if docker compose version &> /dev/null; then
    docker compose up --build -d
elif command -v docker-compose &> /dev/null; then
    docker-compose up --build -d
else
    echo "❌ Não foi possível encontrar comando do Docker Compose"
    exit 1
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 ===== SISTEMA DOCKER INICIADO COM SUCESSO! ====="
    echo ""
    echo "🌐 Acessar aplicação:"
    echo "   URL: http://localhost:8501"
    echo "   Aguarde 30-60 segundos para carregar completamente"
    echo ""
    echo "👤 Credenciais padrão:"
    echo "   admin / admin123"
    echo "   medico / medico123"
    echo "   enfermeiro / enfermeiro123"
    echo ""
    echo "🔧 Comandos úteis:"
    echo "   Ver logs: docker-compose logs -f"
    echo "   Parar: docker-compose down"
    echo "   Reiniciar: docker-compose restart"
    echo "   Status: docker-compose ps"
    echo ""
    echo "🎮 Para testar ESP32:"
    echo "   1. Acesse: https://wokwi.com"
    echo "   2. Use código: esp32_temperature_sensor.ino"
    echo "   3. Sistema MQTT já configurado no container"
    echo ""
    echo "📊 Verificar status do container:"
    echo "   docker-compose ps"
    echo ""
    echo "✨ Sistema rodando via Docker!"
    echo ""
    
    # Mostrar status dos containers
    echo "📋 Status dos containers:"
    if docker compose version &> /dev/null; then
        docker compose ps
    else
        docker-compose ps
    fi
    
else
    echo ""
    echo "❌ Erro ao iniciar o sistema Docker"
    echo ""
    echo "🆘 Solução de problemas:"
    echo "   1. Verificar se Docker está rodando:"
    echo "      docker version"
    echo ""
    echo "   2. Verificar logs de erro:"
    echo "      docker-compose logs"
    echo ""
    echo "   3. Tentar construir manualmente:"
    echo "      docker build -t triagem-medica ."
    echo "      docker run -p 8501:8501 triagem-medica"
    echo ""
    echo "   4. Verificar portas disponíveis:"
    echo "      lsof -i :8501"
    echo ""
    exit 1
fi 