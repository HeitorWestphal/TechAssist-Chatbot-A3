# Dockerfile de Produção para TechAssist AI
FROM python:3.11-slim

# Metadados
LABEL maintainer="TechAssist AI Solutions"
LABEL description="TechAssist AI - Helpdesk Inteligente N1 com PLN e SQLite"
LABEL version="1.2.0"

# Variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# Instalação de dependências do sistema necessárias para compilação leve
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia código da aplicação
COPY . /app/

# Criação de usuário não-root por segurança
RUN useradd -m techuser && chown -R techuser:techuser /app
USER techuser

# Porta exposta da API Web
EXPOSE 5000

# Healthcheck nativo Docker
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Comando padrão de execução
CMD ["python", "-m", "src.app_web"]
