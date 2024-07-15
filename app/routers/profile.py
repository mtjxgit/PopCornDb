"""
This module contains the routes for user profiles, including viewing profiles,
deleting users, and getting recommendations.
"""

from fastapi import Depends, APIRouter, Request,HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import models

router = APIRouter(prefix="/profile", tags=["Profile"])

template = Jinja2Templates(directory="frontend")


@router.get("/u/{uid}")
def profile(uid: int, request: Request, db: Session = Depends(get_db)):
    """
    Fetches and returns the user's profile details.

    Args:
        uid (int): User ID.
        request (Request): The request object.
        db (Session): Database session.

    Returns:
        TemplateResponse: The rendered template with user profile details.
    """
    user = db.query(models.User).filter(models.User.user_id == uid).first()

    watchlists = db.query(models.Watchlist).filter(models.Watchlist.user_id == uid).all()

    ratings = db.query(models.Ratings).filter(models.Ratings.user_id == uid).all()

    watched = []
    for item in ratings:
        movie = db.query(models.Movies).filter(models.Movies.index == item.movie_id).first()
        watched.append(movie)

    watchlist = []
    for item in watchlists:
        movie = db.query(models.Movies).filter(models.Movies.index == item.movie_id).first()
        watchlist.append(movie)

    return template.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "watchlist": watchlist,
            "rated": watched,
            "user": user
        }
    )


@router.delete('/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Deletes a user by ID.

    Args:
        user_id (int): User ID.
        db (Session): Database session.

    Returns:
        dict: Confirmation message of user deletion.
    """
    temp = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not temp:
        raise HTTPException(status_code=404, detail="User not found")

    popped = temp.name
    db.delete(temp)
    db.commit()
    return {"data": f"{popped} deleted"}


@router.get('/{uid}')
def recommendations(uid: int, db: Session = Depends(get_db)):
    """
    Provides movie recommendations for the user based on their highest rated genres.

    Args:
        uid (int): User ID.
        db (Session): Database session.

    Returns:
        list: List of recommended movie titles.
    """
    movie_ids = db.query(models.Ratings).filter(
        models.Ratings.user_id == uid, models.Ratings.rating > 9).all()

    fav_genres = []
    for item in movie_ids:
        movie = db.query(models.Movies).filter(models.Movies.index == item.movie_id).first()
        tags = movie.genre
        if tags not in fav_genres:
            fav_genres.append(tags)

    final = []
    for genre in fav_genres:
        recommends = db.query(models.Movies).filter(models.Movies.genre == genre).all()
        for item in recommends:
            final.append(item.title)
    return final
