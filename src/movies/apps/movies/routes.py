from typing import Optional, List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db import get_db
from src.movies.apps.auth.oauth2 import get_current_user
from src.movies.apps.movies import db_queries
from src.movies.apps.movies import schemas

router = APIRouter(prefix="/movies", tags=["movies"])

@router.post("/create", response_model=schemas.MovieListBase)
def create_list(
    data: schemas.MovieListCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
        Создает новый список фильмов.

        Принимает:
          - data (MovieListCreate): данные, содержащие имя списка.

        Возвращает:
          - MovieListBase: объект с информацией о созданном списке (id и name).
        """
    return db_queries.create_movie_list(db, current_user.id, data)

@router.post("/lists/{list_id}/add", response_model=schemas.Movie)
def add_movie_to_list(
    list_id: int,
    data: schemas.MovieCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Добавляет новый фильм в существующий список.

    Принимает:
      - list_id (int): идентификатор списка фильмов.
      - data (MovieCreate): данные нового фильма (название и описание).

    Возвращает:
      - Movie: объект нового фильма, добавленного в список.
    """
    return db_queries.add_movie_to_list(db, current_user.id, list_id, data)

@router.post("/{list_id}")
def share_list(
    list_id: int,
    data: schemas.MovieListShareCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
       Делится списком фильмов с другим пользователем.

       Принимает:
         - list_id (int): идентификатор списка фильмов.
         - data (MovieListShareCreate): данные для шаринга, включая идентификатор друга и флаг can_edit.

       Возвращает:
         - MovieListShare: объект записи шаринга, показывающий, с кем расшаривается список и какие права предоставлены.
       """
    return db_queries.share_movie_list(db, current_user.id, list_id, data)


@router.get("/get_all_lists", response_model=List[schemas.MovieListDetail])
def get_all_lists(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    watched: Optional[bool] = Query(None, description="True - только просмотренные, False - только непросмотренные, None - все")
):
    """
       Возвращает все списки фильмов, доступные текущему пользователю.

       Принимает:
         - db (Session): сессия базы данных.

       Возвращает:
         - List[MovieListDetail]: список объектов с детальной информацией о каждом списке, включая фильмы с их оценками и список гостей.
       """
    lists = db_queries.get_all_lists_for_user(db, current_user.id)

    from src.movies.apps.movies.db_queries import fill_movies_with_rating

    result = []
    for lst in lists:
        movies_with_rating = fill_movies_with_rating(db, current_user.id, lst, watched)
        guests = [share.friend_id for share in lst.shares]

        item = schemas.MovieListDetail(
            id=lst.id,
            name=lst.name,
            movies=movies_with_rating,
            guests=guests
        )
        result.append(item)

    return result

@router.patch("{list_id}{movie_id}", response_model=schemas.Movie)
def update_movie_info_route(
    list_id: int,
    movie_id: int,
    data: schemas.MovieInfoUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Обновляет информацию о фильме в списке.

    Принимает:
      - list_id (int): идентификатор списка фильмов.
      - movie_id (int): идентификатор фильма.
      - data (MovieInfoUpdate): новые данные для обновления (например, новое название или описание).

    Возвращает:
      - Movie: обновленный объект фильма.
    """
    updated_movie = db_queries.update_movie_info(db, current_user.id, list_id, movie_id, data)
    return updated_movie
