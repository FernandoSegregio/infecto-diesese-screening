#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <time.h>

// Configurações WiFi
const char* ssid = "Wokwi-GUEST";
const char* password = "";

// Configurações MQTT (usando suas credenciais do Farm Tech)
const char* mqtt_server = "91c5f1ea0f494ccebe45208ea8ffceff.s1.eu.hivemq.cloud";
const int mqtt_port = 8883;
const char* mqtt_user = "FARM_TECH";
const char* mqtt_password = "Pato1234";

// Tópicos MQTT para termômetro
const char* temperature_topic = "termometro/temperatura";
const char* status_topic = "termometro/status";
const char* alert_topic = "termometro/alerta";
const char* device_topic = "termometro/device";
const char* command_topic = "termometro/comando";  // Novo tópico para comandos

// Pinos
const int ledVerde = 2;
const int ledAmarelo = 15;
const int ledVermelho = 16;
const int buzzer = 17;
const int botao = 18;
const int sensorTemp = 34; // Potenciômetro simula temperatura

// Variáveis
String deviceID = "ESP32_TERMOMETRO_001";
String location = "Recepção - Posto 1";
float temperatura = 36.5;
bool botaoPressionado = false;
unsigned long ultimaLeitura = 0;
const long intervalLeitura = 15000; // 15 segundos
int batteryLevel = 100;

// MQTT
WiFiClientSecure espClient;
PubSubClient client(espClient);

void setup() {
  Serial.begin(115200);
  Serial.println("=== TERMÔMETRO IoT MQTT COM CONTROLE REMOTO ===");
  
  // Configurar pinos
  pinMode(ledVerde, OUTPUT);
  pinMode(ledAmarelo, OUTPUT);
  pinMode(ledVermelho, OUTPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(botao, INPUT_PULLUP);
  
  Serial.println("Pinos configurados!");
  
  // Teste dos LEDs
  testarLEDs();
  
  // Conectar WiFi
  conectarWiFi();
  
  // Configurar tempo (para timestamps)
  configTime(-3 * 3600, 0, "pool.ntp.org", "time.nist.gov");
  
  // Configurar MQTT
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  conectarMQTT();
  
  Serial.println("===== SISTEMA CONECTADO MQTT COM CONTROLE REMOTO! =====");
  digitalWrite(ledVerde, HIGH);
  
  // Enviar status inicial
  enviarStatusInicial();
}

void loop() {
  // Manter conexão MQTT
  if (!client.connected()) {
    conectarMQTT();
  }
  client.loop();
  
  // Botão pressionado
  if (digitalRead(botao) == LOW && !botaoPressionado) {
    botaoPressionado = true;
    Serial.println("BOTÃO PRESSIONADO - Medindo...");
    medirEEnviarMQTT();
    delay(1000);
  } else if (digitalRead(botao) == HIGH) {
    botaoPressionado = false;
  }
  
  // Medição automática
  if (millis() - ultimaLeitura > intervalLeitura) {
    ultimaLeitura = millis();
    medirEEnviarMQTT();
  }
  
  // Simular descarga da bateria
  if (millis() % 60000 == 0) {
    batteryLevel = max(20, batteryLevel - 1);
  }
  
  delay(100);
}

void testarLEDs() {
  Serial.println("Testando LEDs...");
  
  digitalWrite(ledVermelho, HIGH);
  delay(500);
  digitalWrite(ledVermelho, LOW);
  
  digitalWrite(ledAmarelo, HIGH);
  delay(500);
  digitalWrite(ledAmarelo, LOW);
  
  digitalWrite(ledVerde, HIGH);
  delay(500);
  digitalWrite(ledVerde, LOW);
  
  Serial.println("LEDs OK!");
}

void conectarWiFi() {
  Serial.println("Conectando WiFi...");
  WiFi.begin(ssid, password);
  
  int tentativas = 0;
  while (WiFi.status() != WL_CONNECTED && tentativas < 20) {
    delay(1000);
    Serial.print(".");
    tentativas++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("");
    Serial.println("WiFi conectado!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("WiFi falhou!");
  }
}

void conectarMQTT() {
  while (!client.connected()) {
    Serial.print("Conectando MQTT...");
    espClient.setInsecure();
    
    if (client.connect("TermometroESP32", mqtt_user, mqtt_password)) {
      Serial.println("MQTT conectado!");
      
      // Subscrever ao tópico de comandos
      client.subscribe(command_topic);
      Serial.println("📡 Subscrito ao tópico de comandos: " + String(command_topic));
      
    } else {
      Serial.print("Falhou, rc=");
      Serial.print(client.state());
      Serial.println(" Tentando novamente em 5 segundos");
      delay(5000);
    }
  }
}

// Callback para mensagens MQTT recebidas
void callback(char* topic, byte* payload, unsigned int length) {
  String messageTemp;
  
  for (unsigned int i = 0; i < length; i++) {
    messageTemp += (char)payload[i];
  }
  
  Serial.println("📨 Mensagem recebida no tópico: " + String(topic));
  Serial.println("📄 Conteúdo: " + messageTemp);
  
  // Processar comandos do dashboard web
  if (String(topic) == command_topic) {
    processarComando(messageTemp);
  }
}

void processarComando(String payload) {
  Serial.println("🎮 COMANDO RECEBIDO VIA MQTT!");
  
  // Parse JSON
  StaticJsonDocument<300> doc;
  DeserializationError error = deserializeJson(doc, payload);
  
  if (error) {
    Serial.println("❌ Erro ao decodificar comando JSON");
    return;
  }
  
  String command = doc["command"];
  String deviceId = doc["device_id"];
  String source = doc["source"];
  
  Serial.println("🔧 Comando: " + command);
  Serial.println("📱 Dispositivo alvo: " + deviceId);
  Serial.println("🌐 Origem: " + source);
  
  // Verificar se o comando é para este dispositivo
  if (deviceId != deviceID && deviceId != "ALL") {
    Serial.println("⚠️ Comando não é para este dispositivo, ignorando...");
    return;
  }
  
  // Processar comandos específicos
  if (command == "measure_temperature") {
    Serial.println("🌡️ COMANDO: Medir temperatura remotamente");
    
    // Feedback visual
    digitalWrite(ledAmarelo, HIGH);
    tone(buzzer, 1200, 300);
    delay(500);
    digitalWrite(ledAmarelo, LOW);
    
    // Fazer medição
    medirEEnviarMQTT();
    
    Serial.println("✅ Medição remota concluída!");
    
  } else if (command == "get_status") {
    Serial.println("📊 COMANDO: Solicitar status do dispositivo");
    
    enviarStatusCompleto();
    
  } else if (command == "test_leds") {
    Serial.println("🔧 COMANDO: Testar hardware (LEDs e buzzer)");
    
    testarHardwareRemoto();
    
  } else {
    Serial.println("❓ Comando não reconhecido: " + command);
    
    // Enviar resposta de comando não reconhecido
    enviarRespostaComando("unknown_command", command);
  }
}

void enviarStatusCompleto() {
  Serial.println("📡 Enviando status completo do dispositivo...");
  
  String payload = "{";
  payload += "\"device_id\":\"" + deviceID + "\",";
  payload += "\"status\":\"online\",";
  payload += "\"temperature\":" + String(temperatura, 1) + ",";
  payload += "\"location\":\"" + location + "\",";
  payload += "\"battery_level\":" + String(batteryLevel) + ",";
  payload += "\"wifi_rssi\":" + String(WiFi.RSSI()) + ",";
  payload += "\"free_memory\":" + String(ESP.getFreeHeap()) + ",";
  payload += "\"uptime\":" + String(millis()) + ",";
  payload += "\"firmware\":\"2.0.0\",";
  payload += "\"timestamp\":" + String(millis());
  payload += "}";
  
  client.publish(status_topic, payload.c_str());
  Serial.println("✅ Status completo enviado!");
}

void testarHardwareRemoto() {
  Serial.println("🔧 Testando hardware remotamente...");
  
  // Teste sequencial dos LEDs
  digitalWrite(ledVermelho, HIGH);
  tone(buzzer, 800, 200);
  delay(500);
  digitalWrite(ledVermelho, LOW);
  
  digitalWrite(ledAmarelo, HIGH);
  tone(buzzer, 1000, 200);
  delay(500);
  digitalWrite(ledAmarelo, LOW);
  
  digitalWrite(ledVerde, HIGH);
  tone(buzzer, 1200, 200);
  delay(500);
  digitalWrite(ledVerde, LOW);
  
  // Sequência final
  for (int i = 0; i < 3; i++) {
    digitalWrite(ledVerde, HIGH);
    digitalWrite(ledAmarelo, HIGH);
    digitalWrite(ledVermelho, HIGH);
    tone(buzzer, 1500, 100);
    delay(200);
    
    digitalWrite(ledVerde, LOW);
    digitalWrite(ledAmarelo, LOW);
    digitalWrite(ledVermelho, LOW);
    delay(200);
  }
  
  Serial.println("✅ Teste de hardware concluído!");
  
  // Enviar confirmação
  enviarRespostaComando("hardware_test_complete", "LEDs e buzzer testados com sucesso");
}

void enviarRespostaComando(String responseType, String message) {
  String payload = "{";
  payload += "\"device_id\":\"" + deviceID + "\",";
  payload += "\"response_type\":\"" + responseType + "\",";
  payload += "\"message\":\"" + message + "\",";
  payload += "\"timestamp\":" + String(millis());
  payload += "}";
  
  client.publish(status_topic, payload.c_str());
  Serial.println("📤 Resposta enviada: " + responseType);
}

void medirEEnviarMQTT() {
  // Ler potenciômetro e converter para temperatura
  int valor = analogRead(sensorTemp);
  temperatura = map(valor, 0, 4095, 300, 420) / 10.0;
  
  Serial.print("Temperatura: ");
  Serial.print(temperatura, 1);
  Serial.println("°C");
  
  // Controlar LEDs e alertas
  String status = controlarAlertas();
  
  // Enviar dados via MQTT
  enviarTemperaturaMQTT();
  enviarStatusMQTT(status);
  
  // Se crítico, enviar alerta
  if (status == "CRITICO" || status == "FEBRE") {
    enviarAlertaMQTT(status);
  }
}

String controlarAlertas() {
  // Apagar todos LEDs
  digitalWrite(ledVerde, LOW);
  digitalWrite(ledAmarelo, LOW);
  digitalWrite(ledVermelho, LOW);
  
  String status = "";
  
  if (temperatura >= 39.0) {
    // CRÍTICO
    digitalWrite(ledVermelho, HIGH);
    Serial.println("🚨 CRÍTICO! Temperatura muito alta!");
    status = "CRITICO";
    
    for (int i = 0; i < 5; i++) {
      tone(buzzer, 800, 200);
      delay(300);
    }
    
  } else if (temperatura >= 37.8) {
    // FEBRE
    digitalWrite(ledAmarelo, HIGH);
    Serial.println("⚠️ FEBRE detectada!");
    status = "FEBRE";
    
    for (int i = 0; i < 2; i++) {
      tone(buzzer, 1000, 200);
      delay(300);
    }
    
  } else if (temperatura <= 35.0) {
    // BAIXA
    digitalWrite(ledVermelho, HIGH);
    Serial.println("🔵 Temperatura BAIXA!");
    status = "BAIXA";
    
    for (int i = 0; i < 3; i++) {
      tone(buzzer, 600, 200);
      delay(300);
    }
    
  } else {
    // NORMAL
    digitalWrite(ledVerde, HIGH);
    Serial.println("✅ Temperatura NORMAL");
    status = "NORMAL";
    
    tone(buzzer, 1500, 200);
  }
  
  return status;
}

void enviarTemperaturaMQTT() {
  String payload = "{";
  payload += "\"device_id\":\"" + deviceID + "\",";
  payload += "\"sensor_type\":\"temperature\",";
  payload += "\"value\":" + String(temperatura, 1) + ",";
  payload += "\"unit\":\"°C\",";
  payload += "\"location\":\"" + location + "\",";
  payload += "\"battery_level\":" + String(batteryLevel) + ",";
  payload += "\"timestamp\":" + String(millis());
  payload += "}";
  
  client.publish(temperature_topic, payload.c_str());
  Serial.println("📡 Temperatura enviada: " + payload);
}

void enviarStatusMQTT(String status) {
  String payload = "{";
  payload += "\"device_id\":\"" + deviceID + "\",";
  payload += "\"status\":\"" + status + "\",";
  payload += "\"temperature\":" + String(temperatura, 1) + ",";
  payload += "\"location\":\"" + location + "\",";
  payload += "\"timestamp\":" + String(millis());
  payload += "}";
  
  client.publish(status_topic, payload.c_str());
  Serial.println("📊 Status enviado: " + payload);
}

void enviarAlertaMQTT(String tipoAlerta) {
  String payload = "{";
  payload += "\"device_id\":\"" + deviceID + "\",";
  payload += "\"alert_type\":\"" + tipoAlerta + "\",";
  payload += "\"temperature\":" + String(temperatura, 1) + ",";
  payload += "\"location\":\"" + location + "\",";
  payload += "\"priority\":\"HIGH\",";
  payload += "\"timestamp\":" + String(millis());
  payload += "}";
  
  client.publish(alert_topic, payload.c_str());
  Serial.println("🚨 ALERTA enviado: " + payload);
}

void enviarStatusInicial() {
  String payload = "{";
  payload += "\"device_id\":\"" + deviceID + "\",";
  payload += "\"action\":\"startup\",";
  payload += "\"location\":\"" + location + "\",";
  payload += "\"firmware\":\"2.0.0\",";
  payload += "\"ip\":\"" + WiFi.localIP().toString() + "\",";
  payload += "\"timestamp\":" + String(millis());
  payload += "}";
  
  client.publish(device_topic, payload.c_str());
  Serial.println("📱 Dispositivo registrado: " + payload);
}