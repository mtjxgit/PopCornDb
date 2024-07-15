from fastapi import APIRouter,Depends,Request,BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session
from Database.database import get_db
from .. import models
from scrapper import scrape_news
from typing import Optional


 

router = APIRouter(tags=["Home"])
template = Jinja2Templates(directory="UI")

@router.get("/home/{user_id}")
@router.get("/home")
async def home(
    request: Request, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user_id: Optional[int] = None,
):
    

    all_movies = db.query(models.Movies).all()
    unique_ott_list = db.query(models.Movies.ott).distinct().all()
    unique_ott_list = [ott[0] for ott in unique_ott_list if ott[0] != '' and ott[0] != '(' and ott[0] != ')']

    background_tasks.add_task(scrape_news.scrape)  # Run the scrape function in the background
    news = db.query(models.News).all()

    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    watchlistS = db.query(models.Watchlist).filter(models.Watchlist.user_id == user_id).all()

    watchlist = []
    for item in watchlistS:
        movie = db.query(models.Movies).filter(models.Movies.index == item.movie_id).first()
        watchlist.append(movie)

    ten = db.query(models.Movies).limit(10).all()
    topten = []
    for item in ten:
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
def search_movie(movie_id: str, user_id: Optional[int] = None, db:Session = Depends(get_db)):
    movie= db.query(models.Movies).filter(models.Movies.title==movie_id).first()
    mid = movie.index
    if user_id:
        return RedirectResponse(url=f"/m/{mid}/{user_id}")
    return RedirectResponse(url=f"/m/{mid}")

