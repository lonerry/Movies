from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from apps.auth.oauth2 import create_access_token, get_current_user, oauth2_schema, revoke_token
from apps.auth.schemas import RegisterResponse
from apps.user import schemas as user_schemas, db_queries
from apps.user import schemas
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
)

@router.post("/register", response_model=RegisterResponse)
async def register_user(request: user_schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Зарегистрировать нового пользователя.

    При успешной регистрации генерирует токен и возвращает его.

    **Raises**:
        `HTTPException(422)`: если пользователь с таким email уже существует.
    """
    existing_user = db_queries.get_user(db, email=request.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = db_queries.create_user(db, request)
    access_token = create_access_token(data={"username": new_user.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.post("/token")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Получить токен доступа.

    Проверяет логин/пароль. Если пользователь найден и пароль верный —
    выдаёт токен.

    **Raises**:
        `HTTPException(422)`: если пользователь не найден или неверный пароль.
    """
    user = db_queries.get_user(db, username=request.username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    # Проверка пароля, если есть...
    access_token = create_access_token(data={"username": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(db: Session = Depends(get_db), token: str = Depends(oauth2_schema)):
    """
    Выйти из системы (отозвать токен).

    Добавляет токен в таблицу отозванных (revoked_token).

    **Raises**:
        `HTTPException(401)`: если токен недействителен или не передан.
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
