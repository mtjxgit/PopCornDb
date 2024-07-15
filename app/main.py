"""
Main module for the FastAPI application.

This module initializes the FastAPI application, sets up the database,
and includes various routers for different parts of the application.
"""

from fastapi import FastAPI
from .database.database import Engine, Base
from .routers import movies, authenticate, admin, home, profile

app = FastAPI()
Base.metadata.create_all(Engine)

app.include_router(movies.router)
app.include_router(authenticate.router)
app.include_router(admin.router)
app.include_router(home.router)
app.include_router(profile.router)


'''
functionality >> aesthetics
'''

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import HTTPException, status,Request,Depends,BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from sqlalchemy.orm import Session

from .database.database import get_db
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from .schemas.authenticate import Token,TokenData,SignUp,Login
from .schemas.user import User,UserInDB,CreateUser

from .models.models import Users,Movies,News,Ratings,Watchlist

from scraper import scrape_news

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db:Session, username: str):
    user = db.query(Users).filter(Users.username == username).first()
    print("X inside get_user:",user)
    if user:
        return UserInDB(**user.__dict__)


def authenticate_user(username: str, password: str,db:Session):
    user = get_user(db, username)
    print("X inside authenticate:",user)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(request: Request,db:Session=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db:Session=Depends(get_db)
) -> Token:
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
    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/me")
async def read_users_me(request: Request, current_user: Annotated[User, Depends(get_current_active_user)]):
    print(current_user)
    return current_user





templates = Jinja2Templates(directory="frontend")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
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

@app.get("/signup")
def create_user(request:Request):
    return templates.TemplateResponse("signup.html",{"request":request})


@app.post("/signup")
def handle_signup(
request: Request, db: Session = Depends(get_db),
form_data: SignUp = Depends(SignUp.as_form)
):
    """
    Handles the signup form submission.
    """
    hashed_password = get_password_hash(form_data.password)
    new_user = Users(hashed_password=hashed_password,
        name=form_data.name, username=form_data.username, 
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/home")
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

    background_task.add_task(scrape_news.scrape)  # Run the scrape function in the background
    news = db.query(News).all()

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
