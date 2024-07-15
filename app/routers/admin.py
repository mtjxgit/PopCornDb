from fastapi import Depends,Form , APIRouter
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db
from .. import  models
from ..schemas import movies as schemas

router = APIRouter(prefix="/admin",tags=["Admin"])
template = Jinja2Templates(directory="frontend")

@router.patch("/{id}")
def update_rating(id,request :float = Form( ... ),db:Session=Depends(get_db)):
    temp = db.query(models.Movies).filter(models.Movies.index == id).first()
    temp.rating = request.rating
    db.commit()
    db.refresh(temp)
    return temp

@router.delete("/{id}")
def delete_movie(id,db:Session=Depends(get_db)):
    temp = db.query(models.Movies).filter(models.Movies.index == id).first()
    popped = temp.title
    db.delete(temp)
    db.commit()
    return {"data": f" {popped} deleted"}

@router.get('/ratings')
def view_ratings(db: Session = Depends(get_db)):
    all = db.query(models.Ratings).all()
    return all


@router.get('/users')
def show_all_users(db: Session = Depends(get_db)):
    new = db.query(models.User).all()
    return new

@router.post("/admin/",tags=['admin'])
def add_movie(request: schemas.movies, db: Session = Depends(get_db)):
    temp = request.model_dump()
    new  = models.Movies(**temp)
    db.add(new)   
    db.commit()
    db.refresh(new)
    return new
