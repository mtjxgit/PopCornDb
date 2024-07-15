from fastapi import Depends,Request,HTTPException,Form , APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from typing import Optional
from sqlalchemy.orm import Session
from database.database import get_db
from .. import models

router = APIRouter(prefix="/m",tags=["Movies"])
template = Jinja2Templates(directory="frontend")

@router.get("/{movie_id}")
@router.get('/{movie_id}/{user_id}')
def get_movie_details(
    movie_id: int, 
    request: Request, 
    db: Session = Depends(get_db), 
    user_id: Optional[int] = None):

    movie = db.query(models.Movies).filter(
        models.Movies.index == movie_id
        ).first()
    
    if not movie:
        raise HTTPException(
            status_code=404, detail="Movie not found"
            )

    is_in_watchlist = rating_record = user =  False
    if user_id:
        user = db.query(models.User).filter(
            models.User.user_id == user_id
            ).first()

        is_in_watchlist = db.query(models.Watchlist).filter(
            models.Watchlist.user_id == user_id,
            models.Watchlist.movie_id == movie_id
        ).first() is not None

        rating_record = db.query(models.Ratings).filter(
            models.Ratings.movie_id == movie_id,
            models.Ratings.user_id == user_id
            ).first()

    rating = rating_record.rating if rating_record else 0

    return template.TemplateResponse(
        "movie.html",
        {
            "request": request,
            "movie_details": movie,
            "user": user,
            "is_in_watchlist": is_in_watchlist,
            "rating": rating
        }
    )
 
 
@router.post("/{m_id}/{u_id}/watchlist")
def add_to_watchlist(m_id: int, u_id: int, db: Session = Depends(get_db)):
    new = models.Watchlist(user_id=u_id, movie_id=m_id)
    db.add(new)
    db.commit()
    url = f"/m/{m_id}/{u_id}"
    response = RedirectResponse(url=url, status_code=303)
    return response

@router.post("/{m_id}/{u_id}/rate")
def add_rating(m_id: int,
               u_id: int, 
               rating: float = Form( ... ) ,
               db: Session = Depends(get_db)
               ):
    
    new_rating = models.Ratings(movie_id=m_id, user_id = u_id, rating=rating)
    db.add(new_rating)
    db.commit()
    url = f"/m/{m_id}/{u_id}"
    response = RedirectResponse(url=url, status_code=303)
    return response

