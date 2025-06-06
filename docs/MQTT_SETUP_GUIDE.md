# 🌡️ Guia Completo - Sistema MQTT com Controle Remoto ESP32

## 📋 Visão Geral

O sistema agora oferece **controle remoto completo** dos sensores ESP32 via MQTT, permitindo solicitar medições de temperatura diretamente da interface web.

## 🏗️ Arquitetura do Sistema

```
Interface Web → Comando MQTT → HiveMQ Cloud → ESP32 → Medição → MQTT → Sistema Python → Dashboard
```

### Fluxo de Controle Remoto:

1. **👆 Usuário clica** no botão "Medir Temperatura" na interface web
2. **📤 Sistema envia** comando MQTT para ESP32
3. **🎯 ESP32 recebe** comando e faz medição imediata
4. **📡 ESP32 publica** resultado no tópico de temperatura
5. **📊 Dashboard atualiza** automaticamente com nova leitura
6. **🔄 Triagem médica** pode usar temperatura automaticamente

## 🎮 Controles Disponíveis

### 1. Na Página de Triagem Médica

#### 🌡️ Solicitação de Medição
- **Botão:** "📏 Medir Temperatura"
- **Função:** Solicita medição imediata do ESP32
- **Feedback:** Confirmação visual + balloons
- **Status:** Mostra conexão MQTT em tempo real

```
🎮 Controle Remoto do Termômetro ESP32
┌─────────────────────────────────────┐
│ 🌡️ Solicitação de medição via MQTT  │
│ Use o botão abaixo para solicitar   │
│ uma medição imediata do ESP32       │
├──────────────┬──────────────────────┤
│ 📏 Medir     │ Status MQTT:         │
│ Temperatura  │ 🟢 Conectado         │
└──────────────┴──────────────────────┘
```

### 2. No Dashboard IoT

#### 🎯 Comandos Disponíveis
- **🌡️ Medir Temperatura Agora:** Solicita leitura imediata
- **📊 Solicitar Status:** Obtém status completo do dispositivo
- **🔧 Testar LEDs/Buzzer:** Testa hardware remotamente

#### ⚙️ Comando Personalizado
- Campo para enviar comandos customizados
- Histórico dos últimos 20 comandos enviados
- Status detalhado da conexão MQTT

## 🚀 Como Usar - Passo a Passo

### 1. Configurar o ESP32 no Wokwi

1. **Acesse:** https://wokwi.com
2. **Cole o código atualizado** com controle remoto
3. **Inicie a simulação** (▶️)
4. **Aguarde:** "SISTEMA CONECTADO MQTT COM CONTROLE REMOTO!"

### 2. Verificar Conexão no Sistema

1. **Acesse** http://localhost:8501
2. **Vá para** "🌡️ Dashboard IoT"
3. **Verifique** status MQTT no topo: 🟢 MQTT Conectado

### 3. Usar Controle Remoto na Triagem

1. **Vá para** "🩺 Triagem Médica"
2. **Seção** "🎮 Controle Remoto do Termômetro ESP32"
3. **Clique** "📏 Medir Temperatura"
4. **Aguarde** confirmação: "✅ Comando enviado!"
5. **Aguarde 3-5 segundos** para medição
6. **Clique** "🔄 Atualizar IoT" para ver nova temperatura
7. **Preencha** formulário (temperatura será preenchida automaticamente)

### 4. Usar Controle Avançado no Dashboard

1. **Acesse** aba "🎮 Controle Remoto MQTT"
2. **Selecione** dispositivo (se houver múltiplos)
3. **Use botões:**
   - **📏 Medir Temperatura Agora**
   - **📋 Solicitar Status** 
   - **💡 Testar LEDs/Buzzer**
4. **Monitore** resultados na aba "📡 Monitoramento"

## 📡 Tópicos MQTT

### Comandos (Web → ESP32)

**Tópico:** `termometro/comando`

```json
{
  "command": "measure_temperature",
  "device_id": "ESP32_TERMOMETRO_001", 
  "timestamp": 1701234567890,
  "source": "TriagemMedica_Dashboard",
  "action": "start_reading",
  "priority": "high"
}
```

### Comandos Disponíveis:

| Comando | Descrição | Ação no ESP32 |
|---------|-----------|---------------|
| `measure_temperature` | Solicita medição imediata | LED amarelo + medição + envio MQTT |
| `get_status` | Solicita status completo | Envia dados detalhados do dispositivo |
| `test_leds` | Testa hardware | Sequência de LEDs + buzzer |

### Respostas (ESP32 → Web)

**Medição de Temperatura:**
```json
{
  "device_id": "ESP32_TERMOMETRO_001",
  "sensor_type": "temperature", 
  "value": 37.2,
  "unit": "°C",
  "location": "Recepção - Posto 1",
  "battery_level": 85,
  "timestamp": 1701234567890
}
```

**Status do Dispositivo:**
```json
{
  "device_id": "ESP32_TERMOMETRO_001",
  "status": "online",
  "temperature": 37.2,
  "location": "Recepção - Posto 1", 
  "battery_level": 85,
  "wifi_rssi": -45,
  "free_memory": 234567,
  "uptime": 3600000,
  "firmware": "2.0.0",
  "timestamp": 1701234567890
}
```

## 💡 Recursos do ESP32

### Feedback Visual e Sonoro:
- **LED Verde:** Temperatura normal
- **LED Amarelo:** Febre detectada / Comando recebido
- **LED Vermelho:** Temperatura crítica/baixa
- **Buzzer:** Alertas sonoros diferenciados

### Comandos Reconhecidos:
- ✅ `measure_temperature` - Medição imediata
- ✅ `get_status` - Status completo 
- ✅ `test_leds` - Teste de hardware
- ❓ Outros comandos retornam "unknown_command"

## 🔧 Solução de Problemas

### MQTT Desconectado
```
❌ MQTT não conectado ao broker
🔄 Aguarde a conexão ou reinicie o sistema
```

**Soluções:**
1. Reiniciar aplicação: `streamlit run app.py`
2. Verificar internet
3. Verificar credenciais HiveMQ

### Comando Não Funciona
```
❌ Falha ao enviar comando MQTT
```

**Verificar:**
1. ESP32 está conectado no Wokwi
2. Console do ESP32 mostra: "Subscrito ao tópico de comandos"
3. Status MQTT: 🟢 Conectado

### ESP32 Não Responde
```
🕐 Aguarde alguns segundos para a leitura aparecer
```

**Verificar no Console ESP32:**
- Deve mostrar: "🎮 COMANDO RECEBIDO VIA MQTT!"
- Se não aparecer, reiniciar simulação Wokwi

## 📊 Monitoramento

### Dashboard IoT
- **Status em tempo real** de conexão MQTT
- **Histórico de comandos** enviados
- **Monitoramento de respostas** dos dispositivos
- **Gráficos atualizados** automaticamente

### Logs do Sistema
- Console Python mostra todos os comandos enviados
- Console ESP32 mostra comandos recebidos e processados
- Histórico mantido no Streamlit session state

## 🎯 Fluxo Típico de Uso

```
1. 👨‍⚕️ Profissional acessa triagem médica
2. 🎮 Clica "📏 Medir Temperatura" 
3. ⚡ Sistema envia comando MQTT
4. 📡 ESP32 recebe e faz medição
5. 🌡️ Temperatura publicada no MQTT
6. 📊 Sistema recebe e processa
7. 🔄 Usuário clica "Atualizar IoT"
8. ✅ Temperatura aparece automaticamente
9. 📝 Formulário preenchido com temperatura
10. 🩺 Triagem processada com dados reais
```

## ⚙️ Configurações Avançadas

### Múltiplos Dispositivos
- Selecionar dispositivo específico no dashboard
- Comandos direcionados por `device_id`
- Monitoramento individual por dispositivo

### Comandos Personalizados
- Campo para comandos customizados
- Extensibilidade para novos tipos de comando
- Log completo de atividades

---

**🎉 Sistema totalmente funcional para controle remoto via MQTT!**

Agora você pode controlar o ESP32 remotamente através da interface web, solicitar medições sob demanda e integrar automaticamente com o sistema de triagem médica. 