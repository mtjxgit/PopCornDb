"""
This module handles the authentication routes for the FastAPI application.
"""

from fastapi import Depends, APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database.database import get_db
from app import models
from app.schemas import authenticate as schemas

router = APIRouter(tags=["Authentication"])
template = Jinja2Templates(directory="frontend")

@router.get("/auth/signup")
def signup_page(request: Request):
    """
    Renders the signup page.
    """
    return template.TemplateResponse("signup.html", {"request": request})

@router.post("/auth/signup")
def handle_signup(
    request: Request, db: Session = Depends(get_db),
    form_data: schemas.signup = Depends(schemas.signup.as_form)
):
    """
    Handles the signup form submission.
    """
    new_user = models.User(
        name=form_data.name, username=form_data.username, password=form_data.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print(new_user)
    return template.TemplateResponse("login.html", {"request": request})

@router.get("/auth/login")
def login_page(request: Request):
    """
    Renders the login page.
    """
    return template.TemplateResponse("login.html", {"request": request})

@router.post("/auth/login")
def handle_login(
    request: Request,
    formdata: schemas.login = Depends(schemas.login.as_login_form),
    db: Session = Depends(get_db)
):
    """
    Handles the login form submission.
    """
    user = db.query(models.User).filter(models.User.username == formdata.username).first()
    if user and formdata.password == user.password:
        return RedirectResponse(url=f"/home/{user.user_id}", status_code=303)
    return template.TemplateResponse("login.html",
                                 {"request": request, "error": "Invalid username or password"})

@router.get("/auth/logout")
def logout(request: Request):
    """
    Logs the user out and renders the login page.
    """
    return template.TemplateResponse("login.html", {"request": request})
