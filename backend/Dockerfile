# Backend Dockerfile - Produção
FROM python:3.12-slim

# Configurações de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_ENV=production

# Definir diretório de trabalho
WORKDIR /app

# Criar usuário não-root para segurança
RUN groupadd -r appuser && useradd -r -u 1000 -g appuser -m appuser

# Copiar requirements primeiro (para cache de dependências)
COPY requirements.txt .

# Instalar dependências do sistema e Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY --chown=appuser:appuser app.py wsgi.py config.py extensions.py ./
COPY --chown=appuser:appuser models models/
COPY --chown=appuser:appuser routes routes/
COPY --chown=appuser:appuser seed seed/

# Mudar para usuário não-root
USER appuser

# Expor porta
EXPOSE 5000

# Comando para iniciar em produção com gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "wsgi:app"]
