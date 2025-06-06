"""
Módulo IoT - Integração com Sensores e MQTT
==========================================

Gerencia comunicação com sensores IoT, protocolo MQTT,
dashboard em tempo real e controle remoto de dispositivos.

Classes principais:
- MQTTManager: Gerenciamento de comunicação MQTT
- IoTDashboard: Dashboard para visualização de dados IoT
- IoTManager: Gerenciamento geral de dispositivos IoT
"""

from .mqtt_manager import MQTTManager
from .iot_dashboard import IoTDashboard
from .iot_manager import IoTManager

__all__ = ['MQTTManager', 'IoTDashboard', 'IoTManager'] 