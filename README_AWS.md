# 🚀 Deploy na AWS App Runner - Sistema de Triagem Médica IoT

## 📋 **Pré-requisitos**

### 🎓 **Conta AWS de Estudante**
- ✅ AWS Academy ($100 créditos)
- ✅ AWS Educate ($35-100 créditos)
- ✅ GitHub account (para deploy automático)

### 💰 **Custos Estimados**
- **AWS App Runner**: ~$15-25/mês
- **S3 Storage**: ~$1-3/mês
- **CloudWatch Logs**: ~$1-2/mês
- **Total**: ~$17-30/mês

**Com seus créditos de estudante = 3-4 meses GRÁTIS! 🎉**

---

## 🚀 **Opção 1: Deploy via GitHub (Recomendado)**

### **Passo 1: Preparar Repositório GitHub**

1. **Criar repositório no GitHub:**
   ```bash
   # No seu terminal local
   git init
   git add .
   git commit -m "Sistema de Triagem Médica IoT - Deploy AWS"
   git branch -M main
   git remote add origin https://github.com/SEU-USUARIO/triagem-medica-iot.git
   git push -u origin main
   ```

2. **Verificar arquivos necessários:**
   - ✅ `Dockerfile`
   - ✅ `start.sh`
   - ✅ `apprunner.yaml`
   - ✅ `requirements.txt`
   - ✅ `config.py`
   - ✅ Todos os arquivos `.py` da aplicação

### **Passo 2: Configurar AWS App Runner**

1. **Acessar AWS Console:**
   - Entre na sua conta AWS de estudante
   - Vá para **AWS App Runner**
   - Clique em **"Create service"**

2. **Configurar Source:**
   - **Source**: GitHub
   - **Repository**: `seu-usuario/triagem-medica-iot`
   - **Branch**: `main`
   - **Deployment trigger**: Automatic
   - **Configuration file**: `apprunner.yaml`

3. **Configurar Service:**
   - **Service name**: `triagem-medica-iot`
   - **Virtual CPU**: 0.25 vCPU
   - **Memory**: 0.5 GB
   - **Port**: 8501

4. **Configurar Health Check:**
   - **Path**: `/_stcore/health`
   - **Interval**: 30 seconds
   - **Timeout**: 10 seconds
   - **Healthy threshold**: 3
   - **Unhealthy threshold**: 3

5. **Configurar Auto Scaling:**
   - **Min instances**: 1
   - **Max instances**: 3
   - **Max concurrency**: 10

### **Passo 3: Deploy**

1. **Iniciar Deploy:**
   - Clique em **"Create & deploy"**
   - Aguarde 5-10 minutos para o build e deploy

2. **Verificar Status:**
   - Status deve mudar para **"Running"**
   - URL será gerada automaticamente

3. **Testar Aplicação:**
   - Acesse a URL fornecida
   - Teste login (admin/admin123)
   - Verifique Dashboard IoT

---

## 🐳 **Opção 2: Deploy via Docker Hub**

### **Passo 1: Build e Push da Imagem**

```bash
# Build da imagem
docker build -t triagem-medica-iot:latest .

# Tag para Docker Hub
docker tag triagem-medica-iot:latest SEU-USUARIO/triagem-medica-iot:latest

# Push para Docker Hub
docker push SEU-USUARIO/triagem-medica-iot:latest
```

### **Passo 2: Configurar App Runner**

1. **Source**: Container registry
2. **Image URI**: `SEU-USUARIO/triagem-medica-iot:latest`
3. **Port**: 8501
4. **Seguir mesmas configurações da Opção 1**

---

## 🔧 **Configurações Avançadas**

### **Variáveis de Ambiente**

```yaml
# No AWS App Runner Console
ENVIRONMENT=production
STREAMLIT_SERVER_PORT=8501
IOT_API_PORT=5001
AWS_REGION=us-east-1
DEBUG=false
```

### **Monitoramento**

1. **CloudWatch Logs:**
   - Log group: `/aws/apprunner/triagem-medica-iot`
   - Retention: 7 days (para economizar)

2. **Métricas:**
   - CPU Utilization
   - Memory Utilization
   - Request Count
   - Response Time

### **Domínio Personalizado (Opcional)**

1. **Registrar domínio no Route 53**
2. **Configurar certificado SSL**
3. **Associar ao App Runner service**

---

## 🛠️ **Solução de Problemas**

### **Build Falha**

```bash
# Verificar logs no AWS Console
# Problemas comuns:
# 1. requirements.txt incorreto
# 2. Dockerfile com erro
# 3. start.sh sem permissão de execução
```

### **Aplicação não Inicia**

```bash
# Verificar:
# 1. Porta 8501 configurada corretamente
# 2. Health check path correto
# 3. Variáveis de ambiente
```

### **API IoT não Funciona**

```bash
# Verificar:
# 1. Porta 5001 liberada internamente
# 2. start_iot_api.py executando
# 3. Arquivos JSON criados corretamente
```

---

## 📊 **Monitoramento de Custos**

### **AWS Cost Explorer**

1. **Configurar alertas de billing:**
   - Limite: $20/mês
   - Email de notificação

2. **Monitorar serviços:**
   - App Runner
   - CloudWatch
   - Data Transfer

### **Otimização de Custos**

1. **Auto Scaling agressivo:**
   - Min instances: 1
   - Scale down rápido

2. **Logs retention:**
   - 7 days máximo

3. **Parar serviço quando não usar:**
   - Pausar App Runner service
   - Reativar quando necessário

---

## 🔄 **CI/CD Automático**

### **GitHub Actions (Opcional)**

```yaml
# .github/workflows/deploy.yml
name: Deploy to AWS App Runner

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Deploy to App Runner
      run: |
        echo "Deploy automático configurado!"
        # AWS CLI commands aqui
```

---

## 📱 **URLs e Endpoints**

### **Aplicação Principal**
- **URL**: `https://SEU-SERVICE-ID.us-east-1.awsapprunner.com`
- **Health Check**: `/_stcore/health`

### **API IoT**
- **Base URL**: `https://SEU-SERVICE-ID.us-east-1.awsapprunner.com:5001`
- **Health**: `/api/health`
- **Sensor Data**: `/api/sensor-data` (POST)

---

## 🎯 **Próximos Passos**

### **Melhorias Futuras**

1. **Banco de Dados:**
   - RDS PostgreSQL
   - Backup automático

2. **Storage:**
   - S3 para arquivos
   - CloudFront CDN

3. **Segurança:**
   - WAF
   - Secrets Manager

4. **Monitoramento:**
   - X-Ray tracing
   - Custom metrics

---

## 📞 **Suporte**

### **Documentação AWS**
- [AWS App Runner](https://docs.aws.amazon.com/apprunner/)
- [AWS Free Tier](https://aws.amazon.com/free/)

### **Comunidade**
- [AWS re:Post](https://repost.aws/)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/aws-app-runner)

---

## ✅ **Checklist de Deploy**

- [ ] Repositório GitHub criado
- [ ] Arquivos de deploy commitados
- [ ] AWS App Runner service criado
- [ ] Health check configurado
- [ ] Auto scaling configurado
- [ ] Monitoramento ativo
- [ ] Alertas de custo configurados
- [ ] Aplicação testada
- [ ] API IoT funcionando
- [ ] Dashboard acessível

**🎉 Parabéns! Sua aplicação está rodando na AWS! 🎉** 