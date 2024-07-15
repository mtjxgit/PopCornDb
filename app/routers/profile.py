from fastapi import Depends, APIRouter,Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db
from .. import  models

router = APIRouter(prefix="/profile",tags=["Profile"])

template = Jinja2Templates(directory="frontend")
 


@router.get("/u/{uid}")
def profile(uid:int,
            request: Request, 
            db:Session = Depends(get_db)  
            ):
    
    user = db.query(models.User).filter(
        models.User.user_id == uid).first()
    
    watchlists = db.query(models.Watchlist).filter(models.Watchlist.user_id==uid).all()
    

    ratings = db.query(models.Ratings).filter(models.Ratings.user_id==uid).all()
    
    watched = []
    for item in ratings:
        movie = db.query(models.Movies).filter(
            models.Movies.index == item.movie_id
        ).first()
        watched.append(movie)
    watchlist=[]
    for item in watchlists:
        movie = db.query(models.Movies).filter(
            models.Movies.index == item.movie_id
        ).first()

        watchlist.append(movie)
    
    return template.TemplateResponse("profile.html",
        {
        "request":request,
        "watchlist":watchlist,
        "rated": watched,
        "user": user
        }
    )

@router.delete('/{id}')
def delete_user(id, db: Session = Depends(get_db)):
    temp = db.query(models.User).filter(models.User.user_id == id).first()
    popped = temp.name
    db.delete(temp)
    db.commit()
    return {"data": f" {popped} deleted"}


@router.get('/{uid}')
def reccommendations(id,db:Session=Depends(get_db)):
    movie_ids = db.query(models.Ratings).filter(models.Ratings.user_id == id and models.Ratings.rating>9).all()
    fav_genres= []
    for item in movie_ids:
        movie = db.query(models.Movies).filter(models.Movies.index == item.movie_id).first()
        tags = movie.genre
        if tags not in fav_genres:
            fav_genres.append(tags)
    final = []
    for genre in fav_genres:
        reccommends = db.query(models.Movies).filter(models.Movies.genre == genre).all()
        for item in reccommends:
            final.append(item.title)
    return final

    
        
    
    
