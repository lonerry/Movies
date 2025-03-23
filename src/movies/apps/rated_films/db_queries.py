from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from src.movies.apps.rated_films.models import RatedFilm
from src.movies.apps.rated_films import schemas

from src.movies.apps.movies.models import Movie, MovieList, MovieListShare


def create_or_update_rating(
    db: Session,
    user_id: int,
    data: schemas.RatedFilmCreate
):
    """
    Создаёт или обновляет оценку/статус для (user_id, list_id, movie_id).
    """

    # 1) Проверяем, что список существует
    movie_list = db.query(MovieList).filter(MovieList.id == data.list_id).first()
    if not movie_list:
        raise HTTPException(status_code=404, detail="MovieList not found")

    # 2) Проверяем, есть ли фильм в этом списке
    movie = db.query(Movie).filter(
        Movie.id == data.movie_id,
        Movie.movie_list_id == data.list_id
    ).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found in this list")

    # 3) Проверяем права: владелец или share.can_edit=True
    is_owner = (movie_list.user_id == user_id)
    share_record = db.query(MovieListShare).filter_by(
        movie_list_id=data.list_id,
        friend_id=user_id
    ).first()

    can_edit = False
    if share_record and share_record.can_edit:
        can_edit = True

    if not (is_owner or can_edit):
        raise HTTPException(status_code=403, detail="No permission to rate this list")

    # 4) Ищем существующую запись RatedFilm
    rated = db.query(RatedFilm).filter(
        RatedFilm.user_id == user_id,
        RatedFilm.movie_list_id == data.list_id,
        RatedFilm.movie_id == data.movie_id
    ).first()

    if not rated:
        # Создаём новую
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
        # Обновляем
        if data.rating_type is not None:
            rated.rating_type = data.rating_type
        if data.rating_value is not None:
            rated.rating_value = data.rating_value
        rated.watched = data.watched

    db.commit()
    db.refresh(rated)
    return rated


def update_rating(
    db: Session,
    user_id: int,
    data: schemas.RatedFilmUpdate
):

    """
    Частично обновляет запись RatedFilm (rating_type, rating_value, watched).
    Проверяем права через movie_list_id.
    """
    rated = db.query(RatedFilm).filter_by(
        user_id=user_id,
        movie_list_id=data.list_id,
        movie_id=data.movie_id
    ).first()

    if not rated:
        raise HTTPException(status_code=404, detail="RatedFilm not found")

    # Проверяем список
    movie_list = db.query(MovieList).filter(MovieList.id == rated.movie_list_id).first()
    if not movie_list:
        raise HTTPException(status_code=404, detail="MovieList not found")

    # Проверяем права
    is_owner = (movie_list.user_id == user_id)
    share_record = db.query(MovieListShare).filter_by(
        movie_list_id=movie_list.id,
        friend_id=user_id
    ).first()
    can_edit = False
    if share_record and share_record.can_edit:
        can_edit = True

    if not (is_owner or can_edit):
        raise HTTPException(status_code=403, detail="No permission to update this rating")

    # Обновляем поля
    if data.rating_type is not None:
        rated.rating_type = data.rating_type
    if data.rating_value is not None:
        rated.rating_value = data.rating_value
    if data.watched is not None:
        rated.watched = data.watched

    db.commit()
    db.refresh(rated)
    return rated


def delete_rating(
    db: Session,
    user_id: int,
    data: schemas.RatedFilmDelete
):
    rated = db.query(RatedFilm).filter_by(
        user_id=user_id,
        movie_list_id=data.list_id,
        movie_id=data.movie_id
    ).first()
    if not rated:
        raise HTTPException(status_code=404, detail="RatedFilm not found")

    movie_list = db.query(MovieList).filter(MovieList.id == data.list_id).first()
    if not movie_list:
        raise HTTPException(status_code=404, detail="MovieList not found")

    is_owner = (movie_list.user_id == user_id)
    share_record = db.query(MovieListShare).filter_by(
        movie_list_id=data.list_id,
        friend_id=user_id
    ).first()
    can_edit = share_record and share_record.can_edit

    if not (is_owner or can_edit):
        raise HTTPException(status_code=403, detail="No permission to delete this rating")

    db.delete(rated)
    db.commit()
    return rated


def get_user_ratings(
    db: Session,
    user_id: int,
    watched: Optional[bool] = None
):
    """
    Получает список RatedFilm для конкретного user_id.
    Можно фильтровать watched=True/False.
    """
    query = db.query(RatedFilm).filter(RatedFilm.user_id == user_id)
    if watched is not None:
        query = query.filter(RatedFilm.watched == watched)
    return query.all()
