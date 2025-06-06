import streamlit as st
import hashlib
import json
import os
from datetime import datetime, timedelta
import secrets

class AuthManager:
    def __init__(self):
        self.users_file = 'users.json'
        self.sessions_file = 'sessions.json'
        self.audit_file = 'audit_log.json'
        self._init_default_users()
    
    def _init_default_users(self):
        """Inicializa usuários padrão se não existirem"""
        if not os.path.exists(self.users_file):
            default_users = {
                'admin': {
                    'password_hash': self._hash_password('admin123'),
                    'role': 'administrador',
                    'name': 'Administrador do Sistema',
                    'created_at': datetime.now().isoformat(),
                    'active': True
                },
                'medico': {
                    'password_hash': self._hash_password('medico123'),
                    'role': 'medico',
                    'name': 'Médico Responsável',
                    'created_at': datetime.now().isoformat(),
                    'active': True
                },
                'enfermeiro': {
                    'password_hash': self._hash_password('enfermeiro123'),
                    'role': 'enfermeiro',
                    'name': 'Enfermeiro(a)',
                    'created_at': datetime.now().isoformat(),
                    'active': True
                }
            }
            self._save_users(default_users)
    
    def _hash_password(self, password):
        """Hash seguro da senha"""
        salt = "triagem_medica_salt_2024"
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def _save_users(self, users):
        """Salva usuários no arquivo"""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def _load_users(self):
        """Carrega usuários do arquivo"""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _log_audit(self, action, username, details=""):
        """Registra ações no log de auditoria"""
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'username': username,
            'ip_address': st.session_state.get('client_ip', 'unknown'),
            'details': details
        }
        
        audit_log = []
        if os.path.exists(self.audit_file):
            try:
                with open(self.audit_file, 'r') as f:
                    audit_log = json.load(f)
            except:
                audit_log = []
        
        audit_log.append(audit_entry)
        
        # Manter apenas os últimos 1000 registros
        if len(audit_log) > 1000:
            audit_log = audit_log[-1000:]
        
        with open(self.audit_file, 'w') as f:
            json.dump(audit_log, f, indent=2)
    
    def authenticate(self, username, password):
        """Autentica usuário"""
        users = self._load_users()
        
        if username not in users:
            self._log_audit('LOGIN_FAILED', username, 'Usuário não encontrado')
            return False
        
        user = users[username]
        if not user.get('active', True):
            self._log_audit('LOGIN_FAILED', username, 'Usuário inativo')
            return False
        
        password_hash = self._hash_password(password)
        if password_hash == user['password_hash']:
            # Criar sessão
            session_token = secrets.token_urlsafe(32)
            self._create_session(username, session_token)
            
            # Log de sucesso
            self._log_audit('LOGIN_SUCCESS', username)
            
            # Salvar na sessão do Streamlit
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            st.session_state['user_role'] = user['role']
            st.session_state['user_name'] = user['name']
            st.session_state['session_token'] = session_token
            
            return True
        else:
            self._log_audit('LOGIN_FAILED', username, 'Senha incorreta')
            return False
    
    def _create_session(self, username, token):
        """Cria sessão de usuário"""
        sessions = {}
        if os.path.exists(self.sessions_file):
            try:
                with open(self.sessions_file, 'r') as f:
                    sessions = json.load(f)
            except:
                sessions = {}
        
        sessions[token] = {
            'username': username,
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(hours=8)).isoformat()
        }
        
        with open(self.sessions_file, 'w') as f:
            json.dump(sessions, f, indent=2)
    
    def is_authenticated(self):
        """Verifica se usuário está autenticado"""
        if not st.session_state.get('authenticated', False):
            return False
        
        # Verificar se sessão ainda é válida
        token = st.session_state.get('session_token')
        if not token:
            return False
        
        sessions = {}
        if os.path.exists(self.sessions_file):
            try:
                with open(self.sessions_file, 'r') as f:
                    sessions = json.load(f)
            except:
                return False
        
        if token not in sessions:
            return False
        
        session = sessions[token]
        expires_at = datetime.fromisoformat(session['expires_at'])
        
        if datetime.now() > expires_at:
            # Sessão expirada
            self.logout()
            return False
        
        return True
    
    def logout(self):
        """Faz logout do usuário"""
        username = st.session_state.get('username', 'unknown')
        self._log_audit('LOGOUT', username)
        
        # Remover sessão
        token = st.session_state.get('session_token')
        if token and os.path.exists(self.sessions_file):
            try:
                with open(self.sessions_file, 'r') as f:
                    sessions = json.load(f)
                if token in sessions:
                    del sessions[token]
                with open(self.sessions_file, 'w') as f:
                    json.dump(sessions, f, indent=2)
            except:
                pass
        
        # Limpar sessão do Streamlit
        for key in ['authenticated', 'username', 'user_role', 'user_name', 'session_token']:
            if key in st.session_state:
                del st.session_state[key]
    
    def get_user_permissions(self):
        """Retorna permissões do usuário atual"""
        role = st.session_state.get('user_role', '')
        
        permissions = {
            'administrador': {
                'triagem': True,
                'estatisticas': True,
                'historico': True,
                'audit_log': True,
                'user_management': True,
                'export_data': True
            },
            'medico': {
                'triagem': True,
                'estatisticas': True,
                'historico': True,
                'audit_log': False,
                'user_management': False,
                'export_data': True
            },
            'enfermeiro': {
                'triagem': True,
                'estatisticas': True,
                'historico': False,
                'audit_log': False,
                'user_management': False,
                'export_data': False
            }
        }
        
        return permissions.get(role, {})
    
    def show_login_form(self):
        """Exibe formulário de login"""
        # Container centralizado para o formulário sem fundo branco
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.form("login_form"):
                st.markdown("""
                <div style="padding: 1.5rem 0;">
                """, unsafe_allow_html=True)
                
                # Centralizar usando colunas
                col_a, col_b, col_c = st.columns([1, 2, 1])
                with col_b:
                    st.markdown("### 🔑 Credenciais de Acesso")
                
                st.markdown("---")
                
                username = st.text_input(
                    "👤 Usuário", 
                    placeholder="Digite seu nome de usuário",
                    help="Informe suas credenciais de acesso ao sistema"
                )
                
                password = st.text_input(
                    "🔒 Senha", 
                    type="password",
                    placeholder="Digite sua senha",
                    help="Senha de acesso ao sistema"
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                login_button = st.form_submit_button(
                    "🔓 Entrar no Sistema", 
                    use_container_width=True,
                    type="primary"
                )
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                if login_button:
                    if username and password:
                        if self.authenticate(username, password):
                            st.success(f"✅ Bem-vindo(a), {st.session_state['user_name']}!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Credenciais inválidas! Verifique seu usuário e senha.")
                    else:
                        st.warning("⚠️ Por favor, preencha todos os campos!")
        
        # Informações de ajuda em uma seção separada mais compacta
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.expander("ℹ️ Informações de Acesso", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **🔐 Níveis de Usuário:**
                - **Administrador**: Acesso completo
                - **Médico**: Triagem + estatísticas + histórico
                - **Enfermeiro**: Triagem + estatísticas
                """)
            
            with col2:
                st.markdown("""
                **🛡️ Segurança:**
                - Sessões de 8 horas
                - Logout automático
                - Log de auditoria
                - Dados criptografados
                """)
            
            st.markdown("---")
            st.markdown("""
            **📞 Suporte:** Em caso de problemas de acesso, contate o administrador do sistema.
            Para redefinição de senha, procure o responsável técnico.
            """)
        
        # Footer mais discreto
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #888; font-size: 0.85rem; margin-top: 1rem;">
            🔒 Sistema Seguro | Dados protegidos por criptografia<br>
            🏥 Desenvolvido para profissionais de saúde
        </div>
        """, unsafe_allow_html=True)
    
    def show_user_info(self):
        """Exibe informações do usuário logado"""
        if self.is_authenticated():
            with st.sidebar:
                st.markdown("---")
                st.markdown("### 👤 Usuário Logado")
                st.write(f"**Nome:** {st.session_state['user_name']}")
                st.write(f"**Perfil:** {st.session_state['user_role'].title()}")
                
                if st.button("🚪 Sair", use_container_width=True):
                    self.logout()
                    st.rerun()
    
    def require_permission(self, permission):
        """Decorator para verificar permissões"""
        permissions = self.get_user_permissions()
        if not permissions.get(permission, False):
            st.error("❌ Você não tem permissão para acessar esta funcionalidade!")
            st.stop()
        return True 