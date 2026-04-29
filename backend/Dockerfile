# Usar Python 3.12 slim
FROM python:3.12-slim

# Definir diretório de trabalho
WORKDIR /app

# Expor porta do Flask
EXPOSE 5000

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copiar requirements primeiro (para cache de dependências)
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação (exceto arquivos desnecessários)
COPY app.py wsgi.py config.py extensions.py ./
COPY models models/
COPY routes routes/

# Criar diretório instance para SQLite (se usado em desenvolvimento)
RUN mkdir -p /app/instance

# Usuário não-root para segurança
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Comando para iniciar Flask em modo produção
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "wsgi:app"]