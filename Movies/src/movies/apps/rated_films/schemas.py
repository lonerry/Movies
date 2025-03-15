from pydantic import BaseModel, Field, validator
from typing import Optional

class RatedFilmCreate(BaseModel):
    list_id: int
    movie_id: int
    rating_type: Optional[str] = Field(None, description="stars или poors")
    rating_value: Optional[int] = Field(None, description="1..3")
    watched: bool = False

    @validator("rating_value")
    def check_rating_value(cls, v):
        if v is not None and (v < 1 or v > 3):
            raise ValueError("rating_value must be between 1 and 3")
        return v

class RatedFilmUpdate(BaseModel):
    rating_type: Optional[str] = Field(None, description="stars или poors")
    rating_value: Optional[int] = Field(None, description="1..3")
    watched: Optional[bool] = None

class RatedFilmOut(BaseModel):
    id: int
    user_id: int
    movie_list_id: int
    movie_id: int
    rating_type: Optional[str] = None
    rating_value: Optional[int] = None
    watched: bool = False

    class Config:
        from_attributes = True
