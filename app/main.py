"""
Main module for the FastAPI application.

This module initializes the FastAPI application, sets up the database,
and includes various routers for different parts of the application.
"""

from fastapi import FastAPI
from .database.database import Engine, Base
from .routers import movies, authenticate, admin, home, profile
from fastapi.staticfiles import StaticFiles

app = FastAPI()
Base.metadata.create_all(Engine)


app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(movies.router)
app.include_router(authenticate.router)
app.include_router(admin.router)
app.include_router(home.router)
app.include_router(profile.router)

















