FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc g++ build-essential libffi-dev libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && pip install poetry

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock /app/
RUN poetry install --no-root

COPY . /app
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["sh", "-c", "/wait-for-it.sh db:3306 -- poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --app-dir /app"]
