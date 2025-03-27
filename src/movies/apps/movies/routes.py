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
    return db_queries.create_movie_list(db, current_user.id, data)

@router.post("/lists/{list_id}/add", response_model=schemas.Movie)
def add_movie_to_list(
    list_id: int,
    data: schemas.MovieCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db_queries.add_movie_to_list(db, current_user.id, list_id, data)

@router.post("/{list_id}")
def share_list(
    list_id: int,
    data: schemas.MovieListShareCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    return db_queries.share_movie_list(db, current_user.id, list_id, data)


@router.get("/get_all_lists", response_model=List[schemas.MovieListDetail])
def get_all_lists(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    watched: Optional[bool] = Query(None, description="True - только просмотренные, False - только непросмотренные, None - все")
):

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
    updated_movie = db_queries.update_movie_info(db, current_user.id, list_id, movie_id, data)
    return updated_movie
