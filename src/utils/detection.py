"""
Utilitários de Detecção Automática
=================================

Funções para detecção automática de região geográfica e sintomas
baseados em dados clínicos e localização.
"""

import requests


def detectar_regiao_automatica():
    """
    Detecta região geográfica baseada na localização do usuário via IP.
    
    Returns:
        str: Código da região ('brasil_norte', 'africa', 'asia')
    """
    try:
        # Tentar obter localização via IP
        response = requests.get('http://ip-api.com/json/', timeout=3)
        if response.status_code == 200:
            data = response.json()
            country = data.get('country', '').lower()
            
            # Mapear países para regiões
            if 'brazil' in country or 'brasil' in country:
                return 'brasil_norte'
            elif any(pais in country for pais in [
                'nigeria', 'kenya', 'ghana', 'uganda', 'tanzania', 'ethiopia', 
                'congo', 'sudan', 'mali', 'burkina', 'niger', 'chad', 
                'cameroon', 'senegal'
            ]):
                return 'africa'
            elif any(pais in country for pais in [
                'india', 'bangladesh', 'thailand', 'vietnam', 'indonesia', 
                'philippines', 'myanmar', 'cambodia', 'laos', 'malaysia', 
                'singapore'
            ]):
                return 'asia'
    except Exception:
        pass
    
    # Região padrão se não conseguir detectar
    return 'brasil_norte'


def detectar_febre_automatica(temperatura):
    """
    Detecta febre automaticamente baseada na temperatura corporal.
    
    Args:
        temperatura (float): Temperatura corporal em Celsius
        
    Returns:
        list: Lista de sintomas de febre detectados
    """
    sintomas_febre = []
    
    if temperatura >= 39.0:
        sintomas_febre.append('febre_alta')
        sintomas_febre.append('febre')
    elif temperatura >= 37.8:
        sintomas_febre.append('febre')
    
    return sintomas_febre


def get_regiao_nomes():
    """
    Retorna dicionário com nomes das regiões para exibição.
    
    Returns:
        dict: Mapeamento de códigos para nomes das regiões
    """
    return {
        'brasil_norte': '🇧🇷 Norte do Brasil',
        'africa': '🌍 África Subsaariana',
        'asia': '🌏 Ásia (Sul e Sudeste)'
    }


def get_regiao_nomes_curtos():
    """
    Retorna dicionário com nomes curtos das regiões.
    
    Returns:
        dict: Mapeamento de códigos para nomes curtos das regiões
    """
    return {
        'brasil_norte': 'Norte do Brasil',
        'africa': 'África',
        'asia': 'Ásia'
    } 