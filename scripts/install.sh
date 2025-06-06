#!/bin/bash

# 🏥 Script de Instalação - Sistema de Triagem Médica com IoT
# Executa: bash install.sh

echo "🏥 ===== SISTEMA DE TRIAGEM MÉDICA COM IoT ====="
echo "🚀 Iniciando instalação automática..."
echo ""

# Verificar se Python está instalado
echo "🐍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "💡 Instale Python 3.8+ em: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION encontrado"

# Verificar versão mínima
if [[ $(echo "$PYTHON_VERSION >= 3.8" | bc -l) -eq 0 ]]; then
    echo "⚠️ Aviso: Python 3.8+ recomendado (atual: $PYTHON_VERSION)"
fi

echo ""

# Criar ambiente virtual
echo "📦 Criando ambiente virtual..."
if [ -d "venv" ]; then
    echo "⚠️ Ambiente virtual já existe, usando existente"
else
    python3 -m venv venv
    echo "✅ Ambiente virtual criado"
fi

# Ativar ambiente virtual
echo "🔌 Ativando ambiente virtual..."
source venv/bin/activate

# Verificar pip
echo "📥 Verificando pip..."
pip install --upgrade pip

# Instalar dependências
echo "📦 Instalando dependências..."
echo "   Isso pode demorar alguns minutos na primeira vez..."

pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependências instaladas com sucesso!"
else
    echo "❌ Erro ao instalar dependências"
    echo "💡 Tente: pip install -r requirements.txt"
    exit 1
fi

echo ""

# Verificar dependências críticas
echo "🔍 Verificando instalação..."
python3 -c "
import streamlit
import paho.mqtt.client
import pandas
import plotly
print('✅ Streamlit:', streamlit.__version__)
print('✅ MQTT:', 'OK')
print('✅ Pandas:', pandas.__version__)
print('✅ Plotly:', plotly.__version__)
"

if [ $? -eq 0 ]; then
    echo "✅ Todas as dependências verificadas!"
else
    echo "❌ Erro na verificação das dependências"
    exit 1
fi

echo ""
echo "🎉 ===== INSTALAÇÃO CONCLUÍDA! ====="
echo ""
echo "🚀 Para executar o sistema:"
echo "   1. Ativar ambiente: source venv/bin/activate"
echo "   2. Executar aplicação: streamlit run app.py"
echo "   3. Abrir navegador: http://localhost:8501"
echo ""
echo "👤 Credenciais padrão:"
echo "   admin / admin123"
echo "   medico / medico123"
echo "   enfermeiro / enfermeiro123"
echo ""
echo "📚 Guias disponíveis:"
echo "   README.md - Guia completo de instalação"
echo "   MQTT_SETUP_GUIDE.md - Configuração ESP32"
echo ""
echo "🎮 Para testar ESP32:"
echo "   1. Acesse: https://wokwi.com"
echo "   2. Use código: esp32_temperature_sensor.ino"
echo "   3. Configure componentes conforme MQTT_SETUP_GUIDE.md"
echo ""
echo "🆘 Em caso de problemas:"
echo "   - Verifique Python 3.8+"
echo "   - Reinstale: pip install -r requirements.txt"
echo "   - Consulte seção 'Solução de Problemas' no README.md"
echo ""
echo "✨ Sistema pronto para uso!" 