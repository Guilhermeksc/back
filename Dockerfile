# Usa a imagem base do Python
FROM python:3.13.1-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    libpq-dev gcc postgresql-client \
    --no-install-recommends

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos do projeto
COPY . .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Coleta os arquivos estáticos
RUN python manage.py collectstatic --noinput

# Define o comando padrão ao rodar o container
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
