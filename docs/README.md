# 🏥 Sistema de IA para Triagem Médica com IoT

# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
    <a href="https://www.fiap.com.br/">
        <img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%>
    </a>
</p>

<br>

# Nome do projeto

```
FarmTech Solutions - Sistema Completo de Automação Agrícola
```

## Nome do grupo

```
TriagemSem Fronteiras
```

## 👨‍🎓 Integrantes:

- <a href="https://www.linkedin.com/in/fernando-segregio/">Fernando Segregio</a>    

## 👩‍🏫 Professores:

### Tutor(a) 
- <a href="https://www.linkedin.com/in/leonardoorabona/">Leonardo Ruiz Orabona</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/profandregodoi/">André Godoi</a>

Sistema completo de triagem médica com inteligência artificial, integração IoT via MQTT e controle remoto de sensores ESP32.

## 🎯 Funcionalidades Principais

- ✅ **Triagem Médica com IA** - 15 doenças para áreas vulneráveis
- ✅ **Controle Remoto MQTT** - Comando de sensores ESP32 via interface web
- ✅ **Dashboard IoT** - Monitoramento em tempo real de temperatura
- ✅ **Histórico e Estatísticas** - Análise epidemiológica completa
- ✅ **Sistema de Autenticação** - Controle de acesso por perfis
- ✅ **Auditoria e Segurança** - Log completo de atividades

## 🚀 Como Rodar a Aplicação (3 Métodos)

### ⭐ **Método 1: Docker (RECOMENDADO)**

**Para resolver problemas de compatibilidade do Python 3.12+**

#### Pré-requisitos:
- **Docker Desktop** - [Download aqui](https://docs.docker.com/get-docker/)

#### Execução:

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
# Construir e iniciar
docker-compose up --build -d

# Acessar: http://localhost:8501
```

#### Vantagens Docker:
- ✅ **Não requer Python local**
- ✅ **Dependências pré-configuradas**
- ✅ **Compatível com qualquer SO**
- ✅ **Isolamento completo**
- ✅ **Resolve problemas de versão**

---

### 📦 **Método 2: Instalação Local (Python 3.8-3.11)**

⚠️ **Atenção:** Python 3.12+ tem problemas de compatibilidade. Use Docker se tiver 3.12+.

#### Pré-requisitos:
- **Python 3.8-3.11** - [Download aqui](https://www.python.org/downloads/)
- **Git** - [Download aqui](https://git-scm.com/downloads/)

#### Instalação Automática:

**Linux/macOS:**
```bash
bash install.sh
```

**Windows:**
```cmd
install.bat
```

#### Instalação Manual:
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

---

### ⚡ **Método 3: Início Super Rápido**

```bash
# Se você já tem Python 3.8-3.11 configurado
pip install -r requirements.txt
streamlit run app.py
```

## 🌐 Acessar a Aplicação

1. **Abrir navegador** em: http://localhost:8501
2. **Aguardar carregar** (primeira vez pode demorar 30-60s)
3. **Fazer login** com credenciais padrão:

**Usuários Pré-configurados:**

| Usuário | Senha | Perfil | Permissões |
|---------|-------|--------|------------|
| `admin` | `admin123` | Administrador | Todas |
| `medico` | `medico123` | Médico | Triagem + IoT |
| `enfermeiro` | `enfermeiro123` | Enfermeiro | Triagem + Histórico |

## 🎮 Configurar Sistema MQTT (ESP32)

### ESP32 no Wokwi

#### Acesse o link abaixo, ou use o passo a passo para fazer manualmente:

https://wokwi.com/projects/432976719461101569


1. **Acessar:** https://wokwi.com
2. **Criar projeto** Arduino ESP32
3. **Colar código** de `esp32_temperature_sensor.ino`
4. **Adicionar componentes:**
   - ESP32 DevKit V1
   - 3x LEDs (Verde, Amarelo, Vermelho)
   - Buzzer
   - Botão
   - Potenciômetro (simula sensor temperatura)
   - Resistores de proteção

### Código ESP32 (Já Configurado)

```cpp
// Credenciais MQTT (já incluídas no código)
const char* mqtt_server = "91c5f1ea0f494ccebe45208ea8ffceff.s1.eu.hivemq.cloud";
const char* mqtt_user = "FARM_TECH";
const char* mqtt_password = "Pato1234";

// Tópicos MQTT
const char* command_topic = "termometro/comando";  // Recebe comandos
const char* temperature_topic = "termometro/temperatura";  // Envia dados
```

## ✅ Testar o Sistema Completo

### Teste 1: Interface Web
```bash
# Verificar se carregou corretamente
curl http://localhost:8501
```

### Teste 2: Sistema MQTT
1. **Iniciar simulação ESP32** no Wokwi
2. **Acessar "Dashboard IoT"** na aplicação  
3. **Verificar status:** 🟢 MQTT Conectado
4. **Testar comando:** Botão "📏 Medir Temperatura"

### Teste 3: Triagem Médica
1. **Acessar "Triagem Médica"**
2. **Clicar "📏 Medir Temperatura"** (controle remoto)
3. **Aguardar 3-5 segundos**
4. **Clicar "🔄 Atualizar IoT"**
5. **Verificar temperatura** preenchida automaticamente
6. **Processar triagem** normalmente

## 🛠️ Solução de Problemas Comuns

### ❌ Python 3.12+ Incompatível

```bash
# Erro: "Cannot import 'setuptools.build_meta'"
# SOLUÇÃO: Use Docker!

bash start-docker.sh        # Linux/macOS
start-docker.bat           # Windows
```

### ❌ Erro: "ModuleNotFoundError" (Python Local)

```bash
# Verificar se ambiente virtual está ativo
which python  # Deve apontar para venv

# Reinstalar dependências
pip install -r requirements.txt --upgrade
```

### ❌ Erro: "Port 8501 already in use"

```bash
# Docker
docker-compose down
docker-compose up -d

# Python local
streamlit run app.py --server.port 8502
```

### ❌ Docker Não Inicia

```bash
# Verificar se Docker está rodando
docker version

# Ver logs de erro
docker-compose logs

# Reconstruir imagem
docker-compose up --build --force-recreate
```

### ❌ MQTT Não Conecta

```bash
# Verificar internet
ping google.com

# Reiniciar aplicação
docker-compose restart    # Docker
# OU
streamlit run app.py     # Python local
```

## 🐳 Comandos Docker Úteis

```bash
# Iniciar sistema
bash start-docker.sh

# Ver logs em tempo real
docker-compose logs -f

# Parar sistema
docker-compose down

# Reiniciar
docker-compose restart

# Status dos containers
docker-compose ps

# Acessar container
docker-compose exec triagem-medica bash

# Limpar tudo
docker-compose down -v
docker system prune -f
```

## 📁 Estrutura do Projeto

```
GS-2/
├── 🐳 DOCKER
│   ├── Dockerfile               # Imagem Docker otimizada
│   ├── docker-compose.yml      # Orquestração de containers
│   ├── start-docker.sh         # Script Linux/macOS
│   └── start-docker.bat        # Script Windows
├── 📱 APLICAÇÃO
│   ├── app.py                  # Aplicação principal Streamlit
│   ├── triagem_model.py        # Modelo de IA para triagem
│   ├── mqtt_manager.py         # Cliente MQTT para ESP32
│   ├── iot_dashboard.py        # Dashboard IoT
│   ├── auth.py                 # Sistema de autenticação
│   └── security.py            # Segurança e validação
├── 🔧 CONFIGURAÇÃO
│   ├── requirements.txt        # Dependências Python (atualizado)
│   ├── config.py              # Configurações do sistema
│   ├── install.sh             # Instalação Python Linux/macOS
│   └── install.bat            # Instalação Python Windows
├── 🎮 IoT/ESP32
│   ├── esp32_temperature_sensor.ino  # Código Arduino ESP32
│   └── MQTT_SETUP_GUIDE.md    # Guia detalhado MQTT
├── 📚 DOCUMENTAÇÃO
│   ├── README.md              # Este arquivo
│   └── QUICK_START.md         # Início rápido
└── 📊 DADOS (criados automaticamente)
    ├── data/
    │   ├── users.json         # Usuários cadastrados
    │   ├── iot_devices.json   # Dispositivos IoT
    │   └── iot_readings.json  # Leituras dos sensores
    └── logs/
        └── audit.log          # Log de auditoria
```

## 📋 Requirements.txt Atualizado

```
streamlit==1.28.1      # Interface web principal
pandas==2.0.3          # Manipulação de dados (compatível)
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
paho-mqtt==1.6.1       # Cliente MQTT
```

## 🎯 Fluxo de Uso Típico

### 1. **Profissional de Saúde:**
```
Login → Triagem Médica → Medir Temperatura (MQTT) → 
Preencher Formulário → Processar IA → Ver Resultado
```

### 2. **Administrador:**
```
Login → Dashboard IoT → Monitorar Dispositivos → 
Controlar Remotamente → Ver Estatísticas → Auditoria
```

### 3. **Técnico:**
```
Configurar ESP32 → Registrar Dispositivo → 
Testar Conectividade → Monitorar Funcionamento
```

## 🔐 Segurança e Backup

### Backup dos Dados (Docker)
```bash
# Criar backup dos volumes
docker run --rm -v gs-2_triagem-data:/data -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz -C /data .

# Restaurar backup
docker run --rm -v gs-2_triagem-data:/data -v $(pwd):/backup alpine tar xzf /backup/backup.tar.gz -C /data
```

### Backup dos Dados (Local)
```bash
# Criar backup
mkdir backup_$(date +%Y%m%d)
cp data/*.json backup_$(date +%Y%m%d)/
cp logs/audit.log backup_$(date +%Y%m%d)/
```

### Configurações de Segurança
- ✅ Senhas criptografadas com bcrypt
- ✅ Autenticação obrigatória
- ✅ Log de auditoria completo
- ✅ Validação de dados médicos
- ✅ Controle de acesso por perfis
- ✅ Isolamento via containers Docker

## 🌐 Acesso Externo (Opcional)

**⚠️ ATENÇÃO: Apenas para ambientes controlados**

### Docker:
```bash
# Modificar docker-compose.yml
ports:
  - "0.0.0.0:8501:8501"

# Acessar de outros dispositivos
http://[IP_DO_SERVIDOR]:8501
```

### Python Local:
```bash
streamlit run app.py --server.address 0.0.0.0
```

## 🆘 Suporte e Contato

Em caso de problemas:

1. **🐳 PRIMEIRA OPÇÃO: Use Docker** (`bash start-docker.sh`)
2. **Verificar logs** no terminal
3. **Consultar seção** "Solução de Problemas"
4. **Verificar requisitos** de sistema
5. **Testar passo a passo** conforme este guia

---

## 🎉 Sistema Pronto!

### Via Docker (Recomendado):
- ✅ **Aplicação web** rodando em http://localhost:8501
- ✅ **Zero configuração** de Python
- ✅ **Compatível com qualquer SO**
- ✅ **Dependências isoladas**

### Via Python Local:
- ✅ **Aplicação web** rodando em http://localhost:8501
- ✅ **Sistema MQTT** conectado ao ESP32
- ✅ **Controle remoto** de sensores via interface web
- ✅ **Dashboard IoT** em tempo real
- ✅ **Triagem médica** com IA integrada
- ✅ **Monitoramento completo** de dispositivos

**🎯 Próximo passo:** Execute `bash start-docker.sh` e acesse http://localhost:8501! 
