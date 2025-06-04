#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Configurações WiFi
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// Configurações do servidor
const char* serverURL = "http://localhost:5001/api/sensor-data";

// Configurações do sensor DS18B20
#define ONE_WIRE_BUS 4
#define TEMPERATURE_PRECISION 12

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// Configurações do display OLED
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

// Configurações dos LEDs e botão
#define LED_GREEN 2
#define LED_YELLOW 15
#define LED_RED 16
#define BUZZER_PIN 17
#define BUTTON_PIN 18

// Variáveis globais
String deviceID = "ESP32_TEMP_001";
String location = "Recepção - Posto 1";
unsigned long lastReading = 0;
const unsigned long readingInterval = 10000; // 10 segundos
bool buttonPressed = false;
int batteryLevel = 100;

void setup() {
  Serial.begin(115200);
  Serial.println("🌡️ Iniciando Sensor de Temperatura IoT");
  
  // Inicializar pinos
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_YELLOW, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  // Teste inicial dos LEDs
  testLEDs();
  
  // Inicializar display
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("❌ Falha ao inicializar display OLED");
    for(;;);
  }
  
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0,0);
  display.println("Iniciando...");
  display.display();
  
  // Inicializar sensor de temperatura
  sensors.begin();
  sensors.setResolution(TEMPERATURE_PRECISION);
  
  Serial.println("🔧 Sensor DS18B20 inicializado");
  
  // Conectar WiFi
  connectWiFi();
  
  // Registrar dispositivo
  registerDevice();
  
  Serial.println("✅ Sistema iniciado com sucesso!");
  updateDisplay("Sistema Pronto", "Pressione botao", "para medir");
  setLED("green");
  
  // Beep de inicialização
  playTone(1000, 200);
  delay(100);
  playTone(1500, 200);
}

void loop() {
  // Verificar botão
  if (digitalRead(BUTTON_PIN) == LOW && !buttonPressed) {
    buttonPressed = true;
    Serial.println("🔘 Botão pressionado - Iniciando medição manual");
    measureAndSend();
    delay(1000); // Debounce
  } else if (digitalRead(BUTTON_PIN) == HIGH) {
    buttonPressed = false;
  }
  
  // Leitura automática a cada intervalo
  if (millis() - lastReading > readingInterval) {
    Serial.println("⏰ Medição automática");
    measureAndSend();
    lastReading = millis();
  }
  
  // Simular descarga da bateria
  if (millis() % 60000 == 0) { // A cada minuto
    batteryLevel = max(20, batteryLevel - 1);
  }
  
  delay(100);
}

void testLEDs() {
  Serial.println("🔍 Testando LEDs...");
  digitalWrite(LED_RED, HIGH);
  delay(300);
  digitalWrite(LED_RED, LOW);
  digitalWrite(LED_YELLOW, HIGH);
  delay(300);
  digitalWrite(LED_YELLOW, LOW);
  digitalWrite(LED_GREEN, HIGH);
  delay(300);
  digitalWrite(LED_GREEN, LOW);
}

void connectWiFi() {
  Serial.println("📡 Conectando ao WiFi...");
  WiFi.begin(ssid, password);
  
  updateDisplay("Conectando WiFi", "...", "");
  setLED("yellow");
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(1000);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("");
    Serial.println("✅ WiFi conectado!");
    Serial.print("📍 IP: ");
    Serial.println(WiFi.localIP());
    
    updateDisplay("WiFi Conectado", WiFi.localIP().toString(), "");
    setLED("green");
    playTone(2000, 500);
    delay(2000);
  } else {
    Serial.println("❌ Falha na conexão WiFi");
    updateDisplay("ERRO WiFi", "Verifique rede", "");
    setLED("red");
    playAlert(5);
  }
}

void measureAndSend() {
  updateDisplay("Medindo...", "Aguarde", "");
  setLED("yellow");
  
  Serial.println("🌡️ Iniciando medição de temperatura...");
  
  // Fazer 3 leituras para maior precisão
  float temperatures[3];
  float avgTemp = 0;
  
  for(int i = 0; i < 3; i++) {
    sensors.requestTemperatures();
    temperatures[i] = sensors.getTempCByIndex(0);
    avgTemp += temperatures[i];
    
    Serial.print("📊 Leitura ");
    Serial.print(i + 1);
    Serial.print(": ");
    Serial.print(temperatures[i]);
    Serial.println("°C");
    
    delay(1000);
  }
  
  avgTemp = avgTemp / 3.0;
  
  // Verificar se a leitura é válida
  if(avgTemp == DEVICE_DISCONNECTED_C || avgTemp < -50 || avgTemp > 100) {
    Serial.println("❌ Erro: Sensor desconectado ou leitura inválida!");
    updateDisplay("ERRO", "Sensor", "desconectado");
    setLED("red");
    playAlert(3);
    return;
  }
  
  Serial.print("🌡️ Temperatura média: ");
  Serial.print(avgTemp);
  Serial.println("°C");
  
  // Determinar status baseado na temperatura
  String status = getTemperatureStatus(avgTemp);
  String statusIcon = getStatusIcon(avgTemp);
  
  // Atualizar display
  updateDisplay("Temperatura:", String(avgTemp, 1) + "C", status);
  
  // Definir LED e som baseado na temperatura
  if(avgTemp >= 39.0) {
    setLED("red");
    playAlert(5);
    Serial.println("🚨 ALERTA: Temperatura crítica!");
  } else if(avgTemp >= 37.8) {
    setLED("yellow");
    playAlert(2);
    Serial.println("⚠️ ATENÇÃO: Febre detectada!");
  } else if(avgTemp <= 35.0) {
    setLED("red");
    playAlert(3);
    Serial.println("🔵 ATENÇÃO: Temperatura baixa!");
  } else {
    setLED("green");
    playTone(1500, 200);
    Serial.println("✅ Temperatura normal");
  }
  
  // Enviar dados para o servidor
  sendToServer(avgTemp);
}

String getTemperatureStatus(float temp) {
  if(temp >= 39.0) return "CRITICO";
  else if(temp >= 37.8) return "FEBRE";
  else if(temp <= 35.0) return "BAIXA";
  else return "NORMAL";
}

String getStatusIcon(float temp) {
  if(temp >= 39.0) return "🔴";
  else if(temp >= 37.8) return "🟡";
  else if(temp <= 35.0) return "🔵";
  else return "🟢";
}

void sendToServer(float temperature) {
  if(WiFi.status() == WL_CONNECTED) {
    Serial.println("📤 Enviando dados para o servidor...");
    
    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");
    
    // Criar JSON
    StaticJsonDocument<300> doc;
    doc["device_id"] = deviceID;
    doc["sensor_type"] = "temperature";
    doc["value"] = temperature;
    doc["unit"] = "°C";
    doc["location"] = location;
    doc["battery_level"] = batteryLevel;
    doc["firmware_version"] = "1.0.0";
    
    String jsonString;
    serializeJson(doc, jsonString);
    
    Serial.println("📋 Payload JSON:");
    Serial.println(jsonString);
    
    int httpResponseCode = http.POST(jsonString);
    
    if(httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("✅ Dados enviados com sucesso!");
      Serial.print("📨 Código de resposta: ");
      Serial.println(httpResponseCode);
      Serial.print("📄 Resposta: ");
      Serial.println(response);
      
      // Feedback visual de sucesso
      for(int i = 0; i < 3; i++) {
        setLED("green");
        delay(100);
        setLED("off");
        delay(100);
      }
      setLED("green");
      
    } else {
      Serial.print("❌ Erro no envio: ");
      Serial.println(httpResponseCode);
      
      // Feedback visual de erro
      setLED("red");
      playAlert(2);
    }
    
    http.end();
  } else {
    Serial.println("❌ WiFi desconectado!");
    updateDisplay("ERRO", "WiFi", "desconectado");
    setLED("red");
    playAlert(3);
  }
}

void registerDevice() {
  Serial.println("📝 Registrando dispositivo no sistema...");
  Serial.println("Device ID: " + deviceID);
  Serial.println("Location: " + location);
}

void updateDisplay(String line1, String line2, String line3) {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  
  // Linha 1 - Título
  display.setCursor(0, 0);
  display.setTextSize(1);
  display.println(line1);
  
  // Linha 2 - Valor principal
  display.setCursor(0, 20);
  display.setTextSize(2);
  display.println(line2);
  
  // Linha 3 - Status
  display.setCursor(0, 45);
  display.setTextSize(1);
  display.println(line3);
  
  // Informações do sistema
  display.setCursor(0, 56);
  display.setTextSize(1);
  display.print("BAT:");
  display.print(batteryLevel);
  display.print("% ");
  
  if(WiFi.status() == WL_CONNECTED) {
    display.print("WiFi:OK");
  } else {
    display.print("WiFi:--");
  }
  
  display.display();
}

void setLED(String color) {
  // Apagar todos os LEDs
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_YELLOW, LOW);
  digitalWrite(LED_RED, LOW);
  
  // Acender LED específico
  if(color == "green") {
    digitalWrite(LED_GREEN, HIGH);
  } else if(color == "yellow") {
    digitalWrite(LED_YELLOW, HIGH);
  } else if(color == "red") {
    digitalWrite(LED_RED, HIGH);
  }
  // "off" não acende nenhum LED
}

void playAlert(int beeps) {
  for(int i = 0; i < beeps; i++) {
    playTone(800, 200);
    delay(200);
  }
}

void playTone(int frequency, int duration) {
  // Gerar tom usando PWM
  ledcSetup(0, frequency, 8);
  ledcAttachPin(BUZZER_PIN, 0);
  ledcWrite(0, 128); // 50% duty cycle
  delay(duration);
  ledcWrite(0, 0); // Parar som
}

// Função para debug - mostra informações do sistema
void printSystemInfo() {
  Serial.println("=== INFORMAÇÕES DO SISTEMA ===");
  Serial.println("Device ID: " + deviceID);
  Serial.println("Location: " + location);
  Serial.print("WiFi Status: ");
  Serial.println(WiFi.status() == WL_CONNECTED ? "Conectado" : "Desconectado");
  if(WiFi.status() == WL_CONNECTED) {
    Serial.println("IP: " + WiFi.localIP().toString());
  }
  Serial.println("Battery Level: " + String(batteryLevel) + "%");
  Serial.println("Server URL: " + String(serverURL));
  Serial.println("Reading Interval: " + String(readingInterval) + "ms");
  Serial.println("==============================");
} 