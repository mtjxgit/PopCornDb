"""
This module defines the SQLAlchemy models for the application.
"""

from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database.database import Base
# pylint: disable=R0903
class News(Base):
    """
    Model for the news table.
    """
    __tablename__ = "news"
    index = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    desc = Column(String)
    image_url = Column(String)
    href = Column(String)

class Watchlist(Base):
    """
    Model for the watchlists table.
    """
    __tablename__ = "watchlists"
    watchlist_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    movie_id = Column(Integer, ForeignKey('movies.index'))
    users = relationship('Users', back_populates='watchlist')
    movie = relationship('Movies', back_populates='watchlist')

class Movies(Base):
    """
    Model for the movies table.
    """
    __tablename__ = 'movies'
    index = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    image_url = Column(String)
    rating = Column(String)
    genre = Column(String)
    desc = Column(String)
    year = Column(String)
    runtime = Column(String)
    certificate = Column(String)
    ott = Column(String)
    ott_image = Column(String)
    directors = Column(String)
    writers = Column(String)
    stars = Column(String)
    raters = relationship('Ratings', back_populates='movie')
    watchlist = relationship('Watchlist', back_populates='movie')

class Ratings(Base):
    """
    Model for the ratings table.
    """
    __tablename__ = 'ratings'
    rating_id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey('movies.index'), nullable=False)
    user_id = Column(Integer)
    rating = Column(Float)
    movie = relationship('Movies', back_populates='raters')

class Users(Base):
    """
    Model for the users table.
    """
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String)
    hashed_password = Column(String)
    watchlist = relationship('Watchlist', back_populates='users')
