from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta, UTC
from jose import jwt
from jose.exceptions import JWTError
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from db import get_db
from src.movies.apps.user.db_queries import get_user
from src.movies.apps.auth.db_queries import add_revoked_token, is_token_revoked

# Определяем схему OAuth2 для получения токена из заголовка Authorization
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/token")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

# Функция для создания access token (JWT)
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# Функция для отзыва токена (добавляет токен в "черный список")
def revoke_token(db: Session, token: str):
    add_revoked_token(db, token)

# Зависимость для получения текущего пользователя на основе JWT токена
def get_current_user(
    token: str = Depends(oauth2_schema),
    db: Session = Depends(get_db)
):
    if is_token_revoked(db, token):
        raise _unauthorized("Token has been revoked")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if not username:
            raise ValueError
    except (JWTError, ValueError):
        raise _unauthorized("Invalid token")

    user = get_user(db, username=username)
    if not user:
        raise _unauthorized("User not found")

    return user

# Вспомогательная функция для формирования исключения 401 Unauthorized
def _unauthorized(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"}
    )
