from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from . import schemas, db_queries

router = APIRouter(
    prefix='/user',
    tags=['user'],
)

@router.get("/get-all", response_model=schemas.UserListResponse)
def get_all_users(db: Session = Depends(get_db)):
    """
       Возвращает:
         - UserListResponse: объект, содержащий общее количество пользователей и список деталей каждого пользователя.
       """
    users = db_queries.get_all_users(db)
    return {
        "count": len(users),
        "results": users
    }

@router.get('/{id}', response_model=schemas.UserDetails, summary='Get User By Id')
def get_user(id: int = None, db: Session = Depends(get_db)):
    """
       Принимает:
         - id (int): идентификатор пользователя.

       Возвращает:
         - UserDetails: объект с деталями пользователя (id, username, email).

       Генерирует HTTPException с кодом 404, если пользователь не найден.
       """
    user = db_queries.get_user(db, id=id)
    if not user:
        raise HTTPException(status_code=404, detail='There is no user in db with such credentials')
    return user
