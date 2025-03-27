from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db import get_db
from src.movies.apps.auth.oauth2 import (
    create_access_token,
    get_current_user,
    oauth2_schema,
    revoke_token,
)
from src.movies.apps.user import schemas, db_queries
from src.movies.apps.user.schemas import UserCreate, UserUpdate
from src.movies.apps.auth.hash_password import hash_password, verify_password
router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)


@router.post("/register", status_code=201)
def register_user(request: UserCreate, db: Session = Depends(get_db)):
    """
             Регистрирует нового пользователя.

             Принимает:
               - request (UserCreate): данные для регистрации (username, email, password).

             Возвращает:
               - Сообщение "Successfully registered!" при успешной регистрации.

             Генерирует HTTPException с кодом 400, если пользователь с таким email уже существует.
             """
    if db_queries.get_user(db, email=request.email):

        raise HTTPException(status_code=400, detail="User already exists")
    db_queries.create_user(db, request)
    return "Successfully registered!"


@router.post("/token", status_code=status.HTTP_200_OK)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
        Выполняет аутентификацию пользователя и возвращает JWT токен.

        Принимает:
          - form_data (OAuth2PasswordRequestForm): данные для входа (username и password).
        Возвращает:
          - json с полями "access_token" и "token_type"(bearer)

        Генерирует HTTPException с кодом 401, если аутентификация не проходит.
        """
    user = db_queries.get_user(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"username": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_schema),
):
    """
       Выполняет logout, отзывая текущий JWT токен.
    """

    revoke_token(db, token)
    return {"message": "Successfully logged out"}


@router.patch("/update", response_model=schemas.UserDetails)
def update_user(
    request: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
        Обновляет данные текущего пользователя.

        Принимает:
          - request (UserUpdate): новые данные для пользователя.

        Возвращает:
          - UserDetails: объект с обновленной информацией о пользователе.

        Генерирует HTTPException, если обновление не удалось.
        """

    updated_user = db_queries.update_user(db, user=request, user_id=current_user.id)
    if not updated_user:
        raise HTTPException(status_code=400, detail="User update failed")

    return updated_user


@router.delete("/delete", response_model=schemas.User)
def delete_user(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
        Удаляет текущего пользователя.

        Генерирует HTTPException, если пользователь не найден.
        """
    user = db_queries.get_user(db, id=current_user.id)
    if not user:
        raise HTTPException(status_code=400, detail="User does not exist")

    return db_queries.delete_user(db, current_user.id)
