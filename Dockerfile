# Dockerfile para AWS App Runner - Sistema de Triagem Médica IoT
FROM python:3.9-slim

# Metadados
LABEL maintainer="Sistema de Triagem Médica"
LABEL description="Sistema de IA para Triagem Médica em Áreas Vulneráveis com IoT"

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    procps \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar todo o código da aplicação
COPY . .

# Criar diretórios necessários para dados
RUN mkdir -p data logs && \
    chmod 755 data logs

# Dar permissão de execução para scripts
RUN chmod +x start.sh

# Expor as portas que a aplicação usa
EXPOSE 8501 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Comando de inicialização
CMD ["./start.sh"] 