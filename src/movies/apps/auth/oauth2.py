from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt
from jose.exceptions import JWTError
from sqlalchemy.orm import Session

from db import get_db
from src.movies.apps.user.db_queries import get_user
from src.movies.apps.auth.db_queries import add_revoked_token, is_token_revoked

oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/token')

SECRET_KEY = '52367badbf4e42f3a94d9ce456e1f01cbfee36a604da5c9589fa84f0bb9e661b'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 20

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def revoke_token(db: Session, token: str):
    """
    Добавляет токен в БД как отозванный.
    """
    add_revoked_token(db, token)

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    # 1. Проверяем, нет ли токена в таблице revoked_token
    if is_token_revoked(db, token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={'WWW-Authenticate': 'Bearer'}
        )

    # 2. Декодируем JWT
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        decode_username: str = payload.get('username')
        if decode_username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # 3. Получаем пользователя из БД
    user = get_user(db, username=decode_username)
    if user is None:
        raise credentials_exception

    return user
