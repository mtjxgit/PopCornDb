"""
This module contains the routes for movie details, adding to watchlist, and rating movies.
"""

from typing import Optional,Annotated
from fastapi import Depends, Request, HTTPException, Form, APIRouter
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import models
from app.schemas.user import User
from app.template_config import templates
from app.security.security import get_current_active_user
router = APIRouter(prefix="/m", tags=["Movies"])

@router.get("/{movie_id}")
def get_movie_details(
    movie_id: int,
    request: Request,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db)
):
    """
    Fetches and returns movie details.

    Args:
        movie_id (int): ID of the movie.
        request (Request): The request object.
        db (Session): Database session.
        user_id (Optional[int], optional): ID of the user. Defaults to None.

    Returns:
        TemplateResponse: The rendered template with movie details.
    """

    user = db.query(models.Users).filter(models.Users.username == current_user.username).first()
    movie = db.query(models.Movies).filter(
        models.Movies.index == movie_id
    ).first()

    if not movie:
        raise HTTPException(
            status_code=404, detail="Movie not found"
        )

    if user:
        
        is_in_watchlist = db.query(models.Watchlist).filter(
            models.Watchlist.user_id == user.user_id,
            models.Watchlist.movie_id == movie_id
        ).first() is not None

        rating_record = db.query(models.Ratings).filter(
            models.Ratings.movie_id == movie_id,
            models.Ratings.user_id == user.user_id
        ).first()
    else:
        is_in_watchlist = rating_record = user = False

    rating = rating_record.rating if rating_record else False

    return templates.TemplateResponse(
        "movie.html",
        {
            "request": request,
            "movie_details": movie,
            "user": user,
            "is_in_watchlist": is_in_watchlist,
            "rating": rating
        }
    )


@router.post("/{m_id}/watchlist")
def add_to_watchlist(
    m_id: int,
    current_user: Annotated[User,Depends(get_current_active_user)],
    db: Session = Depends(get_db)):

    """
    Adds a movie to the user's watchlist.

    Args:
        m_id (int): Movie ID.
        u_id (int): User ID.
        db (Session): Database session.

    Returns:
        RedirectResponse: Redirects to the movie details page.
    """
    user = db.query(models.Users).filter(models.Users.username==current_user.username).first()
    new = models.Watchlist(user_id=user.user_id, movie_id=m_id)
    db.add(new)
    db.commit()
    url = f"/m/{m_id}"
    response = RedirectResponse(url=url, status_code=303)
    return response


@router.post("/{m_id}/rate")
def add_rating(
    m_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    rating: float = Form(...),
    db: Session = Depends(get_db)
):
    """
    Adds a rating for a movie.

    Args:
        m_id (int): Movie ID.
        u_id (int): User ID.
        rating (float): Rating value.
        db (Session): Database session.

    Returns:
        RedirectResponse: Redirects to the movie details page.
    """
    if current_user:
        user = db.query(models.Users).filter(models.Users.username==current_user.username).first()
        new_rating = models.Ratings(movie_id=m_id, user_id= user.user_id, rating=rating)
        db.add(new_rating)
        db.commit()
        url = f"/m/{m_id}"
        response = RedirectResponse(url=url, status_code=303)
        return response
