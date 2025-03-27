from typing import Optional, List
from pydantic import BaseModel

class MovieCreate(BaseModel):
    title: str
    description: Optional[str] = None


class Movie(BaseModel):
    id: int
    title: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class MovieWithRating(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    rating_type: Optional[str] = None    # e.g. "stars", "poors"
    rating_value: Optional[int] = None   # 1..3
    watched: bool = False

    class Config:
        from_attributes = True


class MovieInfoUpdate(BaseModel):
    new_title: Optional[str] = None
    new_description: Optional[str] = None


class MovieStatusUpdate(BaseModel):
    watched: Optional[bool] = None
    rating_type: Optional[str] = None
    rating_value: Optional[int] = None


class MovieListCreate(BaseModel):
    name: str


class MovieListBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class MovieListDetail(BaseModel):
    id: int
    name: str
    movies: List[MovieWithRating] = []
    guests: List[int] = []

    class Config:
        from_attributes = True

class MovieListShareCreate(BaseModel):
    friend_id: int
    can_edit: bool = False
