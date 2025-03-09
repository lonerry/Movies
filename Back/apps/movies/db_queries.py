from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import Optional

from apps.movies.models import MovieList, Movie, MovieListShare
from apps.movies import schemas
from apps.user.models import User
from apps.rated_films.models import RatedFilm  # <-- Импортируем RatedFilm

def fill_movies_with_rating(
    db: Session,
    user_id: int,
    movie_list,
    filter_watched: Optional[bool] = None
):
    """
    Превращает movie_list.movies -> список MovieWithRating,
    подставляя rating_type, rating_value, watched из rated_film (если есть).
    Если filter_watched=True, возвращаем только просмотренные.
    Если filter_watched=False, только непросмотренные.
    Если None, возвращаем все.
    """
    result = []
    for m in movie_list.movies:
        # Ищем запись в rated_film (RatedFilm) для текущего user_id
        rated = db.query(RatedFilm).filter_by(
            user_id=user_id,
            movie_list_id=movie_list.id,
            movie_id=m.id
        ).first()

        if rated:
            rating_type = rated.rating_type
            rating_value = rated.rating_value
            watched_flag = rated.watched if hasattr(rated, "watched") else False
        else:
            rating_type = None
            rating_value = None
            watched_flag = False

        # Если фильтр по watched задан, пропускаем те, что не совпадают
        if filter_watched is not None and watched_flag != filter_watched:
            continue

        movie_with_rating = schemas.MovieWithRating(
            id=m.id,
            title=m.title,
            description=m.description,
            rating_type=rating_type,
            rating_value=rating_value,
            watched=watched_flag
        )
        result.append(movie_with_rating)
    return result



def create_movie_list(db: Session, user_id: int, data: schemas.MovieListCreate):
    new_list = MovieList(name=data.name, user_id=user_id)
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list


def add_movie_to_list(db: Session, user_id: int, list_id: int, data: schemas.MovieCreate):
    movie_list = db.query(MovieList).filter(MovieList.id == list_id).first()
    if not movie_list:
        raise HTTPException(status_code=404, detail="List not found")

    # Проверяем права
    share_record = db.query(MovieListShare).filter_by(movie_list_id=list_id, friend_id=user_id, can_edit=True).first()
    is_owner = (movie_list.user_id == user_id)
    if not (is_owner or share_record):
        raise HTTPException(status_code=403, detail="No permission to edit this list")

    new_movie = Movie(
        title=data.title,
        description=data.description,
        movie_list_id=list_id
    )
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie


def share_movie_list(db: Session, user_id: int, list_id: int, data: schemas.MovieListShareCreate):
    movie_list = db.query(MovieList).filter(MovieList.id == list_id, MovieList.user_id == user_id).first()
    if not movie_list:
        raise HTTPException(status_code=404, detail="List not found or not owned by user")

    existing_share = db.query(MovieListShare).filter_by(movie_list_id=list_id, friend_id=data.friend_id).first()
    if existing_share:
        existing_share.can_edit = data.can_edit
        db.commit()
        db.refresh(existing_share)
        return existing_share

    new_share = MovieListShare(
        movie_list_id=list_id,
        friend_id=data.friend_id,
        can_edit=data.can_edit
    )
    db.add(new_share)
    db.commit()
    db.refresh(new_share)
    return new_share


def get_movie_list(db: Session, user_id: int, list_id: int):
    """
    Возвращаем список, если user_id владелец или guest
    """
    from sqlalchemy import or_, and_
    q = db.query(MovieList).outerjoin(
        MovieListShare,
        MovieList.id == MovieListShare.movie_list_id
    ).filter(
        MovieList.id == list_id,
        or_(
            MovieList.user_id == user_id,
            and_(MovieListShare.friend_id == user_id)
        )
    )
    movie_list = q.first()
    if not movie_list:
        raise HTTPException(status_code=404, detail="List not found or no access")
    return movie_list


def get_all_lists_for_user(db: Session, user_id: int):
    from sqlalchemy import or_
    q = db.query(MovieList).outerjoin(
        MovieListShare,
        MovieList.id == MovieListShare.movie_list_id
    ).filter(
        or_(
            MovieList.user_id == user_id,
            MovieListShare.friend_id == user_id
        )
    )
    return q.all()

def update_movie_info(
    db: Session,
    user_id: int,
    list_id: int,
    movie_id: int,
    data: schemas.MovieInfoUpdate
):
    """
    Обновляет название и/или описание фильма в указанном списке.
    Проверяем, что user_id владелец или share.can_edit=True.
    """
    # 1) Проверяем, что список существует
    movie_list = db.query(MovieList).filter(MovieList.id == list_id).first()
    if not movie_list:
        raise HTTPException(status_code=404, detail="List not found")

    # 2) Проверяем права
    is_owner = (movie_list.user_id == user_id)
    share_record = db.query(MovieListShare).filter_by(
        movie_list_id=list_id,
        friend_id=user_id,
        can_edit=True
    ).first()

    if not (is_owner or share_record):
        raise HTTPException(status_code=403, detail="No permission to edit this list")

    # 3) Ищем фильм в этом списке
    movie = db.query(Movie).filter(
        Movie.id == movie_id,
        Movie.movie_list_id == list_id
    ).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found in this list")

    # 4) Обновляем поля
    if data.new_title is not None:
        movie.title = data.new_title
    if data.new_description is not None:
        movie.description = data.new_description

    db.commit()
    db.refresh(movie)
    return movie
