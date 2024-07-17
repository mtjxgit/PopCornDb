"""
This module contains the routes for the home page and search functionality.
"""

from typing import Optional,Annotated
from fastapi import APIRouter, Depends, Request, BackgroundTasks,HTTPException

from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from scraper import scrape_news
from app.database.database import get_db
from app.models.models import Movies,Watchlist,News,Users
from app.schemas.user import User
from app.security.security import get_current_active_user
from scraper import scrape_news

from fuzzywuzzy import process
from app.template_config import templates

router = APIRouter(tags=["Home"])


@router.get("/home")
async def protected_home(request: Request,background_task:BackgroundTasks,current_user: Annotated[User, Depends(get_current_active_user)],db: Session = Depends(get_db)):

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
    all_movies = db.query(Movies).all()
    unique_ott_list = db.query(Movies.ott).distinct().all()
    unique_ott_list = [ott[0] for ott in unique_ott_list if ott[0] not in ('', '(', ')')]

    background_task.add_task(scrape_news.scrape)
    news = db.query(News).all()

    user = None
    watchlist = None
    if current_user:
        user = db.query(Users).filter(Users.username == current_user.username).first()
        watchlist_items = db.query(Watchlist).filter(Watchlist.user_id == user.user_id).all()

        watchlist = []
        for item in watchlist_items:
            movie = db.query(Movies).filter(Movies.index == item.movie_id).first()
            watchlist.append(movie)
    
    top_ten_movies = db.query(Movies).limit(10).all()
    topten = []
    for item in top_ten_movies:
        movie = db.query(Movies).filter(Movies.index == item.index).first()
        topten.append(movie)

    return templates.TemplateResponse("index.html",
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
    
    movies = db.query(Movies).all()
    movie_titles = [movie.title for movie in movies]

    matched_movie, score = process.extractOne(movie_id, movie_titles, score_cutoff=60)

    if not matched_movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    movie = db.query(Movies).filter(Movies.title == matched_movie).first()
    movie_index = movie.index

    if user_id:
        return RedirectResponse(url=f"/m/{movie_index}/{user_id}")
    return RedirectResponse(url=f"/m/{movie_index}")
