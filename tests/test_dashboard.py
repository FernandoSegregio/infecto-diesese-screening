#!/usr/bin/env python3
"""
Teste simples do Dashboard IoT
"""

import streamlit as st
from iot_dashboard import IoTDashboard

def main():
    st.set_page_config(
        page_title="Teste Dashboard IoT",
        page_icon="🌡️",
        layout="wide"
    )
    
    st.title("🧪 Teste do Dashboard IoT")
    
    try:
        # Criar instância do dashboard
        dashboard = IoTDashboard()
        
        st.success("✅ Dashboard IoT criado com sucesso")
        
        # Testar métodos básicos
        st.subheader("🔧 Testes Básicos")
        
        try:
            devices = dashboard.iot_manager.get_all_devices()
            st.success(f"✅ Dispositivos carregados: {len(devices)}")
        except Exception as e:
            st.error(f"❌ Erro ao carregar dispositivos: {str(e)}")
        
        try:
            readings = dashboard.iot_manager._load_readings()
            st.success(f"✅ Leituras carregadas: {len(readings)}")
        except Exception as e:
            st.error(f"❌ Erro ao carregar leituras: {str(e)}")
        
        # Mostrar dashboard completo
        st.subheader("📊 Dashboard Completo")
        dashboard.show_dashboard()
        
    except Exception as e:
        st.error(f"❌ Erro ao criar dashboard: {str(e)}")
        st.exception(e)

if __name__ == "__main__":
    main() 