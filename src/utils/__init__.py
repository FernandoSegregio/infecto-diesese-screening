"""
Módulo Utils - Utilitários e Funções Auxiliares
==============================================

Contém funções utilitárias, helpers e ferramentas auxiliares
utilizadas em todo o sistema.

Funções:
- Detecção automática de região geográfica
- Detecção automática de febre
- Formatação de dados
- Validações auxiliares
"""

from .detection import (
    detectar_regiao_automatica,
    detectar_febre_automatica,
    get_regiao_nomes,
    get_regiao_nomes_curtos
)

__all__ = [
    'detectar_regiao_automatica',
    'detectar_febre_automatica', 
    'get_regiao_nomes',
    'get_regiao_nomes_curtos'
] 