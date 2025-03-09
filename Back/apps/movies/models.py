from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

# Импортируем User из папки user
from apps.user.models import User

class MovieList(Base):
    __tablename__ = "movie_list"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="movie_lists")

    movies = relationship("Movie", back_populates="movie_list", cascade="all, delete-orphan")
    shares = relationship("MovieListShare", back_populates="movie_list", cascade="all, delete-orphan")

class MovieListShare(Base):
    __tablename__ = "movie_list_share"

    id = Column(Integer, primary_key=True, index=True)
    movie_list_id = Column(Integer, ForeignKey("movie_list.id"))
    friend_id = Column(Integer, ForeignKey("user.id"))
    can_edit = Column(Boolean, default=False)  # True => гость может редактировать

    movie_list = relationship("MovieList", back_populates="shares")
    # friend = relationship("User")  # если нужно

class Movie(Base):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(1000), nullable=True)

    movie_list_id = Column(Integer, ForeignKey("movie_list.id"))
    movie_list = relationship("MovieList", back_populates="movies")

    watched_by = relationship("WatchedMovie", back_populates="movie")

class WatchedMovie(Base):
    __tablename__ = "watched_movie"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movie.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    rating_type = Column(String(255), nullable=True)
    rating_value = Column(Integer, nullable=True)

    movie = relationship("Movie", back_populates="watched_by")
    user = relationship("User", back_populates="watched_movies")
