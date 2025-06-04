# 🏥 Sistema de IA para Triagem Médica em Áreas Vulneráveis

Sistema inteligente de apoio ao diagnóstico médico desenvolvido especificamente para profissionais de saúde em regiões remotas, áreas de desastre e contextos humanitários.

## 🚀 Início Rápido

### Instalação
```bash
# 1. Clone o repositório
git clone <repository-url>
cd triagem-medica-ia

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o sistema
streamlit run app.py

# 4. Acesse no navegador
# http://localhost:8501
```

### 🔐 Primeiro Acesso
O sistema possui autenticação segura. Para acessar pela primeira vez:

**📖 Consulte o [Guia de Acesso](ACESSO.md)** para credenciais padrão e instruções detalhadas.

## 🎯 Características Principais

### 🧠 Inteligência Artificial Avançada
- **15 doenças contempladas** relevantes para áreas vulneráveis
- **Algoritmo ponderado** com 4 fatores de análise
- **Diagnósticos diferenciais** com top 3 alternativas
- **Score detalhado** para transparência médica

### 🌡️ Sistema IoT Integrado
- **Sensores ESP32** para medição automática de temperatura
- **Dashboard em tempo real** com monitoramento de dispositivos
- **Integração automática** com formulário de triagem
- **Alertas inteligentes** para casos críticos

### 🌍 Contexto Epidemiológico
- **Eventos climáticos**: 16 tipos de contextos ambientais
- **Populações vulneráveis**: Ribeirinhos, gestantes, imunodeprimidos
- **Histórico médico**: 14 condições de risco
- **Incidências regionais**: Baseadas em dados epidemiológicos

### 🔒 Segurança Médica
- **Autenticação robusta** com 3 níveis de usuário
- **Criptografia AES-256** para dados sensíveis
- **Log de auditoria** completo
- **Validação rigorosa** de dados médicos

## 🏥 Doenças Contempladas

| Categoria | Doenças | Gravidade |
|-----------|---------|-----------|
| **Arboviroses** | Dengue, Zika, Chikungunya, Febre Amarela | Alta/Crítica |
| **Transmitidas por Água** | Leptospirose, Diarreia, Hepatite A, Esquistossomose | Média/Alta |
| **Respiratórias** | Infecção Respiratória, Tuberculose, COVID-19 | Média/Alta |
| **Parasitárias** | Malária, Leishmaniose, Doença de Chagas | Alta/Crítica |
| **Emergências** | Meningite Bacteriana | Crítica |

## 📊 Funcionalidades

### 🩺 Triagem Médica
- Formulário completo com 40+ sintomas
- Sinais vitais e dados demográficos
- Contexto ambiental e climático
- Resultado com medicação e urgência
- **Integração IoT** para temperatura automática

### 🌡️ Dashboard IoT
- **Monitoramento em tempo real** de sensores de temperatura
- **Gerenciamento de dispositivos** ESP32
- **Histórico de leituras** com análise estatística
- **Alertas automáticos** para febre e temperaturas críticas
- **Integração com triagem** para preenchimento automático

### 📈 Estatísticas Epidemiológicas
- Distribuição de diagnósticos
- Análise de urgência
- Eventos climáticos associados
- Métricas de atendimento

### 📋 Histórico de Atendimentos
- Registro completo de triagens
- Filtros por diagnóstico e urgência
- Rastreabilidade de casos
- Informações do profissional responsável

### 🔍 Log de Auditoria (Admin)
- Registro de todas as ações
- Análise de segurança
- Monitoramento de acesso
- Estatísticas de uso

## 👥 Perfis de Usuário

| Perfil | Triagem | Estatísticas | Histórico | Auditoria |
|--------|---------|--------------|-----------|-----------|
| **Administrador** | ✅ | ✅ | ✅ | ✅ |
| **Médico** | ✅ | ✅ | ✅ | ❌ |
| **Enfermeiro** | ✅ | ✅ | ❌ | ❌ |

## 📚 Documentação

### 📖 Guias Principais
- **[Guia de Acesso](ACESSO.md)** - Credenciais, login e primeiros passos
- **[Documentação de Segurança](SECURITY.md)** - Configurações e procedimentos
- **[Sistema IoT](README_IOT.md)** - Sensores ESP32 e integração completa
- **[Manual do Usuário](USER_MANUAL.md)** - Como usar o sistema (em desenvolvimento)

### 🔧 Documentação Técnica
- **[API Reference](API.md)** - Documentação da API (em desenvolvimento)
- **[Deployment Guide](DEPLOY.md)** - Guia de implantação (em desenvolvimento)

## 🛡️ Segurança

### Características de Segurança
- **Autenticação SHA-256** com salt personalizado
- **Sessões seguras** com tokens de 32 bytes
- **Criptografia Fernet** (AES-128) para dados sensíveis
- **Rate limiting** para tentativas de login
- **Anonimização** automática de dados

### Conformidade
- ✅ **LGPD** - Lei Geral de Proteção de Dados
- ✅ **CFM** - Conselho Federal de Medicina
- ✅ **ISO 27001** - Controles de segurança

## 🌟 Casos de Uso

### 🚑 Médicos Sem Fronteiras
- Triagem rápida em campos de refugiados
- Diagnóstico em áreas sem laboratório
- Apoio em surtos epidemiológicos

### 🌊 Desastres Naturais
- Atendimento pós-enchentes
- Triagem em abrigos temporários
- Monitoramento de doenças relacionadas ao clima

### 🏞️ Áreas Remotas
- Comunidades ribeirinhas
- Aldeias indígenas
- Regiões sem acesso a especialistas

### 🏥 Unidades Básicas de Saúde
- Apoio ao diagnóstico
- Capacitação de profissionais
- Padronização de atendimento

## 🔧 Requisitos Técnicos

### Dependências Principais
- Python 3.8+
- Streamlit 1.28+
- Pandas, NumPy, Scikit-learn
- Plotly (visualizações)
- Cryptography (segurança)
- **Flask** (API IoT)
- **Requests** (comunicação HTTP)

### Sistema IoT
- **ESP32** com WiFi
- **Sensor DS18B20** (temperatura)
- **Display OLED** (feedback visual)
- **Wokwi** para simulação virtual

### Recursos do Sistema
- **RAM**: Mínimo 2GB
- **Armazenamento**: 500MB
- **Rede**: Opcional (funciona offline)
- **Navegador**: Chrome, Firefox, Safari
- **Porta 5001**: Para API IoT (Flask)

## 📈 Algoritmo de IA

### Fórmula de Cálculo
```
Score Final = (Sintomas × 45%) + (Climático × 25%) + (População × 15%) + (Gravidade × 15%)
```

### Fatores Considerados
- **Sintomas clínicos**: Compatibilidade com a doença
- **Eventos climáticos**: Correlação epidemiológica
- **População de risco**: Vulnerabilidades específicas
- **Gravidade da doença**: Impacto na saúde pública

## 🤝 Contribuição

### Como Contribuir
1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

### Áreas de Contribuição
- 🩺 Expansão de doenças
- 🌍 Dados epidemiológicos regionais
- 🔒 Melhorias de segurança
- 🎨 Interface do usuário
- 📚 Documentação

## 📞 Suporte

### Contatos
- **Issues**: Use o sistema de issues do GitHub
- **Email**: suporte@triagem-medica.org
- **Documentação**: Consulte os guias na pasta `/docs`

### Comunidade
- **Discussões**: GitHub Discussions
- **Updates**: Acompanhe as releases
- **Feedback**: Sempre bem-vindo!

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE) - veja o arquivo LICENSE para detalhes.

## 🙏 Agradecimentos

Desenvolvido para apoiar profissionais de saúde que trabalham em condições desafiadoras, levando tecnologia e conhecimento médico para onde mais se precisa.

**Dedicado a todos os profissionais de saúde que atuam em áreas vulneráveis** 🌍❤️

---

**⚠️ Aviso Médico**: Este sistema é uma ferramenta de apoio ao diagnóstico e não substitui a avaliação médica profissional. Sempre considere o contexto clínico completo e procure atendimento especializado quando necessário. 