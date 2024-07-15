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

@router.get("/home/{user_id}")
@router.get("/home")
async def home(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user_id: Optional[int] = None,
):
    """
    Home route that displays the main page.

    Args:
        request (Request): The request object.
        background_tasks (BackgroundTasks): Background tasks for scraping news.
        db (Session): Database session.
        user_id (Optional[int], optional): The ID of the user. Defaults to None.

    Returns:
        TemplateResponse: The rendered template response.
    """
    all_movies = db.query(models.Movies).all()
    unique_ott_list = db.query(models.Movies.ott).distinct().all()
    unique_ott_list = [ott[0] for ott in unique_ott_list if ott[0] not in ('', '(', ')')]

    background_tasks.add_task(scrape_news.scrape)  # Run the scrape function in the background
    news = db.query(models.News).all()

    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    watchlist_items = db.query(models.Watchlist).filter(models.Watchlist.user_id == user_id).all()

    watchlist = []
    for item in watchlist_items:
        movie = db.query(models.Movies).filter(models.Movies.index == item.movie_id).first()
        watchlist.append(movie)

    top_ten_movies = db.query(models.Movies).limit(10).all()
    topten = []
    for item in top_ten_movies:
        movie = db.query(models.Movies).filter(models.Movies.index == item.index).first()
        topten.append(movie)

    return template.TemplateResponse("index.html",
                                     {"request": request,
                                      "topten": topten,
                                      "watchlist": watchlist,
                                      "user": user,
                                      "news": news,
                                      "all": all_movies,
                                      "unique_ott_list": unique_ott_list
                                     })


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
