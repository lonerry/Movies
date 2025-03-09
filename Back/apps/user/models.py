from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import Base

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(100000))

    # Записи о просмотре (WatchedMovie)
    watched_movies = relationship("WatchedMovie", back_populates="user")

    # Несколько списков (MovieList)
    movie_lists = relationship("MovieList", back_populates="owner")
