from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from . import schemas, db_queries

router = APIRouter(
    prefix='/user',
    tags=['user'],
)

@router.get("/get-all", response_model=schemas.UserListResponse)
async def get_all_users(db: Session = Depends(get_db)):
    """
    Получить всех пользователей.

    Возвращает список всех зарегистрированных пользователей.

    **Raises**:
        `HTTPException(401)`: если пользователь не авторизован.
        `HTTPException(500)`: при внутренних ошибках сервера.
    """
    users = db_queries.get_all_users(db)
    return {
        "count": len(users),
        "results": users
    }

@router.get('/{id}', response_model=schemas.UserDetails, summary='Get User By Id')
async def get_user(id: int = None, db: Session = Depends(get_db)):
    """
    Получить данные конкретного пользователя по его ID.

    **Raises**:
        `HTTPException(404)`: если пользователь с таким ID не найден.
    """
    user = db_queries.get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail='There is no user in db with such credentials')
    return user
