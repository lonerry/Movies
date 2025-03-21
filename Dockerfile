FROM python:3.11-slim

# Устанавливаем системные пакеты (компиляторы, заголовки PostgreSQL и т.п.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ build-essential libffi-dev libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install --upgrade pip && pip install poetry

WORKDIR /src

# 1. Копируем pyproject.toml и poetry.lock
COPY pyproject.toml poetry.lock /src/

# 2. Устанавливаем зависимости (без локального пакета или с ним — в зависимости от нужд)
RUN poetry install --no-root

# 3. Копируем весь остальной код
COPY Movies /src

EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
