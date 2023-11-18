ARG PYTHON_VERSION=3.12-slim-bullseye

FROM python:${PYTHON_VERSION}

# Встановимо змінну середовища
ENV APP_HOME /app

# Встановимо робочу директорію всередині контейнера
WORKDIR $APP_HOME

COPY poetry.lock $APP_HOME/poetry.lock
COPY pyproject.toml $APP_HOME/pyproject.toml

# Встановимо залежності всередині контейнера
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --only main

# Скопіюємо інші файли в робочу директорію контейнера
COPY . .

# Позначимо порт, де працює застосунок всередині контейнера
EXPOSE 8000

# Запустимо наш застосунок всередині контейнера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]