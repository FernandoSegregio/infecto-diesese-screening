# 🍎 Executando no macOS - Sistema de Triagem Médica IoT

## 🚨 **Problema da Porta 5001 no macOS**

No macOS, a porta **5001** é usada pelo **AirPlay Receiver** por padrão, causando conflitos. Por isso, alteramos a API IoT para usar a **porta 5002**.

## ✅ **Solução Implementada**

### **Mudanças Realizadas:**

1. **`config.py`** - Porta padrão alterada para 5002
2. **`start_iot_api.py`** - Usa configuração do config.py
3. **`start.sh`** - Atualizado para porta 5002
4. **`Dockerfile`** - Expõe porta 5002
5. **`esp32_temperature_sensor.ino`** - URL atualizada para porta 5002
6. **Documentação** - Todas as referências atualizadas

## 🚀 **Como Executar no macOS**

### **Opção 1: Execução Local**

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar diretamente
streamlit run app.py

# 3. Em outro terminal, iniciar API IoT
python start_iot_api.py

# 4. Ou usar o script completo
chmod +x start.sh
./start.sh
```

### **Opção 2: Docker**

```bash
# 1. Build da imagem
docker build -t triagem-medica-iot .

# 2. Executar container (portas atualizadas)
docker run -p 8501:8501 -p 5002:5002 triagem-medica-iot

# 3. Acessar aplicação
open http://localhost:8501
```

### **Opção 3: Docker Compose**

```yaml
# docker-compose.yml
version: '3.8'
services:
  triagem-medica:
    build: .
    ports:
      - "8501:8501"  # Streamlit
      - "5002:5002"  # API IoT (compatível com macOS)
    environment:
      - ENVIRONMENT=development
      - DEBUG=true
    volumes:
      - ./data:/app/data
```

```bash
# Executar com docker-compose
docker-compose up --build
```

## 🌡️ **Configuração do ESP32 (Wokwi)**

### **URL Atualizada:**
```cpp
// No arquivo esp32_temperature_sensor.ino
const char* serverURL = "http://localhost:5002/api/sensor-data";
```

### **Para Docker:**
```cpp
// Se usando Docker, substitua localhost pelo IP do container
const char* serverURL = "http://SEU-IP-DOCKER:5002/api/sensor-data";
```

### **Descobrir IP do Docker:**
```bash
# Descobrir IP do container
docker inspect CONTAINER_ID | grep IPAddress

# Ou usar host.docker.internal (macOS/Windows)
const char* serverURL = "http://host.docker.internal:5002/api/sensor-data";
```

## 🔧 **Verificação de Portas**

### **Verificar se porta 5002 está livre:**
```bash
# Verificar porta 5002
lsof -i :5002

# Se estiver em uso, matar processo
sudo lsof -ti:5002 | xargs kill -9
```

### **Verificar AirPlay (porta 5001):**
```bash
# Ver se AirPlay está usando porta 5001
lsof -i :5001

# Desabilitar AirPlay Receiver (opcional)
# System Preferences > Sharing > AirPlay Receiver (desmarcar)
```

## 🐛 **Solução de Problemas no macOS**

### **1. Erro de Permissão no start.sh**
```bash
chmod +x start.sh
```

### **2. Python não encontrado**
```bash
# Instalar Python via Homebrew
brew install python

# Ou usar pyenv
brew install pyenv
pyenv install 3.9.0
pyenv global 3.9.0
```

### **3. Dependências não instalam**
```bash
# Atualizar pip
pip install --upgrade pip

# Instalar com usuário
pip install --user -r requirements.txt

# Usar virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **4. Docker não funciona**
```bash
# Verificar se Docker está rodando
docker --version

# Instalar Docker Desktop para Mac
# https://docs.docker.com/desktop/mac/install/
```

### **5. Streamlit não abre no navegador**
```bash
# Abrir manualmente
open http://localhost:8501

# Ou especificar navegador
streamlit run app.py --browser.serverAddress localhost
```

## 📱 **URLs de Acesso**

### **Aplicação Principal:**
- **Local**: http://localhost:8501
- **Docker**: http://localhost:8501

### **API IoT:**
- **Local**: http://localhost:5002
- **Docker**: http://localhost:5002
- **Health Check**: http://localhost:5002/api/health

### **Wokwi ESP32:**
- **Simulador**: https://wokwi.com
- **URL para API**: `http://localhost:5002/api/sensor-data`

## 🔐 **Credenciais Padrão**

```
Usuário: admin
Senha: admin123
```

## 📊 **Monitoramento**

### **Logs da API IoT:**
```bash
# Ver logs em tempo real
tail -f logs/iot_api.log

# Ou no terminal onde rodou start_iot_api.py
```

### **Logs do Streamlit:**
```bash
# Ver logs no terminal onde rodou streamlit
# Ou verificar ~/.streamlit/logs/
```

## 🎯 **Próximos Passos**

1. ✅ **Executar sistema** localmente
2. ✅ **Testar API IoT** na porta 5002
3. ✅ **Configurar ESP32** no Wokwi
4. ✅ **Verificar Dashboard IoT**
5. ✅ **Testar integração** completa

---

**🍎 Configuração otimizada para macOS!**  
*Porta 5002 evita conflitos com AirPlay Receiver* 