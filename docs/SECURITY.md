# 🔒 DOCUMENTAÇÃO DE SEGURANÇA
## Sistema de Triagem Médica com IA

### 📋 ÍNDICE
1. [Visão Geral de Segurança](#visão-geral)
2. [Autenticação e Autorização](#autenticação)
3. [Criptografia de Dados](#criptografia)
4. [Auditoria e Logs](#auditoria)
5. [Validação de Dados](#validação)
6. [Controle de Acesso](#controle-acesso)
7. [Configurações de Segurança](#configurações)
8. [Procedimentos de Emergência](#emergência)

---

## 🛡️ VISÃO GERAL DE SEGURANÇA

### Princípios de Segurança Implementados
- **Confidencialidade**: Dados sensíveis criptografados
- **Integridade**: Validação rigorosa de entrada
- **Disponibilidade**: Rate limiting e controle de sessão
- **Auditabilidade**: Log completo de todas as ações
- **Não-repúdio**: Assinatura digital de ações críticas

### Conformidade
- **LGPD**: Anonimização e criptografia de dados pessoais
- **CFM**: Rastreabilidade de diagnósticos médicos
- **ISO 27001**: Controles de segurança da informação

---

## 🔐 AUTENTICAÇÃO E AUTORIZAÇÃO

### Sistema de Usuários
```
ADMINISTRADOR
├── Triagem médica ✓
├── Estatísticas ✓
├── Histórico completo ✓
├── Log de auditoria ✓
├── Gerenciamento de usuários ✓
└── Exportação de dados ✓

MÉDICO
├── Triagem médica ✓
├── Estatísticas ✓
├── Histórico completo ✓
├── Log de auditoria ✗
├── Gerenciamento de usuários ✗
└── Exportação de dados ✓

ENFERMEIRO
├── Triagem médica ✓
├── Estatísticas ✓
├── Histórico completo ✗
├── Log de auditoria ✗
├── Gerenciamento de usuários ✗
└── Exportação de dados ✗
```

### Credenciais Padrão (ALTERAR EM PRODUÇÃO)
- **admin/admin123** - Administrador
- **medico/medico123** - Médico
- **enfermeiro/enfermeiro123** - Enfermeiro

### Segurança de Sessão
- **Duração**: 8 horas
- **Token**: 32 bytes seguros
- **Renovação**: Automática a cada ação
- **Logout**: Automático por inatividade

---

## 🔒 CRIPTOGRAFIA DE DADOS

### Algoritmos Utilizados
- **Senhas**: SHA-256 + Salt personalizado
- **Dados sensíveis**: Fernet (AES 128 em modo CBC)
- **Tokens**: secrets.token_urlsafe(32)
- **Integridade**: HMAC-SHA256

### Dados Criptografados
- Informações pessoais dos pacientes
- Histórico médico sensível
- Tokens de sessão
- Chaves de API (se aplicável)

### Gerenciamento de Chaves
- **Localização**: `.encryption_key` (permissão 600)
- **Rotação**: Manual (recomendado a cada 90 dias)
- **Backup**: Necessário para recuperação de dados

---

## 📊 AUDITORIA E LOGS

### Eventos Auditados
- **LOGIN_SUCCESS**: Login bem-sucedido
- **LOGIN_FAILED**: Tentativa de login falhada
- **LOGOUT**: Logout do usuário
- **TRIAGEM_REALIZADA**: Triagem médica processada
- **ESTATISTICAS_ACESSADAS**: Acesso às estatísticas
- **HISTORICO_ACESSADO**: Acesso ao histórico
- **AUDIT_LOG_ACESSADO**: Acesso ao log de auditoria

### Informações Registradas
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "action": "TRIAGEM_REALIZADA",
  "username": "medico",
  "ip_address": "192.168.1.100",
  "details": "Paciente: hash_anonimo_123",
  "integrity_hash": "sha256_hash"
}
```

### Retenção de Logs
- **Período**: Últimos 1000 registros
- **Rotação**: Automática
- **Backup**: Recomendado diário

---

## ✅ VALIDAÇÃO DE DADOS

### Validações Médicas Implementadas
- **Idade**: 0-150 anos
- **Temperatura**: 30-45°C
- **Pressão Arterial**: 50-300/30-200 mmHg
- **Frequência Cardíaca**: 20-250 bpm
- **Peso**: 0.5-500 kg

### Sanitização de Entrada
- Remoção de caracteres perigosos: `< > " '`
- Trim de espaços em branco
- Validação de tipos de dados
- Escape de caracteres especiais

### Rate Limiting
- **Tentativas de login**: 5 por 15 minutos
- **Triagens**: Sem limite (uso médico)
- **Consultas**: Sem limite (uso médico)

---

## 🚪 CONTROLE DE ACESSO

### Verificações de Segurança
1. **Autenticação**: Usuário válido e ativo
2. **Autorização**: Permissões adequadas
3. **Sessão**: Token válido e não expirado
4. **Rate Limiting**: Dentro dos limites
5. **Validação**: Dados corretos e seguros

### Proteções Implementadas
- **Session Hijacking**: Tokens únicos e seguros
- **CSRF**: Formulários com tokens
- **XSS**: Sanitização de entrada
- **SQL Injection**: Não aplicável (sem SQL)
- **Path Traversal**: Validação de caminhos

---

## ⚙️ CONFIGURAÇÕES DE SEGURANÇA

### Arquivos Críticos
```
.encryption_key     # Chave de criptografia (600)
users.json         # Base de usuários (644)
sessions.json      # Sessões ativas (644)
audit_log.json     # Log de auditoria (644)
rate_limits.json   # Controle de rate limiting (644)
```

### Variáveis de Ambiente Recomendadas
```bash
export TRIAGEM_SECRET_KEY="sua_chave_secreta_aqui"
export TRIAGEM_SALT="seu_salt_personalizado"
export TRIAGEM_SESSION_TIMEOUT="28800"  # 8 horas
export TRIAGEM_MAX_LOGIN_ATTEMPTS="5"
```

### Configurações do Streamlit
```toml
[server]
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 1

[browser]
gatherUsageStats = false
```

---

## 🚨 PROCEDIMENTOS DE EMERGÊNCIA

### Em Caso de Comprometimento
1. **Imediato**:
   - Parar a aplicação: `pkill -f streamlit`
   - Revogar todas as sessões: `rm sessions.json`
   - Verificar logs: `tail -f audit_log.json`

2. **Investigação**:
   - Analisar log de auditoria
   - Verificar tentativas de login
   - Identificar ações suspeitas

3. **Recuperação**:
   - Alterar todas as senhas
   - Regenerar chave de criptografia
   - Reiniciar aplicação com novos tokens

### Backup de Segurança
```bash
# Backup diário recomendado
tar -czf backup_$(date +%Y%m%d).tar.gz \
  users.json audit_log.json .encryption_key \
  historico_atendimentos.json
```

### Monitoramento Contínuo
- Verificar logs diariamente
- Monitorar tentativas de login falhadas
- Acompanhar padrões de uso anômalos
- Validar integridade dos dados

---

## 📞 CONTATOS DE EMERGÊNCIA

### Responsáveis pela Segurança
- **Administrador do Sistema**: admin@sistema-triagem.com
- **Responsável Técnico**: dev@sistema-triagem.com
- **Compliance LGPD**: lgpd@sistema-triagem.com

### Procedimentos de Notificação
1. **Incidente de Segurança**: Notificar em até 2 horas
2. **Vazamento de Dados**: Notificar ANPD em até 72 horas
3. **Falha do Sistema**: Notificar usuários em até 1 hora

---

## 🔄 ATUALIZAÇÕES DE SEGURANÇA

### Cronograma de Manutenção
- **Senhas**: Alterar a cada 90 dias
- **Chaves**: Rotacionar a cada 90 dias
- **Logs**: Backup semanal
- **Sistema**: Atualizar mensalmente

### Checklist de Segurança Mensal
- [ ] Verificar logs de auditoria
- [ ] Validar integridade dos dados
- [ ] Testar procedimentos de backup
- [ ] Revisar permissões de usuários
- [ ] Atualizar dependências
- [ ] Verificar configurações de segurança

---

**⚠️ IMPORTANTE**: Esta documentação deve ser mantida atualizada e revisada regularmente. Em ambiente de produção, todas as senhas padrão devem ser alteradas imediatamente. 