# Usar imagem Python oficial como base
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivo de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pandas pyarrow

# Copia o código da aplicação
COPY . .

# Criar diretórios para downloads e extrações
RUN mkdir -p extracted parquet

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expor porta (opcional, para interface web futura)
EXPOSE 8000

# Comando padrão (será sobrescrito pelo docker-compose)
CMD ["python", "importa_cnpj_parquet.py"] 