
Movies App — это веб-приложение на FastAPI, которое позволяет пользователям регистрироваться, создавать списки фильмов, добавлять фильмы в списки, оценивать их и делиться списками с другими пользователями.

Особенности:
1) Регистрация и авторизация пользователей с использованием JWT.

2) Создание и управление списками фильмов.

3) Добавление, оценка и обновление информации о фильмах.

4) Совместное использование списков с разными уровнями доступа (просмотр/редактирование).


Установка

Клонируйте репозиторий:

bash


git clone https://github.com/yourusername/movies-app.git

cd movies-app

Установите зависимости через Poetry:

bash

poetry install

Создайте файл .env с необходимыми переменными окружения:

ini


DATABASE_URL=mysql+pymysql://root:password@db:3306/my_database

SECRET_KEY=your_secret_key

MYSQL_ROOT_PASSWORD=your_mysql_root_password

ACCESS_TOKEN_EXPIRE_MINUTES=60

Запустите приложение:

bash

poetry run uvicorn main:app --host 0.0.0.0 --port 8000

Запуск через Docker

Убедитесь, что Docker и Docker Compose установлены.

Запустите контейнеры:

bash

docker-compose up --build

Приложение будет доступно по адресу http://localhost:8000.