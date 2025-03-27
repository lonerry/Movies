from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from src.movies.apps.rated_films.models import RatedFilm
from src.movies.apps.rated_films import schemas
from src.movies.apps.movies.models import Movie, MovieList, MovieListShare

# Функция проверки прав доступа к списку фильмов
def _check_list_permissions(db: Session, user_id: int, list_id: int, can_edit_required: bool = False):
    movie_list = db.query(MovieList).filter(MovieList.id == list_id).first()
    if not movie_list:
        raise HTTPException(status_code=404, detail="MovieList not found")

    if movie_list.user_id == user_id:
        return movie_list

    share = db.query(MovieListShare).filter_by(
        movie_list_id=list_id,
        friend_id=user_id
    ).first()

    if not share or (can_edit_required and not share.can_edit):
        raise HTTPException(status_code=403, detail="No permission")

    return movie_list

# Функция создания или обновления оценки фильма
def create_or_update_rating(db: Session, user_id: int, data: schemas.RatedFilmUpdate):
    _check_list_permissions(db, user_id, data.list_id, can_edit_required=True)

    movie = db.query(Movie).filter(
        Movie.id == data.movie_id,
        Movie.movie_list_id == data.list_id
    ).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found in this list")

    rated = db.query(RatedFilm).filter_by(
        user_id=user_id,
        movie_list_id=data.list_id,
        movie_id=data.movie_id
    ).first()

    if not rated:
        rated = RatedFilm(
            user_id=user_id,
            movie_list_id=data.list_id,
            movie_id=data.movie_id,
            rating_type=data.rating_type,
            rating_value=data.rating_value,
            watched=data.watched
        )
        db.add(rated)
    else:
        if data.rating_type is not None:
            rated.rating_type = data.rating_type
        if data.rating_value is not None:
            rated.rating_value = data.rating_value
        rated.watched = data.watched

    db.commit()
    db.refresh(rated)
    return rated

# Функция обновления существующей оценки
def update_rating(db: Session, user_id: int, data: schemas.RatedFilmUpdate):
    rated = db.query(RatedFilm).filter_by(
        user_id=user_id,
        movie_list_id=data.list_id,
        movie_id=data.movie_id
    ).first()
    if not rated:
        raise HTTPException(status_code=404, detail="RatedFilm not found")

    _check_list_permissions(db, user_id, rated.movie_list_id, can_edit_required=True)

    if data.rating_type is not None:
        rated.rating_type = data.rating_type
    if data.rating_value is not None:
        rated.rating_value = data.rating_value
    if data.watched is not None:
        rated.watched = data.watched

    db.commit()
    db.refresh(rated)
    return rated

# Функция удаления оценки
def delete_rating(db: Session, user_id: int, data: schemas.RatedFilmDelete):
    rated = db.query(RatedFilm).filter_by(
        user_id=user_id,
        movie_list_id=data.list_id,
        movie_id=data.movie_id
    ).first()
    if not rated:
        raise HTTPException(status_code=404, detail="RatedFilm not found")

    _check_list_permissions(db, user_id, data.list_id, can_edit_required=True)

    db.delete(rated)
    db.commit()
    return rated

# Функция получения всех оценок пользователя, с возможной фильтрацией по статусу "watched"
def get_user_ratings(db: Session, user_id: int, watched: Optional[bool] = None):
    query = db.query(RatedFilm).filter(RatedFilm.user_id == user_id)
    if watched is not None:
        query = query.filter(RatedFilm.watched == watched)
    return query.all()
