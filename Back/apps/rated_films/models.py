from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class RatedFilm(Base):
    __tablename__ = "rated_film"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    movie_list_id = Column(Integer, ForeignKey("movie_list.id"))
    movie_id = Column(Integer, ForeignKey("movie.id"))

    rating_type = Column(String(255), nullable=True)   # "stars" или "poors"
    rating_value = Column(Integer, nullable=True) # 1..3

    # Добавляем это поле, если хотим хранить watched
    watched = Column(Boolean, default=False)
