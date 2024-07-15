"""
This module contains the routes for the home page and search functionality.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Request, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from scraper import scrape_news
from app.database.database import get_db
from app.models import models

router = APIRouter(tags=["Home"])
template = Jinja2Templates(directory="frontend")



@router.get("/search", tags=["search"])
def search_movie(movie_id: str, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Search route that redirects to the movie page.

    Args:
        movie_id (str): The ID of the movie.
        user_id (Optional[int], optional): The ID of the user. Defaults to None.
        db (Session): Database session.

    Returns:
        RedirectResponse: Redirects to the movie page.
    """
    movie = db.query(models.Movies).filter(models.Movies.title == movie_id).first()
    movie_index = movie.index
    if user_id:
        return RedirectResponse(url=f"/m/{movie_index}/{user_id}")
    return RedirectResponse(url=f"/m/{movie_index}")
