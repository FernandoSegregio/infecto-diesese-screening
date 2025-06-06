# 🌡️ Sistema IoT - Sensores de Temperatura

## 📋 Visão Geral

O Sistema IoT integra sensores de temperatura ESP32 ao sistema de triagem médica, permitindo medição automática e monitoramento em tempo real da temperatura corporal dos pacientes.

## 🏗️ Arquitetura do Sistema

```
ESP32 (Wokwi) → WiFi → API Flask → Sistema Streamlit → Dashboard IoT
```

### Componentes Principais:

1. **ESP32 + Sensores** (Hardware Virtual no Wokwi)
2. **API REST** (Flask - Porta 5002)
3. **Dashboard IoT** (Streamlit)
4. **Integração Automática** (Triagem Médica)

## 🔧 Hardware Virtual (Wokwi)

### Componentes do Circuito:
- **ESP32 DevKit V1** - Microcontrolador principal
- **DS18B20** - Sensor de temperatura digital
- **Display OLED 128x64** - Feedback visual
- **3x LEDs** (Verde, Amarelo, Vermelho) - Indicadores de status
- **Buzzer** - Alertas sonoros
- **Botão** - Medição manual
- **Resistores** - Proteção e pull-up

### Pinagem:
```
ESP32          Componente
D4    ←→       DS18B20 (Data)
D21   ←→       OLED (SDA)
D22   ←→       OLED (SCL)
D2    ←→       LED Verde
D15   ←→       LED Amarelo
D16   ←→       LED Vermelho
D17   ←→       Buzzer
D18   ←→       Botão
3V3   ←→       Alimentação
GND   ←→       Terra
```

## 📡 Comunicação e Protocolos

### API REST Endpoints:

#### 1. Receber Dados do Sensor
```http
POST /api/sensor-data
Content-Type: application/json

{
  "device_id": "ESP32_TEMP_001",
  "sensor_type": "temperature",
  "value": 36.5,
  "unit": "°C",
  "location": "Recepção - Posto 1",
  "battery_level": 85,
  "firmware_version": "1.0.0"
}
```

#### 2. Status do Dispositivo
```http
GET /api/device-status/{device_id}
```

#### 3. Health Check
```http
GET /api/health
```

### Resposta de Sucesso:
```json
{
  "status": "success",
  "reading_id": 123,
  "timestamp": "2024-06-03T21:30:45.123456",
  "message": "Data received successfully"
}
```

## 🚀 Como Usar

### 1. Configurar o ESP32 no Wokwi

1. **Acesse o Wokwi:** https://wokwi.com
2. **Crie um novo projeto** ESP32
3. **Copie o código** do arquivo `esp32_temperature_sensor.ino`
4. **Importe o diagrama** do arquivo `diagram.json`
5. **Configure as bibliotecas** necessárias

### 2. Configurar o Sistema

1. **Registrar Dispositivo:**
   - Acesse "🌡️ Dashboard IoT" → "🔧 Dispositivos"
   - Clique em "➕ Registrar Novo Dispositivo"
   - Preencha: ID, Nome, Tipo, Localização

2. **Iniciar Servidor API:**
   - O servidor inicia automaticamente na porta 5002
   - Verificar status no dashboard

### 3. Executar Simulação

1. **No Wokwi:**
   - Clique em "▶️ Start Simulation"
   - Aguarde conexão WiFi
   - Observe o display OLED

2. **Medições:**
   - **Automática:** A cada 10 segundos
   - **Manual:** Pressione o botão azul
   - **Temperatura:** Clique no sensor DS18B20 para alterar

### 4. Monitorar no Dashboard

1. **Acesse:** "🌡️ Dashboard IoT"
2. **Visualize:**
   - Dispositivos online
   - Leituras em tempo real
   - Alertas de temperatura
   - Histórico de dados

## 📊 Funcionalidades do Dashboard

### 📡 Monitoramento em Tempo Real
- Status de dispositivos online/offline
- Métricas de leituras (24h)
- Contagem de casos de febre
- Temperatura média
- Gráficos em tempo real
- Últimas leituras

### 🔧 Gerenciamento de Dispositivos
- Registrar novos sensores
- Visualizar status e localização
- Monitorar bateria e firmware
- Última comunicação

### 📈 Histórico e Análise
- Filtros por período e dispositivo
- Estatísticas detalhadas
- Gráficos de tendência
- Distribuição de temperaturas
- Exportação de dados (CSV)

### ⚙️ Configurações
- Limites de temperatura
- Intervalos de leitura
- Configurações de conectividade
- Teste de simulação

## 🚨 Sistema de Alertas

### Níveis de Temperatura:
- **🟢 Normal:** < 37.8°C
- **🟡 Febre:** 37.8°C - 39.0°C
- **🔴 Crítico:** > 39.0°C
- **🔵 Baixa:** < 35.0°C

### Indicadores Visuais:
- **LEDs:** Cores correspondentes aos níveis
- **Display:** Temperatura e status
- **Buzzer:** Alertas sonoros
- **Dashboard:** Notificações em tempo real

## 🔗 Integração com Triagem

### Preenchimento Automático:
1. **Detecção:** Sistema verifica sensores ativos
2. **Última Leitura:** Busca temperatura dos últimos 5 minutos
3. **Sugestão:** Exibe temperatura detectada
4. **Aplicação:** Botão para usar valor automaticamente

### Benefícios:
- ✅ Reduz erros de digitação
- ✅ Acelera o processo de triagem
- ✅ Garante precisão das medições
- ✅ Rastreabilidade completa

## 📁 Estrutura de Arquivos

```
projeto/
├── iot_manager.py          # Gerenciador IoT principal
├── iot_dashboard.py        # Dashboard Streamlit
├── esp32_temperature_sensor.ino  # Código ESP32
├── diagram.json            # Circuito Wokwi
├── iot_devices.json        # Dispositivos registrados
├── iot_readings.json       # Leituras dos sensores
└── README_IOT.md          # Esta documentação
```

## 🔒 Segurança e Auditoria

### Logs de Auditoria:
- Acesso ao dashboard IoT
- Registro de dispositivos
- Recebimento de dados
- Alertas gerados

### Validação de Dados:
- Verificação de campos obrigatórios
- Validação de faixas de temperatura
- Controle de dispositivos autorizados
- Timestamps para rastreabilidade

## 🛠️ Solução de Problemas

### Problemas Comuns:

#### 1. ESP32 não conecta ao WiFi
- **Verificar:** Credenciais WiFi no código
- **Solução:** Usar "Wokwi-GUEST" (sem senha)

#### 2. Dados não chegam ao sistema
- **Verificar:** URL do servidor no código ESP32
- **Solução:** Usar `http://localhost:5002/api/sensor-data`

#### 3. Sensor não detecta temperatura
- **Verificar:** Conexões do DS18B20
- **Solução:** Verificar pinagem e resistor pull-up

#### 4. Dashboard não mostra dispositivos
- **Verificar:** Dispositivo registrado
- **Solução:** Registrar na aba "Dispositivos"

### Logs de Debug:
- **ESP32:** Monitor Serial no Wokwi
- **Sistema:** Console do Streamlit
- **API:** Logs do Flask

## 🚀 Expansões Futuras

### Sensores Adicionais:
- 💓 Oxímetro (SpO2)
- 🩺 Pressão arterial
- ⚖️ Balança inteligente
- 🫁 Frequência respiratória

### Conectividade:
- 📶 MQTT para múltiplos dispositivos
- ☁️ Cloud IoT
- 📱 App mobile
- 📞 Notificações push

### Análise Avançada:
- 🤖 ML para detecção de anomalias
- 📊 Predição de surtos
- 🗺️ Mapeamento geográfico
- 📈 Análise epidemiológica

## 📞 Suporte

Para dúvidas ou problemas:
1. Consulte esta documentação
2. Verifique os logs de sistema
3. Teste com simulação de dados
4. Contate o administrador do sistema

---

**Desenvolvido para o Sistema de Triagem Médica em Áreas Vulneráveis**  
*Integração IoT para medição automática de temperatura corporal* 