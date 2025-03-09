from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import schemas, models
from apps.auth.hash_password import HashPassword

def get_all_users(db: Session):
    return db.query(models.User).all()

def get_user(db: Session, id: int = None, email: str = None, username: str = None):
    query = db.query(models.User)
    if id:
        return query.filter(models.User.id == id).first()
    if email:
        return query.filter(models.User.email == email).first()
    if username:
        return query.filter(models.User.username == username).first()

def create_user(db: Session, request: schemas.UserCreate):
    existing_username = get_user(db, username=request.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username is already taken")

    existing_email = get_user(db, email=request.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email is already in use")

    new_user = models.User(
        username=request.username,
        email=request.email,
        password=HashPassword.bcrypt(request.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def update_user(db: Session, user: schemas.UserCreate, user_id: int):
    db_user = get_user(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = HashPassword.bcrypt(user.password)

    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, id: int):
    db_user = get_user(db, id=id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User does not exist")
    db.delete(db_user)
    db.commit()
    return db_user
