# poetry export --without-hashes --format=requirements.txt > requirements.txt

# python -c 'import secrets; print(secrets.token_urlsafe())'

# goit_personal_assistant

В одном уровне с модулем manage.py небходимо добавить файл .env,
там прописать переменные окружения:

# Django

DEBUG=True
DJANGO_SECRET_KEY=<...>

# PostgreSQL DB

DB_NAME=<...>
DB_USER=<...>
DB_PASSWORD=<...>
DB_HOST=<...>
DB_PORT=5432 -->

# Email

EMAIL_HOST=<...>
EMAIL_PORT=<...>
EMAIL_HOST_USER=<...>
EMAIL_HOST_PASSWORD=<...>

# Cloudinary

CLOUD_NAME=<...>
API_KEY=<...>
API_SECRET=<...>
