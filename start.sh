#!/bin/bash

# Script de inicialização para AWS App Runner
# Sistema de Triagem Médica IoT

set -e  # Parar em caso de erro

echo "🏥 =========================================="
echo "🏥 Sistema de Triagem Médica IoT"
echo "🏥 Iniciando na AWS App Runner..."
echo "🏥 =========================================="
echo "📅 $(date)"
echo "🌍 Timezone: $(date +%Z)"
echo "💻 Python: $(python --version)"
echo "📦 Pip: $(pip --version)"

# Verificar se os arquivos principais existem
echo "🔍 Verificando arquivos principais..."
required_files=("app.py" "triagem_model.py" "auth.py" "security.py" "iot_manager.py" "iot_dashboard.py")

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Erro: $file não encontrado"
        exit 1
    else
        echo "✅ $file encontrado"
    fi
done

# Inicializar arquivos de dados se não existirem
echo "📂 Inicializando arquivos de dados..."

# Arquivo de usuários
if [ ! -f "users.json" ]; then
    echo '{
  "admin": {
    "password_hash": "scrypt:32768:8:1$salt$hash",
    "name": "Administrador",
    "role": "admin",
    "permissions": ["triagem", "historico", "audit_log", "user_management"],
    "created_at": "'$(date -Iseconds)'",
    "last_login": null,
    "active": true
  }
}' > users.json
    echo "✅ users.json criado com usuário admin padrão"
else
    echo "✅ users.json já existe"
fi

# Arquivo de dispositivos IoT
if [ ! -f "iot_devices.json" ]; then
    echo '{
  "ESP32_DEMO_001": {
    "name": "Sensor Demo AWS",
    "type": "temperature_sensor",
    "location": "AWS App Runner Demo",
    "registered_at": "'$(date -Iseconds)'",
    "last_seen": null,
    "status": "offline",
    "battery_level": null,
    "firmware_version": "1.0.0"
  }
}' > iot_devices.json
    echo "✅ iot_devices.json criado com dispositivo demo"
else
    echo "✅ iot_devices.json já existe"
fi

# Arquivo de leituras IoT
if [ ! -f "iot_readings.json" ]; then
    echo '[]' > iot_readings.json
    echo "✅ iot_readings.json criado"
else
    echo "✅ iot_readings.json já existe"
fi

# Arquivo de histórico de atendimentos
if [ ! -f "historico_atendimentos.json" ]; then
    echo '[]' > historico_atendimentos.json
    echo "✅ historico_atendimentos.json criado"
else
    echo "✅ historico_atendimentos.json já existe"
fi

# Arquivo de auditoria
if [ ! -f "audit_log.json" ]; then
    echo '[]' > audit_log.json
    echo "✅ audit_log.json criado"
else
    echo "✅ audit_log.json já existe"
fi

# Arquivo de sessões
if [ ! -f "sessions.json" ]; then
    echo '{}' > sessions.json
    echo "✅ sessions.json criado"
else
    echo "✅ sessions.json já existe"
fi

# Chave de criptografia
if [ ! -f ".encryption_key" ]; then
    python -c "
import secrets
import base64
key = secrets.token_bytes(32)
with open('.encryption_key', 'wb') as f:
    f.write(base64.b64encode(key))
print('✅ Chave de criptografia gerada')
"
else
    echo "✅ .encryption_key já existe"
fi

echo "📂 Todos os arquivos de dados inicializados!"

# Função para verificar se uma porta está em uso
check_port() {
    local port=$1
    if netstat -tuln 2>/dev/null | grep -q ":$port "; then
        return 0  # Porta em uso
    else
        return 1  # Porta livre
    fi
}

# Iniciar API IoT em background
echo "📡 Iniciando API IoT na porta 5001..."

if check_port 5001; then
    echo "⚠️ Porta 5001 já está em uso, tentando matar processo..."
    pkill -f "start_iot_api.py" || true
    sleep 2
fi

# Iniciar API IoT
python start_iot_api.py &
API_PID=$!
echo "🔄 API IoT iniciada com PID: $API_PID"

# Aguardar API inicializar
echo "⏳ Aguardando API IoT inicializar..."
sleep 15

# Verificar se API está respondendo
echo "🔍 Verificando API IoT..."
api_ready=false

for i in {1..10}; do
    if curl -f -s http://localhost:5001/api/health > /dev/null 2>&1; then
        echo "✅ API IoT respondendo na tentativa $i!"
        api_ready=true
        break
    else
        echo "⏳ Tentativa $i/10 - API ainda não está pronta..."
        sleep 3
    fi
done

if [ "$api_ready" = true ]; then
    echo "🎉 API IoT iniciada com sucesso!"
    curl -s http://localhost:5001/api/health | head -1
else
    echo "⚠️ API IoT não respondeu, mas continuando com Streamlit..."
fi

# Verificar se Streamlit está disponível
echo "🔍 Verificando instalação do Streamlit..."
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit não encontrado!"
    exit 1
fi

echo "✅ Streamlit encontrado: $(streamlit version)"

# Configurar variáveis de ambiente para Streamlit
export STREAMLIT_SERVER_PORT=${STREAMLIT_SERVER_PORT:-8501}
export STREAMLIT_SERVER_ADDRESS=${STREAMLIT_SERVER_ADDRESS:-0.0.0.0}
export STREAMLIT_SERVER_HEADLESS=${STREAMLIT_SERVER_HEADLESS:-true}
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=${STREAMLIT_BROWSER_GATHER_USAGE_STATS:-false}
export STREAMLIT_SERVER_ENABLE_CORS=${STREAMLIT_SERVER_ENABLE_CORS:-false}
export STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=${STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION:-false}

echo "🌐 Configurações do Streamlit:"
echo "   - Porta: $STREAMLIT_SERVER_PORT"
echo "   - Endereço: $STREAMLIT_SERVER_ADDRESS"
echo "   - Headless: $STREAMLIT_SERVER_HEADLESS"

# Iniciar Streamlit
echo "🚀 Iniciando Streamlit..."
echo "🔗 A aplicação estará disponível em breve na porta $STREAMLIT_SERVER_PORT"
echo "🏥 Sistema de Triagem Médica IoT - Pronto para uso!"

# Executar Streamlit (este comando não retorna)
exec streamlit run app.py \
    --server.port $STREAMLIT_SERVER_PORT \
    --server.address $STREAMLIT_SERVER_ADDRESS \
    --server.headless $STREAMLIT_SERVER_HEADLESS \
    --server.enableCORS $STREAMLIT_SERVER_ENABLE_CORS \
    --server.enableXsrfProtection $STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION \
    --server.maxUploadSize 10 