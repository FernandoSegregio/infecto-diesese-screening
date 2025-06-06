"""
Módulo Auth - Sistema de Autenticação e Segurança
================================================

Gerencia autenticação de usuários, controle de acesso, auditoria
e segurança dos dados médicos.

Classes principais:
- AuthManager: Gerenciamento de autenticação
- SecurityManager: Validação e segurança de dados
"""

from .auth import AuthManager
from .security import SecurityManager

__all__ = ['AuthManager', 'SecurityManager'] 