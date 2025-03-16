from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from src.movies.apps.auth.oauth2 import create_access_token, get_current_user, oauth2_schema, revoke_token
from src.movies.apps.user.schemas import UserCreate
from src.movies.apps.user import schemas, db_queries
from .hash_password import HashPassword
from fastapi import status
from .schemas import LoginSchema
router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

@router.post("/register", status_code=201)
async def register_user(request: UserCreate, db: Session = Depends(get_db)):
    """
    Зарегистрировать нового пользователя.
    Ничего не возвращает (при успехе 201 Created).
    """
    existing_user = db_queries.get_user(db, email=request.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    # Создаём нового пользователя
    db_queries.create_user(db, request)
    # Просто завершаем без возвращаемых данных
    return

@router.post("/login")
def login(request: LoginSchema, db: Session = Depends(get_db)):
    """
    Логин по JSON:
    {
      "username": "...",
      "password": "..."
    }

    Возвращает JSON с ключом "token".
    """
    user = db_queries.get_user(db, username=request.username)
    # Проверяем, что пользователь существует и пароль совпадает
    if not user or not HashPassword.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = create_access_token(data={"username": user.username})
    return {"token": access_token}

@router.post("/logout")
def logout(db: Session = Depends(get_db), token: str = Depends(oauth2_schema)):
    """
    Выйти из системы (отозвать токен).
    """
    revoke_token(db, token)
    return {"message": "Successfully logged out"}

@router.patch("/update", response_model=schemas.UserDetails)
async def update_user(
    request: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Обновить данные пользователя (username/email/password).

    **Raises**:
        `HTTPException(422)`: при ошибке обновления.
    """
    updated_user = db_queries.update_user(db, user=request, user_id=current_user.id)
    if not updated_user:
        raise HTTPException(status_code=400, detail="User update failed")
    return updated_user

@router.delete("/delete", response_model=schemas.User)
async def delete_user(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Удалить текущего пользователя.

    **Raises**:
        `HTTPException(422)`: если пользователь не существует.
    """
    user_to_delete = db_queries.get_user(db, id=current_user.id)
    if not user_to_delete:
        raise HTTPException(status_code=400, detail="User does not exist")
    return db_queries.delete_user(db, current_user.id)
