
# 🎬 Movies App

**Movies App** — это веб-приложение на FastAPI, которое позволяет пользователям регистрироваться, создавать списки фильмов, добавлять фильмы в списки, оценивать их и делиться списками с другими пользователями.

## 🚀 Особенности

- ✅ Регистрация и авторизация пользователей с использованием **JWT**
- 📝 Создание и управление **списками фильмов**
- 🎞 Добавление, оценка и обновление информации о фильмах
- 🤝 Совместное использование списков с разными уровнями доступа (*просмотр / редактирование*)

## ⚙️ Установка

### 🔻 Клонирование репозитория

```bash
git clone https://github.com/lonerry/movies-app.git
cd movies-app
```

### 📦 Установка зависимостей через Poetry

```bash
poetry install
```

### 🔐 Создание `.env`

Создайте файл `.env` в корне проекта со следующим содержанием:

```ini
DATABASE_URL=mysql+pymysql://root:password@db:3306/my_database
SECRET_KEY=your_secret_key
MYSQL_ROOT_PASSWORD=your_mysql_root_password
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### ▶️ Запуск приложения

```bash
poetry run uvicorn main:app --host 0.0.0.0 --port 8000
```

Документация будет доступна по адресу:  
👉 http://localhost:8000/docs

## 🐳 Запуск через Docker

Убедитесь, что установлены **Docker** и **Docker Compose**.

### ▶️ Запуск контейнеров

```bash
docker-compose up --build
```

Приложение будет доступно по адресу:  
👉 http://localhost:8000

## 🧾 Пример `.env`

```ini
DATABASE_URL=mysql+pymysql://root:password@db:3306/movies_db
SECRET_KEY=supersecretkey
MYSQL_ROOT_PASSWORD=secure_root_password
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## 🛠 Планы на будущее

- 📮 Уведомления о новых фильмах в списке
- 📊 Статистика и рекомендации
- 🌐 Интеграция с внешними API (TMDb, IMDb)
- 🧪 Покрытие тестами с использованием `pytest` и `httpx`
