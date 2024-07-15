from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from .routers import movies,authenticate,admin,home,profile
from database.database import Engine,Base
from typing import Optional






app = FastAPI()
template = Jinja2Templates(directory="UI")
Base.metadata.create_all(Engine)
  
app.include_router(movies.router)
app.include_router(authenticate.router)
app.include_router(admin.router)
app.include_router(home.router)
app.include_router(profile.router)

