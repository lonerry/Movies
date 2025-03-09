from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import Base
from db import engine

from apps.movies import routes as blog_routes
from apps.auth.routes import router as auth_router
from apps.user.routes import router as user_router
from apps.auth import routes as auth_routes
from apps.rated_films.routes import router as rated_films_router

import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные из .env

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

Base.metadata.create_all(bind=engine)


app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5500', 'http://127.0.0.1:5500'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get('/')
# async def root():
#     return {'message': 'This is root url'}
Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(user_router)

app.include_router(rated_films_router)
app.include_router(auth_router)
app.include_router(auth_routes.router)
app.include_router(blog_routes.router)