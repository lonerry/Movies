from sqlalchemy.orm import Session, joinedload
from src.movies.apps.auth.models import RevokedToken
from src.movies.apps.movies.models import Movie

def add_revoked_token(db: Session, token: str):
    """
    Добавляет токен в таблицу revoked_token.
    """
    revoked = RevokedToken(token=token)
    db.add(revoked)
    db.commit()
    db.refresh(revoked)
    return revoked

def is_token_revoked(db: Session, token: str) -> bool:
    """
    Проверяет, есть ли токен в таблице revoked_token.
    Возвращает True, если отозван, False – если нет.
    """
    revoked = db.query(RevokedToken).filter(RevokedToken.token == token).first()
    return revoked is not None

def get_all_movies_with_statuses(db: Session):
    """
    Возвращает все фильмы вместе со списком WatchedMovie.
    """
    # joinedload("watched_by") подгрузит список WatchedMovie для каждого Movie
    return db.query(Movie).options(joinedload(Movie.watched_by)).all()