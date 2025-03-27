from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_engine(DATABASE_URL)#движок SQLAlchemy для подключения к бд

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)#Фабрика сессий

Base = declarative_base()

# Функция-генератор для получения сессии
def get_db():
    db = SessionLocal()  # Создаем новую сессию
    try:
        yield db       # Передаем сессию в эндпоинт
    finally:
        db.close()     # Гарантируем закрытие сессии после завершения запроса
