from fastapi import Depends,APIRouter,Request,HTTPException,status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database.database import get_db
from .. import models
from ..schemas import authenticate as schemas



router= APIRouter(tags=["Authentication"])

template = Jinja2Templates(directory="frontend")



@router.get("/auth/signup")
def signup_page(request:Request):
    return template.TemplateResponse("signup.html",{"request":request})

@router.post("/auth/signup")
def signup_page(request:Request,db:Session = Depends(get_db),form_data: schemas.signup = Depends(schemas.signup.as_form)):
    new  = models.User(name = form_data.name,username= form_data.username,password=form_data.password)
    db.add(new)   
    db.commit()
    db.refresh(new)
    print(new)
    return template.TemplateResponse("login.html",{"request":request})

@router.get("/auth/login") 
def login_page(request:Request):
        return template.TemplateResponse("login.html",{"request":request})

@router.post("/auth/login")
def login_page(request: Request, formdata: schemas.login = Depends(schemas.login.as_login_form), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == formdata.username).first()
    if user and formdata.password == user.password:
        return RedirectResponse(url=f"/home/{user.user_id}", status_code=303)
    return template.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password"})
   
@router.get("/auth/logout")
def logout_out(request:Request):
    return template.TemplateResponse("login.html",{"request":request})
