# Imagem base Python 3.10 slim
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Variáveis de ambiente para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas o requirements.txt primeiro para otimizar cache
COPY requirements.txt .

# Instala dependências Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Baixa stopwords do NLTK
RUN python -c "import nltk; nltk.download('stopwords')"

# Copia o restante do código da aplicação
COPY app/ ./app/
COPY models/ ./models/

# Expõe a porta da API
EXPOSE 8000

# Comando para rodar a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
