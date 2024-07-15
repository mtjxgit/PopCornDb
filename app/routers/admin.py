"""
Admin API routes for managing movies and users.

This module defines CRUD operations for movies, including updating ratings, deleting movies,
viewing ratings, and managing users.
"""

from fastapi import Depends, Form, APIRouter
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import models
from app.schemas import movies as schemas

router = APIRouter(prefix="/admin", tags=["Admin"])
template = Jinja2Templates(directory="frontend")

@router.patch("/{movie_id}")
def update_rating(movie_id: int, rating: float = Form(...), db: Session = Depends(get_db)):
    """
    Update the rating of a movie by its ID.
    """
    movie = db.query(models.Movies).filter(models.Movies.index == movie_id).first()
    if movie:
        movie.rating = rating
        db.commit()
        db.refresh(movie)
        return movie
    return {"error": "Movie not found"}

@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Delete a movie by its ID.
    """
    movie = db.query(models.Movies).filter(models.Movies.index == movie_id).first()
    if movie:
        title = movie.title
        db.delete(movie)
        db.commit()
        return {"data": f"{title} deleted"}
    return {"error": "Movie not found"}

@router.get('/ratings')
def view_ratings(db: Session = Depends(get_db)):
    """
    View all movie ratings.
    """
    ratings = db.query(models.Ratings).all()
    return ratings

@router.get('/users')
def show_all_users(db: Session = Depends(get_db)):
    """
    Show all users.
    """
    users = db.query(models.User).all()
    return users

@router.post("/movie")
def add_movie(request: schemas.Movie, db: Session = Depends(get_db)):
    """
    Add a new movie.
    """
    movie_data = request.dict()
    new_movie = models.Movies(**movie_data)
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie
