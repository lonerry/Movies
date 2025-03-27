from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from db import Base

class RatedFilm(Base):
    __tablename__ = "rated_film"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    movie_list_id = Column(Integer, ForeignKey("movie_list.id"))
    movie_id = Column(Integer, ForeignKey("movie.id"))
    rating_type = Column(String(255), nullable=True)
    rating_value = Column(Integer, nullable=True)
    watched = Column(Boolean, default=False)
