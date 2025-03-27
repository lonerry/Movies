from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import schemas, models
from src.movies.apps.auth.hash_password import hash_password


def get_all_users(db: Session):
    return db.query(models.User).all()


def get_user(db: Session, *, id=None, email=None, username=None):
    if sum(p is not None for p in (id, email, username)) != 1:
        raise ValueError("Provide exactly one of id, email, or username")

    if id:
        return db.query(models.User).filter_by(id=id).first()
    if email:
        return db.query(models.User).filter_by(email=email).first()
    if username:
        return db.query(models.User).filter_by(username=username).first()


def create_user(db: Session, request: schemas.UserCreate):
    if get_user(db, username=request.username):
        raise HTTPException(status_code=400, detail="Username is already taken")
    if get_user(db, email=request.email):
        raise HTTPException(status_code=400, detail="Email is already in use")

    new_user = models.User(
        username=request.username,
        email=request.email,
        password=hash_password(request.password),  # ✅ исправлено здесь
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
    db_user.password = hash_password(user.password)  # ✅ исправлено здесь

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
