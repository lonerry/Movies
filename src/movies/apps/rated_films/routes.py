from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import Body
from db import get_db
from src.movies.apps.auth.oauth2 import get_current_user
from src.movies.apps.rated_films import schemas
from src.movies.apps.rated_films import db_queries

router = APIRouter(prefix="/rated-films", tags=["rated_films"])

@router.post("/create_rating", response_model=schemas.RatedFilmOut)
def create_or_update_rating(
    data: schemas.RatedFilmUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db_queries.create_or_update_rating(db, current_user.id, data)

@router.delete("/delete", response_model=schemas.RatedFilmOut)
def delete_rating(
    data: schemas.RatedFilmDelete = Body(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return db_queries.delete_rating(db, current_user.id, data)



