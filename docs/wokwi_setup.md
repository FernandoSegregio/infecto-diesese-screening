# 🌡️ Configuração ESP32 no Wokwi - Passo a Passo

## 🚀 **Método 1: Criar Projeto Novo**

### **1. Acessar Wokwi:**
- Vá para: https://wokwi.com
- Faça login (se necessário)

### **2. Criar Projeto ESP32:**
- Clique em **"New Project"**
- Selecione **"Arduino ESP32"** (NÃO "ESP32 C")
- Nome do projeto: "ESP32 Temperature Sensor"

### **3. Configurar Arquivo Principal:**
- Renomeie `sketch.ino` para `esp32_sensor.ino`
- Apague todo o conteúdo
- Cole o código do arquivo `esp32_temperature_sensor.ino`

### **4. Adicionar Componentes:**
- Clique no **"+"** para adicionar componentes
- Adicione os seguintes componentes:

#### **Componentes Necessários:**
```
- ESP32 DevKit V1 (já incluído)
- DS18B20 Temperature Sensor
- SSD1306 OLED Display (128x64)
- LED (3x - Verde, Amarelo, Vermelho)
- Buzzer
- Pushbutton
- Resistor 4.7kΩ (pull-up DS18B20)
- Resistor 220Ω (3x - para LEDs)
```

### **5. Fazer Conexões:**
```
ESP32 Pin    →    Componente
D4           →    DS18B20 (Data)
D21          →    OLED (SDA)
D22          →    OLED (SCL)
D2           →    LED Verde
D15          →    LED Amarelo
D16          →    LED Vermelho
D17          →    Buzzer
D18          →    Botão
3V3          →    Alimentação (+)
GND          →    Terra (-)
```

## 🔧 **Método 2: Usar Diagram.json**

### **1. Criar Projeto Vazio:**
- Novo projeto Arduino ESP32
- Apagar componentes padrão

### **2. Importar Circuito:**
- Clique em **"diagram.json"** (aba ao lado do código)
- Apague conteúdo atual
- Cole o conteúdo do arquivo `diagram.json` do projeto

### **3. Adicionar Código:**
- Volte para aba do código
- Cole o código do `esp32_temperature_sensor.ino`

## 🌐 **Método 3: Link Direto (Mais Fácil)**

### **Template Pronto:**
```
https://wokwi.com/projects/new/esp32
```

### **Configuração Rápida:**
1. Acesse o link acima
2. Cole o código abaixo no editor
3. Adicione os componentes manualmente

## 📋 **Código Simplificado para Teste:**

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Configurações WiFi
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// Configurações do servidor
const char* serverURL = "http://localhost:5002/api/sensor-data";

// Variáveis globais
String deviceID = "ESP32_TEMP_001";
float temperature = 36.5;

void setup() {
  Serial.begin(115200);
  Serial.println("🌡️ Iniciando Sensor de Temperatura IoT");
  
  // Conectar WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi conectado!");
}

void loop() {
  // Simular temperatura
  temperature = 36.0 + random(0, 40) / 10.0; // 36.0 a 40.0°C
  
  Serial.print("🌡️ Temperatura: ");
  Serial.print(temperature);
  Serial.println("°C");
  
  // Enviar dados
  sendToServer(temperature);
  
  delay(10000); // 10 segundos
}

void sendToServer(float temp) {
  if(WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");
    
    // Criar JSON
    StaticJsonDocument<200> doc;
    doc["device_id"] = deviceID;
    doc["sensor_type"] = "temperature";
    doc["value"] = temp;
    doc["unit"] = "°C";
    doc["location"] = "Wokwi Simulator";
    doc["battery_level"] = 100;
    doc["firmware_version"] = "1.0.0";
    
    String jsonString;
    serializeJson(doc, jsonString);
    
    int httpResponseCode = http.POST(jsonString);
    
    if(httpResponseCode > 0) {
      Serial.println("✅ Dados enviados com sucesso!");
      Serial.println("📨 Código: " + String(httpResponseCode));
    } else {
      Serial.println("❌ Erro no envio: " + String(httpResponseCode));
    }
    
    http.end();
  }
}
```

## 🔍 **Verificação de Erros:**

### **1. Arquivo deve ser .ino:**
- ✅ `esp32_sensor.ino`
- ❌ `main.c`

### **2. Projeto deve ser Arduino ESP32:**
- ✅ "Arduino ESP32"
- ❌ "ESP32 C"

### **3. Bibliotecas necessárias:**
```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
```

## 🎯 **Teste Rápido:**

1. **Cole o código simplificado** acima
2. **Execute a simulação**
3. **Verifique o monitor serial**
4. **Confirme se dados chegam na API**

Se funcionar, depois adicione os componentes extras (OLED, LEDs, etc.)!

## 📞 **Se ainda der erro:**

1. **Tente o código simplificado primeiro**
2. **Verifique se é projeto Arduino ESP32**
3. **Confirme extensão .ino**
4. **Teste sem componentes extras** 