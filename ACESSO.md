# 🔑 GUIA DE ACESSO AO SISTEMA
## Sistema de Triagem Médica com IA

---

## 🚀 PRIMEIROS PASSOS

### Como Executar o Sistema
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar a aplicação
streamlit run app.py

# 3. Acessar no navegador
# Local: http://localhost:8501
# Rede: http://SEU_IP:8501
```

---

## 🔐 CREDENCIAIS PADRÃO

### ⚠️ IMPORTANTE: ALTERAR EM PRODUÇÃO

O sistema vem com usuários pré-configurados para facilitar os testes iniciais:

| Usuário | Senha | Perfil | Permissões |
|---------|-------|--------|------------|
| **admin** | admin123 | Administrador | ✅ Todas as funcionalidades |
| **medico** | medico123 | Médico | ✅ Triagem, Estatísticas, Histórico |
| **enfermeiro** | enfermeiro123 | Enfermeiro | ✅ Triagem, Estatísticas |

### 🛡️ Segurança das Credenciais
- **Senhas hasheadas**: SHA-256 + salt personalizado
- **Sessões seguras**: Tokens de 32 bytes
- **Expiração automática**: 8 horas de inatividade
- **Log de auditoria**: Todas as tentativas registradas

---

## 👥 PERFIS DE USUÁRIO

### 🔧 ADMINISTRADOR
**Acesso Completo ao Sistema**
- ✅ Realizar triagens médicas
- ✅ Visualizar estatísticas epidemiológicas
- ✅ Acessar histórico completo de atendimentos
- ✅ Consultar log de auditoria
- ✅ Gerenciar usuários (futuro)
- ✅ Exportar dados (futuro)

**Casos de Uso:**
- Supervisão geral do sistema
- Análise de segurança e auditoria
- Configuração e manutenção
- Relatórios gerenciais

### 🩺 MÉDICO
**Acesso Clínico Completo**
- ✅ Realizar triagens médicas
- ✅ Visualizar estatísticas epidemiológicas
- ✅ Acessar histórico completo de atendimentos
- ❌ Log de auditoria (restrito)
- ❌ Gerenciamento de usuários
- ✅ Exportar dados médicos

**Casos de Uso:**
- Triagem de pacientes
- Análise epidemiológica
- Acompanhamento de casos
- Tomada de decisões clínicas

### 👩‍⚕️ ENFERMEIRO
**Acesso Operacional**
- ✅ Realizar triagens médicas
- ✅ Visualizar estatísticas básicas
- ❌ Histórico completo (restrito)
- ❌ Log de auditoria (restrito)
- ❌ Gerenciamento de usuários
- ❌ Exportação de dados

**Casos de Uso:**
- Triagem inicial de pacientes
- Coleta de dados clínicos
- Acompanhamento básico
- Suporte ao atendimento médico

---

## 🔒 PROCESSO DE LOGIN

### 1. Tela de Acesso
- Interface limpa e profissional
- Campos para usuário e senha
- Validação em tempo real
- Mensagens de erro claras

### 2. Autenticação
- Verificação de credenciais
- Validação de usuário ativo
- Criação de sessão segura
- Log de tentativas

### 3. Sessão Ativa
- Token único por sessão
- Renovação automática
- Logout por inatividade
- Informações do usuário na sidebar

---

## 🚨 PROCEDIMENTOS DE SEGURANÇA

### Primeira Configuração
```bash
# 1. Alterar senhas padrão (OBRIGATÓRIO em produção)
# Acesse como admin e altere todas as senhas

# 2. Configurar backup
tar -czf backup_inicial.tar.gz users.json .encryption_key

# 3. Definir permissões de arquivo
chmod 600 .encryption_key
chmod 644 users.json
```

### Monitoramento de Acesso
- **Tentativas de login**: Máximo 5 por 15 minutos
- **Sessões ativas**: Monitoradas em `sessions.json`
- **Log de auditoria**: Todas as ações registradas
- **Alertas**: Tentativas suspeitas identificadas

---

## 🔧 CONFIGURAÇÃO AVANÇADA

### Variáveis de Ambiente
```bash
# Configurações opcionais de segurança
export TRIAGEM_SECRET_KEY="sua_chave_personalizada"
export TRIAGEM_SALT="seu_salt_personalizado"
export TRIAGEM_SESSION_TIMEOUT="28800"  # 8 horas
export TRIAGEM_MAX_LOGIN_ATTEMPTS="5"
```

### Configuração do Streamlit
Crie um arquivo `.streamlit/config.toml`:
```toml
[server]
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 1
port = 8501

[browser]
gatherUsageStats = false
serverAddress = "localhost"

[theme]
primaryColor = "#1e3c72"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

---

## 🆘 SOLUÇÃO DE PROBLEMAS

### Problemas Comuns

#### ❌ "Credenciais inválidas"
- Verificar usuário e senha
- Confirmar se usuário está ativo
- Aguardar se houver rate limiting

#### ❌ "Sessão expirada"
- Fazer login novamente
- Verificar conectividade
- Limpar cache do navegador

#### ❌ "Erro ao carregar sistema"
- Verificar dependências instaladas
- Confirmar arquivos de configuração
- Verificar permissões de arquivo

### Comandos de Diagnóstico
```bash
# Verificar status dos arquivos
ls -la users.json sessions.json audit_log.json

# Verificar logs de erro
tail -f audit_log.json

# Reiniciar sistema
pkill -f streamlit
streamlit run app.py
```

---

## 📞 SUPORTE TÉCNICO

### Contatos de Emergência
- **Administrador**: admin@sistema-triagem.local
- **Suporte Técnico**: suporte@sistema-triagem.local
- **Segurança**: security@sistema-triagem.local

### Procedimentos de Suporte
1. **Problemas de Acesso**: Contatar administrador
2. **Falhas Técnicas**: Verificar logs e contatar suporte
3. **Questões de Segurança**: Notificar imediatamente
4. **Solicitação de Novos Usuários**: Processo via administrador

---

## 📋 CHECKLIST DE IMPLANTAÇÃO

### Antes de Usar em Produção
- [ ] Alterar todas as senhas padrão
- [ ] Configurar backup automático
- [ ] Testar todos os perfis de usuário
- [ ] Verificar logs de auditoria
- [ ] Configurar monitoramento
- [ ] Treinar usuários finais
- [ ] Documentar procedimentos locais
- [ ] Definir responsáveis por manutenção

### Manutenção Regular
- [ ] Backup semanal dos dados
- [ ] Verificação mensal de logs
- [ ] Atualização trimestral de senhas
- [ ] Revisão semestral de permissões

---

**🔐 LEMBRE-SE**: A segurança do sistema depende do uso responsável das credenciais. Nunca compartilhe senhas e sempre faça logout ao terminar o uso. 