"""
This module handles the authentication routes for the FastAPI application.
"""

from fastapi import Depends, APIRouter, Request,HTTPException,status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse,HTMLResponse
from datetime import timedelta
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import models
from app.schemas import authenticate as schemas
from app.security.security import create_access_token,authenticate_user
from app.security.hashing import get_password_hash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from app.security.security import ACCESS_TOKEN_EXPIRE_MINUTES


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(tags=["Authentication"])
template = Jinja2Templates(directory="frontend")


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db:Session=Depends(get_db)
) -> schemas.Token:
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

templates = Jinja2Templates(directory="frontend")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db:Session=Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Incorrect username or password"})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    response = RedirectResponse(url="/home", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@router.get("/signup")
def create_user(request:Request):
    return templates.TemplateResponse("signup.html",{"request":request})


@router.post("/signup")
def handle_signup(
request: Request, db: Session = Depends(get_db),
form_data: schemas.SignUp = Depends(schemas.SignUp.as_form)
):
    """
    Handles the signup form submission.
    """
    check = db.query(models.Users).filter(models.Users.username == form_data.username).first()
    if check:
        return templates.TemplateResponse("login.html", {"request": request,"error":"user already registered"})

    hashed_password = get_password_hash(form_data.password)
    new_user = models.Users(hashed_password=hashed_password,
        name=form_data.name, username=form_data.username, 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return templates.TemplateResponse("login.html", {"request": request})