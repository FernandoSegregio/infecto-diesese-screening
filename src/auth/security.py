import hashlib
import hmac
import secrets
import re
from cryptography.fernet import Fernet
from datetime import datetime
import json
import os

class SecurityManager:
    def __init__(self):
        self.key_file = '.encryption_key'
        self.cipher = self._get_or_create_cipher()
    
    def _get_or_create_cipher(self):
        """Obtém ou cria chave de criptografia"""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(key)
            # Tornar arquivo somente leitura
            os.chmod(self.key_file, 0o600)
        
        return Fernet(key)
    
    def encrypt_sensitive_data(self, data):
        """Criptografa dados sensíveis"""
        if isinstance(data, str):
            data = data.encode()
        elif isinstance(data, dict):
            data = json.dumps(data).encode()
        
        return self.cipher.encrypt(data).decode()
    
    def decrypt_sensitive_data(self, encrypted_data):
        """Descriptografa dados sensíveis"""
        try:
            decrypted = self.cipher.decrypt(encrypted_data.encode())
            return decrypted.decode()
        except:
            return None
    
    def hash_patient_id(self, patient_data):
        """Cria hash único para identificação do paciente (sem dados pessoais)"""
        # Usar apenas dados não sensíveis para criar ID único
        identifier = f"{patient_data.get('idade', '')}{patient_data.get('sexo', '')}{datetime.now().strftime('%Y%m%d')}"
        return hashlib.sha256(identifier.encode()).hexdigest()[:16]
    
    def sanitize_input(self, input_text):
        """Sanitiza entrada do usuário"""
        if not isinstance(input_text, str):
            return str(input_text)
        
        # Remove caracteres perigosos
        sanitized = re.sub(r'[<>"\']', '', input_text)
        sanitized = sanitized.strip()
        
        return sanitized
    
    def validate_medical_data(self, dados_paciente):
        """Valida dados médicos de entrada"""
        errors = []
        
        # Validar idade
        idade = dados_paciente.get('idade', 0)
        if not isinstance(idade, (int, float)) or idade < 0 or idade > 150:
            errors.append("Idade deve estar entre 0 e 150 anos")
        
        # Validar temperatura
        temperatura = dados_paciente.get('temperatura', 36.5)
        if not isinstance(temperatura, (int, float)) or temperatura < 30 or temperatura > 45:
            errors.append("Temperatura deve estar entre 30°C e 45°C")
        
        # Validar pressão arterial
        pressao_sistolica = dados_paciente.get('pressao_sistolica', 120)
        pressao_diastolica = dados_paciente.get('pressao_diastolica', 80)
        
        if not isinstance(pressao_sistolica, (int, float)) or pressao_sistolica < 50 or pressao_sistolica > 300:
            errors.append("Pressão sistólica deve estar entre 50 e 300 mmHg")
        
        if not isinstance(pressao_diastolica, (int, float)) or pressao_diastolica < 30 or pressao_diastolica > 200:
            errors.append("Pressão diastólica deve estar entre 30 e 200 mmHg")
        
        if pressao_diastolica >= pressao_sistolica:
            errors.append("Pressão sistólica deve ser maior que a diastólica")
        
        # Validar frequência cardíaca
        fc = dados_paciente.get('frequencia_cardiaca', 70)
        if not isinstance(fc, (int, float)) or fc < 20 or fc > 250:
            errors.append("Frequência cardíaca deve estar entre 20 e 250 bpm")
        
        # Validar peso
        peso = dados_paciente.get('peso', 70)
        if not isinstance(peso, (int, float)) or peso < 0.5 or peso > 500:
            errors.append("Peso deve estar entre 0.5 e 500 kg")
        
        return errors
    
    def anonymize_patient_data(self, dados_paciente):
        """Anonimiza dados do paciente para estatísticas"""
        anonymized = dados_paciente.copy()
        
        # Remover dados identificáveis
        sensitive_fields = ['nome', 'cpf', 'rg', 'endereco', 'telefone', 'email']
        for field in sensitive_fields:
            if field in anonymized:
                del anonymized[field]
        
        # Substituir por hash único
        anonymized['patient_hash'] = self.hash_patient_id(dados_paciente)
        
        return anonymized
    
    def create_audit_hash(self, data):
        """Cria hash para verificar integridade dos dados"""
        data_str = json.dumps(data, sort_keys=True)
        return hmac.new(
            b'audit_key_2024',
            data_str.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def verify_audit_integrity(self, data, expected_hash):
        """Verifica integridade dos dados de auditoria"""
        calculated_hash = self.create_audit_hash(data)
        return hmac.compare_digest(calculated_hash, expected_hash)
    
    def generate_session_token(self):
        """Gera token de sessão seguro"""
        return secrets.token_urlsafe(32)
    
    def mask_sensitive_info(self, text):
        """Mascara informações sensíveis em logs"""
        # Mascarar CPF
        text = re.sub(r'\d{3}\.\d{3}\.\d{3}-\d{2}', '***.***.***-**', text)
        
        # Mascarar telefone
        text = re.sub(r'\(\d{2}\)\s*\d{4,5}-\d{4}', '(**) ****-****', text)
        
        # Mascarar email
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '***@***.***', text)
        
        return text
    
    def check_password_strength(self, password):
        """Verifica força da senha"""
        issues = []
        
        if len(password) < 8:
            issues.append("Senha deve ter pelo menos 8 caracteres")
        
        if not re.search(r'[A-Z]', password):
            issues.append("Senha deve conter pelo menos uma letra maiúscula")
        
        if not re.search(r'[a-z]', password):
            issues.append("Senha deve conter pelo menos uma letra minúscula")
        
        if not re.search(r'\d', password):
            issues.append("Senha deve conter pelo menos um número")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            issues.append("Senha deve conter pelo menos um caractere especial")
        
        return issues
    
    def rate_limit_check(self, identifier, max_attempts=5, window_minutes=15):
        """Verifica limite de tentativas"""
        rate_limit_file = 'rate_limits.json'
        
        current_time = datetime.now()
        
        # Carregar dados de rate limiting
        rate_limits = {}
        if os.path.exists(rate_limit_file):
            try:
                with open(rate_limit_file, 'r') as f:
                    rate_limits = json.load(f)
            except:
                rate_limits = {}
        
        # Limpar entradas antigas
        cutoff_time = current_time.timestamp() - (window_minutes * 60)
        for key in list(rate_limits.keys()):
            rate_limits[key] = [
                timestamp for timestamp in rate_limits[key]
                if timestamp > cutoff_time
            ]
            if not rate_limits[key]:
                del rate_limits[key]
        
        # Verificar limite atual
        attempts = rate_limits.get(identifier, [])
        if len(attempts) >= max_attempts:
            return False, f"Muitas tentativas. Tente novamente em {window_minutes} minutos."
        
        # Registrar nova tentativa
        attempts.append(current_time.timestamp())
        rate_limits[identifier] = attempts
        
        # Salvar dados atualizados
        with open(rate_limit_file, 'w') as f:
            json.dump(rate_limits, f)
        
        return True, "" 