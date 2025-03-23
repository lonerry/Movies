from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import Body
from db import get_db
from src.movies.apps.auth.oauth2 import get_current_user
from src.movies.apps.rated_films import schemas
from src.movies.apps.rated_films import db_queries

router = APIRouter(prefix="/rated-films", tags=["rated_films"])

@router.post("/", response_model=schemas.RatedFilmOut)
def create_or_update_rating(
    data: schemas.RatedFilmCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Создаёт или обновляет оценку и статус просмотра фильма в рамках конкретного списка.

    - list_id: ID списка, в котором оцениваем фильм
    - movie_id: ID фильма, который принадлежит этому списку
    - rating_type: "stars" или "poors"
    - rating_value: 1..3
    - watched: True/False

    **Права**: владелец списка или гость с can_edit=True
    """
    return db_queries.create_or_update_rating(db, current_user.id, data)


@router.patch("/", response_model=schemas.RatedFilmOut)
def update_rating(
    data: schemas.RatedFilmUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db_queries.update_rating(db, current_user.id, data)



@router.delete("/", response_model=schemas.RatedFilmOut)
def delete_rating(
    data: schemas.RatedFilmDelete = Body(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db_queries.delete_rating(db, current_user.id, data)



@router.get("/", response_model=List[schemas.RatedFilmOut])
def get_user_ratings(
    watched: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Получить список всех фильмов (RatedFilm), которые пользователь оценил
    (в любых списках).
    - Параметр watched=True/False фильтрует только просмотренные/непросмотренные.
    """
    rated_films = db_queries.get_user_ratings(db, current_user.id, watched)
    return rated_films
