from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import Base
from db import engine
from src.movies.apps.movies.routes import router as movies_router
from src.movies.apps.auth.routes import router as auth_router
from src.movies.apps.user.routes import router as user_router
from src.movies.apps.auth import routes as auth_routes
from src.movies.apps.rated_films.routes import router as rated_films_router

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

Base.metadata.create_all(bind=engine)


app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(movies_router)
app.include_router(user_router)
app.include_router(rated_films_router)
app.include_router(auth_routes.router)
