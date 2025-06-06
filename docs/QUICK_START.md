# ⚡ Início Rápido - Sistema de Triagem Médica com IoT

## 🚀 Para Usuários Apressados (2 minutos)

### 🐳 **MÉTODO RECOMENDADO: Docker**

**Resolve problemas do Python 3.12+ automaticamente!**

#### 1️⃣ Instalação e Execução Docker

**Linux/macOS:**
```bash
bash start-docker.sh
```

**Windows:**
```cmd
start-docker.bat
```

**OU comandos manuais:**
```bash
docker-compose up --build -d
```

#### 2️⃣ Acessar Sistema

1. **Abrir:** http://localhost:8501
2. **Login:** `admin` / `admin123`
3. **Testar:** Triagem Médica → Processar formulário

#### 3️⃣ ESP32 (Opcional)

1. **Wokwi:** https://wokwi.com
2. **Código:** `esp32_temperature_sensor.ino`
3. **Testar:** Dashboard IoT → Controle Remoto

---

## 🐍 **Método Alternativo: Python Local (3.8-3.11)**

⚠️ **ATENÇÃO:** Se você tem Python 3.12+, use Docker acima!

### Instalação Automática

**Linux/macOS:**
```bash
bash install.sh
```

**Windows:**
```cmd
install.bat
```

### Executar Sistema

```bash
# Ativar ambiente
source venv/bin/activate        # Linux/macOS
# OU
venv\Scripts\activate          # Windows

# Iniciar aplicação
streamlit run app.py
```

---

## 📋 Requirements.txt Atualizado (Compatível)

```
streamlit==1.28.1      # Interface web principal
pandas==2.0.3          # Manipulação de dados (compatível 3.9-3.11)
numpy==1.24.3          # Computação numérica
scikit-learn==1.3.0    # Machine Learning (compatível)
joblib==1.3.2          # Serialização de modelos
plotly==5.17.0         # Gráficos interativos
seaborn==0.12.2        # Visualização estatística
matplotlib==3.7.2      # Plots básicos
cryptography==41.0.4   # Criptografia de dados
flask==2.3.3           # API REST para IoT
requests==2.31.0       # Cliente HTTP
python-dateutil==2.8.2 # Manipulação de datas
bcrypt==4.0.1          # Hash de senhas
paho-mqtt==1.6.1       # Cliente MQTT (NOVO!)
```

## 🎯 Comandos Essenciais

### Docker (Recomendado)

```bash
# Iniciar sistema
bash start-docker.sh

# Ver logs
docker-compose logs -f

# Parar sistema
docker-compose down

# Status
docker-compose ps
```

### Python Local (Se 3.8-3.11)

```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate          # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar aplicação
streamlit run app.py
```

## 🛠️ Solução de Problemas

### ❌ Python 3.12+ Incompatível

```bash
# Erro típico: "Cannot import 'setuptools.build_meta'"
# SOLUÇÃO: Use Docker!

bash start-docker.sh        # Linux/macOS
start-docker.bat           # Windows
```

### ❌ Outros Erros

```bash
# Docker: Porta ocupada
docker-compose down
docker-compose up -d

# Python: Erro de módulo
pip install --upgrade -r requirements.txt

# Porta ocupada (Python)
streamlit run app.py --server.port 8502

# Verificar MQTT
python -c "import paho.mqtt.client; print('MQTT OK')"
```

## 🏥 Fluxo de Teste Completo

### Teste Básico (2 minutos)
1. Login → Triagem Médica
2. Idade: `25`, Temperatura: `38.1`
3. Sintomas: `febre`, `dor_cabeca`
4. Processar → Ver resultado

### Teste IoT (5 minutos)
1. Wokwi → ESP32 → `esp32_temperature_sensor.ino`
2. Dashboard IoT → Status MQTT: 🟢
3. Triagem → "📏 Medir Temperatura"
4. Aguardar → "🔄 Atualizar IoT"
5. Temperatura automática → Processar

### Teste Completo (10 minutos)
1. **Admin:** Login → Dashboard IoT → Controle Remoto
2. **Médico:** Triagem com MQTT → Estatísticas
3. **Enfermeiro:** Histórico → Monitoramento

## 📁 Estrutura Mínima

```
GS-2/
├── 🐳 DOCKER (NOVO!)
│   ├── Dockerfile              # ← Imagem otimizada Python 3.9
│   ├── docker-compose.yml     # ← Orquestração
│   ├── start-docker.sh        # ← Script Linux/macOS
│   └── start-docker.bat       # ← Script Windows
├── 📱 APLICAÇÃO
│   ├── app.py                 # ← Principal
│   ├── triagem_model.py       # ← IA
│   ├── mqtt_manager.py        # ← MQTT
│   └── iot_dashboard.py       # ← IoT
├── 🔧 CONFIGURAÇÃO
│   ├── requirements.txt       # ← Dependências (atualizado)
│   ├── install.sh            # ← Auto-install Linux/macOS
│   └── install.bat           # ← Auto-install Windows
└── 📚 DOCUMENTAÇÃO
    ├── README.md             # ← Guia completo
    └── QUICK_START.md        # ← Este arquivo
```

## 🐳 Vantagens do Docker

- ✅ **Zero configuração** de Python
- ✅ **Funciona em qualquer SO**
- ✅ **Resolve incompatibilidades** automaticamente
- ✅ **Dependências isoladas**
- ✅ **Fácil deploy** e distribuição
- ✅ **Backup simples** via volumes

## 🎉 Pronto!

### Via Docker (Recomendado):
- ✅ **Sistema funcionando** em http://localhost:8501
- ✅ **Zero configuração Python**
- ✅ **Compatível com Python 3.12+**
- ✅ **MQTT integrado** com ESP32
- ✅ **Controle remoto** via interface web

### Via Python Local (3.8-3.11):
- ✅ **Sistema funcionando** em http://localhost:8501
- ✅ **MQTT integrado** com ESP32
- ✅ **Controle remoto** via interface web
- ✅ **Triagem com IA** para 15 doenças
- ✅ **Dashboard IoT** em tempo real

**📚 Guia completo:** README.md  
**🎮 Setup ESP32:** MQTT_SETUP_GUIDE.md

**🎯 Comando principal:** `bash start-docker.sh` (Linux/macOS) ou `start-docker.bat` (Windows) 